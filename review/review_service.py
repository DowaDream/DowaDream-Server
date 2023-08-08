from .models import *
from .response import *
from .serializers import ReviewSerializer
from .image_service import *


def post_review(request) -> ResponseDto:
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return ResponseDto(status=400, msg=message["TooManyImages"])
    
    # Review serializer & save
    mutable_data = request.data.copy()
    mutable_data['writer'] = request.user.id    # 현재 로그인된 user를 writer로
    serializer = ReviewSerializer(data=mutable_data)
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    review_instance = serializer.save()     # review를 DB에 저장
    
    # Image serializer & save
    s3_urls = save_images_db(images, review_instance.rid)   # image를 DB에 저장
    if s3_urls is None:
        return ResponseDto(status=400, msg=message['ImageFormatError'])
    
    data = serializer.data
    data["images"] = s3_urls
    return ResponseDto(status=201, data=data, msg=message['ReviewCreateSuccess'])


def put_review(request, review) -> ResponseDto:
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return ResponseDto(status=400, msg=message["TooManyImages"])
    
    # Review serializer & save
    mutable_data = request.data.copy()
    mutable_data['writer'] = request.user.id
    serializer = ReviewSerializer(review, data=mutable_data)
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    review_instance = serializer.save()
    
    # Image serializer & save
    delete_images_db(review.rid)    # 기존의 images 삭제
    s3_urls = save_images_db(images, review_instance.rid)   # image를 DB에 저장
    if s3_urls is None:
        return ResponseDto(status=400, msg=message['ImageFormatError'])
    
    data = serializer.data
    data["images"] = s3_urls
    return ResponseDto(status=200, data=data, msg=message['ReviewPutSuccess'])


def get_review_list() -> ResponseDto:
    review_list = []
    reviews = Review.objects.all()
    for review in reviews:
        images = Image.objects.filter(review__rid=review.rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [image.image.url for image in images]
        review_list.append(review_data)
    return ResponseDto(status=200, data=review_list, msg=message['ReviewListGetSuccess'])


def get_review_list_in_progrm(progrmRegistNo) -> ResponseDto:
    review_list = []
    reviews = Review.objects.filter(progrmRegistNo=progrmRegistNo)
    for review in reviews:
        images = Image.objects.filter(review__rid=review.rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [image.image.url for image in images]
        review_list.append(review_data)
    return ResponseDto(status=200, data=review_list, msg=message['ReviewListInProgramGetSuccess'])


def get_one_review(rid) -> ResponseDto:
    try:
        review = Review.objects.get(rid=rid)
        images = Image.objects.filter(review__rid=rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [image.image.url for image in images]
        return ResponseDto(status=200, data=review_data, msg=message['ReviewGetSuccess'])
    except Review.DoesNotExist:
        return ResponseDto(status=404, msg=message['ReviewNotFound'])


def delete_review(review):
    res = delete_images_db(review.rid)
    review.delete()
    if res == 204:   # 삭제 성공
        return ResponseDto(status=204, msg=message['ReviewDeleteSuccess'])
    elif res == 404:
        return ResponseDto(status=400, msg=message['ReviewNotFound'])
    else:
        return ResponseDto(status=500, msg=message['ReviewDeleteFailed'])
