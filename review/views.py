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


class ReviewList(APIView):
    @transaction.atomic     # 오류 생기면 롤백
    def post(self, request):
        try:
            images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
            if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
                images = []
            
            if len(images) > 5:
                response = JsonResponse(ReviewTooManyImages(), status=400)
                raise Exception()
            
            review_serializer_data = save_review(request, images)
            if isinstance(review_serializer_data, JsonResponse):
                response = review_serializer_data
                raise Exception()
            response = JsonResponse(ReviewCreateSuccessed(review_serializer_data), status=201)
        
        except:
            transaction.set_rollback(True)
        finally:
            return response
    
    
    def get(self, request):
        return


class ReviewDetail(APIView):
    def get(self, request, rid):
        return
    
    def put(self, request, rid):
        return

    def delete(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        review.delete()
        return JsonResponse(ReviewDeleteSuccess(rid), status=204)