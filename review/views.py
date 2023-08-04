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
    # @transaction.atomic     # 오류 생기면 롤백
    def post(self, request):
        review_serializer = ReviewSerializer(data=request.data)
        if not review_serializer.is_valid():
            return JsonResponse(ReviewCreateFailed(review_serializer.errors), status=400)
        
        # 모두 valid한 경우 저장
        review_instance = review_serializer.save()
        
        images = request.data.getlist('images')
        
        for image in images:    # image 파일 validation 검사
            image_serializer = ImageSerializer(data={"image": image, "review":review_instance.rid})
            if not image_serializer.is_valid():
                return JsonResponse(ReviewImageFormatError(image_serializer.errors), status=400)
            s3_url = save_image(image, review_instance.rid)
            image_serializer.validated_data["image"] = s3_url
            image_serializer.save()
        
        # for image in images:
        #     try:
        #         s3_url = save_image(image, review_instance.rid)
        #         new_image = Image.objects.create(
        #             image = s3_url,
        #             review = review_instance
        #         )
        #     except:
        #         response = JsonResponse(ReviewImageUploadError, status=500)
        
        # 모두 완료되면 commit
        # if 400 <= response.status_code < 600:
        #     transaction.set_rollback(True)
        response = JsonResponse(ReviewCreateSuccessed(review_serializer.data), status=201)
        
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