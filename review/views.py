from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import IsWriterOrReadOnly
from django.http import JsonResponse
from django.db import transaction

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
            
            review_serializer = ReviewSerializer(data=request.data)
            if not review_serializer.is_valid():
                response = JsonResponse(ReviewCreateFailed(review_serializer.errors), status=400)
                raise Exception()
            review_instance = review_serializer.save()
            
            s3_urls = []
            for image in images:
                image_serializer = ImageSerializer(data={"image": image, "review":review_instance.rid})
                if not image_serializer.is_valid():
                    response = JsonResponse(ReviewImageFormatError(image_serializer.errors), status=400)
                    raise Exception()
                s3_url = save_image(image, review_instance.rid)
                s3_urls.append(s3_url)
                image_serializer.validated_data["image"] = s3_url
                image_serializer.save()
            
            review_serializer_data = review_serializer.data
            review_serializer_data["images"] = s3_urls
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
        return