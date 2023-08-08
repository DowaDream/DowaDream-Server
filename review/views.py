from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import IsWriterOrReadOnly
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import *
from .response import *
from .comment_service import *
from .review_service import *


def responseFactory(res: ResponseDto):
    if res.data is None:
        return JsonResponse(
            status=res.status,
            data={
                "msg": res.msg
            }
        )
    else:
        return JsonResponse(
            status=res.status,
            data={
                "msg": res.msg,
                "data": res.data
            }
        )


### Review ###
class ReviewList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @transaction.atomic     # 오류 생기면 롤백
    def post(self, request):
        res = post_review(request)
        if res.status >= 400:
            transaction.set_rollback(True)
        return responseFactory(res)
    
    def get(self, request):
        progrmRegistNo = request.GET.get('progrmRegistNo')
        print(progrmRegistNo, type(progrmRegistNo))
        if progrmRegistNo is None:
            data = get_review_list()
        else:
            data = get_review_list_in_progrm(progrmRegistNo)
        return responseFactory(data)


class ReviewDetail(APIView):
    permission_classes = [IsWriterOrReadOnly]
    
    def get(self, request, rid):
        data = get_one_review(rid)
        return responseFactory(data)
    
    @transaction.atomic     # 오류 생기면 롤백
    def put(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        self.check_object_permissions(self.request, review) # 인가 체크
        res = put_review(request, review)
        
        if res.status >= 400:
            transaction.set_rollback(True)
        return responseFactory(res)

    def delete(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        self.check_object_permissions(self.request, review)
        res = delete_review(review)
        return responseFactory(res)



### Comment ###
class CommentList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, rid):
        data = get_comment(rid)
        return responseFactory(data)

    def post(self, request, rid):
        res = save_comment(request, rid, None)
        return responseFactory(res)


class CommentDetail(APIView):
    permission_classes = [IsWriterOrReadOnly]
    
    def put(self, request, rid, cid):
        comment = get_object_or_404(Comment, cid=cid)
        self.check_object_permissions(self.request, comment)
        res = save_comment(request, rid, comment)
        return responseFactory(res)
    
    def delete(self, request, rid, cid):
        comment = get_object_or_404(Comment, cid=cid)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return JsonResponse(status=204, data={'msg': message['CommentDeleteSuccess']})