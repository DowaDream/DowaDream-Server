from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import IsWriterOrReadOnly
from django.http import JsonResponse

from .models import *
from .serializers import *
from .response import *
from .service import *


class ReviewList(APIView):
    def post(self, request):
        images = request.data.getlist('images')
        
        for image in images:    # image 파일 validation 검사
            image_serializer = ImageSerializer(data={"image": image, "rid":1})
            if not image_serializer.is_valid():
                return JsonResponse(ReviewImageFormatError(image_serializer.errors), status=400)
        
        review_serializer = ReviewSerializer(data=request.data)
        if not review_serializer.is_valid():
            return JsonResponse(ReviewCreateFailed(review_serializer.errors), status=400)
        
        # 모두 valid한 경우 저장
        review_instance = review_serializer.save()
        # review_serializer.data['images'] = []
        for image in images:
            try:
                s3_url = save_image(image)
                new_image = Image.objects.create(
                    image = s3_url,
                    rid = review_instance.rid
                )
                # review_serializer.data['images'].append(s3_url)
            except:
                return JsonResponse(ReviewImageUploadError, status=500)
        
        return JsonResponse(ReviewCreateSuccessed(review_serializer.data), status=201)
    
    
    def get(self, request):
        return


class ReviewDetail(APIView):
    def get(self, request, rid):
        return
    
    def put(self, request, rid):
        return
    
    def delete(self, request, rid):
        return