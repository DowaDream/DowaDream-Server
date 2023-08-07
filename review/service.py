from config import settings
import boto3
from django.http import JsonResponse

from .response import *
from .serializers import *


### Review save 관련 메소드
def save_review(request, review):
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return JsonResponse(ReviewTooManyImages(), status=400)
    
    request.data['writer'] = request.user.id    # 현재 로그인된 user를 writer로
    
    if review is None:
        serializer = ReviewSerializer(data=request.data)    # post인 경우 새로운 review 생성
    else:
        serializer = ReviewSerializer(review, data=request.data) # put인 경우 기존의 review를 수정
    
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    review_instance = serializer.save()     # review를 DB에 저장
    s3_urls = save_images_db(images, review_instance.rid)   # image를 DB에 저장
    
    review_serializer_data = serializer.data
    review_serializer_data["images"] = s3_urls
    return review_serializer_data


def save_image_s3(image, rid):      # S3에 이미지 저장
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


def save_images_db(images, rid):
    s3_urls = []
    for image in images:
        image_serializer = ImageSerializer(data={"image": image, "review":rid})
        if not image_serializer.is_valid():
            return JsonResponse(ReviewImageFormatError(image_serializer.errors), status=400)
        s3_url = save_image_s3(image, rid)
        s3_urls.append(s3_url)
        image_serializer.validated_data["image"] = s3_url
        image_serializer.save()
    return s3_urls