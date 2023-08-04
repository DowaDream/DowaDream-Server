from config import settings
import boto3
from django.http import JsonResponse

from .response import *
from .serializers import *


def save_image(image, rid):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        file_path = image.name
        s3.upload_fileobj(image, bucket_name, file_path)
        s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{rid}/{file_path}"
        return s3_url
        
    except:
        return Exception("s3 이미지 업로드 실패")


def save_review(request, images):
    review_serializer = ReviewSerializer(data=request.data)
    if not review_serializer.is_valid():
        return JsonResponse(ReviewCreateFailed(review_serializer.errors), status=400)
    review_instance = review_serializer.save()
            
    s3_urls = []
    for image in images:
        image_serializer = ImageSerializer(data={"image": image, "review":review_instance.rid})
        if not image_serializer.is_valid():
            return JsonResponse(ReviewImageFormatError(image_serializer.errors), status=400)
        s3_url = save_image(image, review_instance.rid)
        s3_urls.append(s3_url)
        image_serializer.validated_data["image"] = s3_url
        image_serializer.save()
            
    review_serializer_data = review_serializer.data
    review_serializer_data["images"] = s3_urls
    return review_serializer_data