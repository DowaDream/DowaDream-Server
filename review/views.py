from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import IsWriterOrReadOnly
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *
from .response import *
from .service import *


# 나중에 로그인한 유저로 자동 writer 추가
class ReviewList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @transaction.atomic     # 오류 생기면 롤백
    def post(self, request):
        try:
            review_serializer_data = save_review(request)
            if isinstance(review_serializer_data, JsonResponse):
                response = review_serializer_data
                raise Exception()
            response = JsonResponse(ReviewCreateSuccessed(review_serializer_data), status=201)
        except:
            transaction.set_rollback(True)
        finally:
            return response
    
    def get(self, request):
        try:
            review_lists = []
            reviews = Review.objects.all()
            for review in reviews:
                images = Image.objects.filter(review__rid=review.rid)
                review_data = ReviewSerializer(review).data
                review_data["images"] = [image.image.url for image in images]
                review_lists.append(review_data)
            
            return JsonResponse(ReviewGetListSuccess(review_lists), status=200)
        except:
            return JsonResponse(ReviewGetListFail(), status=500)


class ReviewDetail(APIView):
    permission_classes = [IsWriterOrReadOnly]
    
    def get(self, request, rid):
        try:
            review = get_object_or_404(Review, rid=rid)
            images = Image.objects.filter(review__rid=rid)
            review_data = ReviewSerializer(review).data
            review_data["images"] = [image.image.url for image in images]
            return JsonResponse(ReviewDetailGetSuccess(review_data), status=200)
        except:
            return JsonResponse(ReviewDetailGetFail(), status=500)

    
    @transaction.atomic     # 오류 생기면 롤백
    def put(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        self.check_object_permissions(self.request, review)
        try:
            review_serializer_data = put_review(request, review)
            if isinstance(review_serializer_data, JsonResponse):
                response = review_serializer_data
                raise Exception()
            return JsonResponse(ReviewPutSuccess(review_serializer_data), status=200)
        except:
            transaction.set_rollback(True)
            return response


    def delete(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        self.check_object_permissions(self.request, review)
        review.delete()
        return JsonResponse(ReviewDeleteSuccess(rid), status=204)



### Comment ###
class CommentList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        comments = Comment.objects.filter(review=review)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(CommentGetSuccess(serializer.data), status=200)

    def post(self, request, rid):
        request.data['review'] = rid
        request.data['writer'] = request.user.id    # 현재 로그인된 user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(CommentCreateSuccess(serializer.data), status=201)
        return JsonResponse(CommentCreateFail(serializer.errors), status=400)


class CommentDetail(APIView):
    permission_classes = [IsWriterOrReadOnly]
    
    def put(self, request, rid, cid):
        comment = get_object_or_404(Comment, cid=cid)
        self.check_object_permissions(self.request, comment)
        
        request.data['cid'] = comment.cid
        request.data['writer'] = request.user.id    # 현재 로그인된 user
        request.data['review'] = rid
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(CommentPutSuccess(serializer.data), status=201)
        return JsonResponse(CommentPutFail(serializer.errors), status=400)
    
    def delete(self, request, rid, cid):
        comment = get_object_or_404(Comment, cid=cid)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return JsonResponse(CommentDeleteSuccess(cid), status=204)