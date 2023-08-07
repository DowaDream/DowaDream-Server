from config import settings
import boto3
from django.http import JsonResponse

from .response import *
from .serializers import *


### 리뷰 관련 메소드
# 리뷰 생성/수정 메소드
def save_review(request, review) -> ResponseDto:
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return ResponseDto(status=400, msg=message["TooManyImages"])
    
    mutable_data = request.data.copy()
    mutable_data['writer'] = request.user.id    # 현재 로그인된 user를 writer로
    
    if review is None:
        serializer = ReviewSerializer(data=mutable_data)    # post인 경우 새로운 review 생성
    else:
        serializer = ReviewSerializer(review, data=mutable_data) # put인 경우 기존의 review를 수정
    
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    review_instance = serializer.save()     # review를 DB에 저장
    s3_urls = save_images_db(images, review_instance.rid)   # image를 DB에 저장
    
    if s3_urls is None:
        return ResponseDto(status=400, msg=message['ImageFormatError'])
    
    data = serializer.data
    data["images"] = s3_urls
    if review is None:
        return ResponseDto(status=201, data=data, msg=message['ReviewCreateSuccess'])
    else:
        return ResponseDto(status=200, data=data, msg=message['ReviewPutSuccess'])


# 리뷰 리스트 조회
def get_review_list() -> ResponseDto:
    review_list = []
    reviews = Review.objects.all()
    for review in reviews:
        images = Image.objects.filter(review__rid=review.rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [image.image.url for image in images]
        review_list.append(review_data)
    return ResponseDto(status=200, data=review_list, msg=message['ReviewListGetSuccess'])


# 단일 리뷰 조회
def get_one_review(rid) -> ResponseDto:
    try:
        review = Review.objects.get(rid=rid)
        images = Image.objects.filter(review__rid=rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [image.image.url for image in images]
        return ResponseDto(status=200, data=review_data, msg=message['ReviewGetSuccess'])
    except Review.DoesNotExist:
        return ResponseDto(status=404, msg=message['ReviewNotFound'])



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
        print("s3 이미지 업로드 불가")
        return None

def save_images_db(images, rid):
    s3_urls = []
    for image in images:
        image_serializer = ImageSerializer(data={"image": image, "review":rid})
        if not image_serializer.is_valid():
            print("이미지 형식이 아님")
            return None
        
        s3_url = save_image_s3(image, rid)
        if s3_url is None:
            return None
        
        s3_urls.append(s3_url)
        image_serializer.validated_data["image"] = s3_url
        image_serializer.save()
    return s3_urls




### 댓글 관련 메소드
def get_comment(rid) -> ResponseDto:
    try:
        review = Review.objects.get(rid=rid)
        comments = Comment.objects.filter(review=review)
        serializer = CommentSerializer(comments, many=True)
        return ResponseDto(status=200, data=serializer.data, msg=message['CommentGetSuccess'])
    except Review.DoesNotExist:
        return ResponseDto(status=404, msg=message['ReviewNotFound'])

def save_comment(request, rid, comment):
    request.data['review'] = rid
    request.data['writer'] = request.user.id    # 현재 로그인된 user
    
    if comment is None:     # post일 때
        serializer = CommentSerializer(data=request.data)
    else:   # put일 때
        serializer = CommentSerializer(comment, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        if comment is None:
            return ResponseDto(status=201, data=serializer.data, msg=message['CommentCreateSuccess'])
        else:
            return ResponseDto(status=200, data=serializer.data, msg=message['CommentPutSuccess'])
    return ResponseDto(status=400, msg=message['InvalidFormat'])