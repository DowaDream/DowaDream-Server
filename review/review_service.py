from .models import *
from .response import *
from .serializers import ReviewSerializer
from .image_service import *
from django.db.models import Count
from user.service import get_userinfo
from program.search_service import callByRegistNo


def post_review(request) -> ResponseDto:
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return ResponseDto(status=400, msg=message["TooManyImages"])
    
    # Review serializer & save
    mutable_data = request.data.copy()
    mutable_data['writer'] = request.user.id    # 현재 로그인된 user를 writer로
    
    # 봉사 정보 찾아와서 Review DB에 넣어주기
    program = callByRegistNo(mutable_data['progrmRegistNo'])
    mutable_data['tag'] = program['tagCode']
    mutable_data['region'] = program['areaCode']
    
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
    
    # 봉사 정보 찾아와서 Review DB에 넣어주기
    program = callByRegistNo(mutable_data['progrmRegistNo'])
    mutable_data['tag'] = program['tagCode']
    mutable_data['region'] = program['areaCode']
    
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


# Code Refactoring: 반복되는 코드: 리뷰 리스트 조회하기
def get_reviews(reviews):
    review_list = []
    for review in reviews:
        images = Image.objects.filter(review__rid=review.rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [str(image.image) for image in images]
        
        # 작성자 이름, 작성자 프로필 가져오기
        user = User.objects.get(id=review_data['writer'])
        user_info = get_userinfo(user)
        review_data['writer_username'] = user.username
        review_data['writer_profile_img'] = str(user.profile_img)
        
        review_data['num_cheer'] = get_cheered_review_count(review)
        review_data['num_comment'] = get_comment_count(review)
        
        # 맞춤 후기인지 검사
        # if review_data['']
        
        
        review_list.append(review_data)
    return review_list

def get_cheered_review_count(review):
    cheered_count = Cheered_Review.objects.filter(review=review).count()
    return cheered_count

def get_comment_count(review):
    comment_count = Comment.objects.filter(review=review).count()
    return comment_count


def get_all_review_list() -> ResponseDto:
    reviews = Review.objects.filter(is_public=True).order_by('-created_at')
    review_list = get_reviews(reviews)
    return ResponseDto(status=200, data=review_list, msg=message['AllReviewListGetSuccess'])


def get_user_review_list(user) -> ResponseDto:
    reviews = Review.objects.filter(writer=user).order_by('-created_at')  # created_at 필드 기준으로 내림차순 정렬
    review_list = get_reviews(reviews)
    return ResponseDto(status=200, data=review_list, msg=message['UserReviewListGetSuccess'])


def get_review_list_in_progrm(progrmRegistNo) -> ResponseDto:
    reviews = Review.objects.filter(progrmRegistNo=progrmRegistNo).order_by('-created_at')  # created_at 필드 기준으로 내림차순 정렬
    review_list = get_reviews(reviews)
    return ResponseDto(status=200, data=review_list, msg=message['ReviewListInProgramGetSuccess'])


def get_one_review(rid) -> ResponseDto:
    try:
        review = Review.objects.get(rid=rid)
        images = Image.objects.filter(review__rid=rid)
        review_data = ReviewSerializer(review).data
        review_data["images"] = [str(image.image) for image in images]
        return ResponseDto(status=200, data=review_data, msg=message['ReviewGetSuccess'])
    except Review.DoesNotExist:
        return ResponseDto(status=404, msg=message['ReviewNotFound'])


def delete_review(review) -> ResponseDto:
    res = delete_images_db(review.rid)
    review.delete()
    if res == 204:   # 삭제 성공
        return ResponseDto(status=204, msg=message['ReviewDeleteSuccess'])
    elif res == 404:
        return ResponseDto(status=400, msg=message['ReviewNotFound'])
    else:
        return ResponseDto(status=500, msg=message['ReviewDeleteFailed'])


### 리뷰 응원하기
def cheer_review(user, rid) -> ResponseDto:
    try:
        review = Review.objects.get(rid=rid)
    except Review.DoesNotExist:
        return ResponseDto(status=404, msg=message['ReviewNotFound'])
        
    cheer, is_created = Cheered_Review.objects.get_or_create(writer=user, review=review)
    if is_created:
        return ResponseDto(status=201, msg=message['CheerReviewSuccess'])
    else:
        return ResponseDto(status=400, msg=message['AlreadyCheered'])


def cancel_cheering_review(user, rid) -> ResponseDto:
    try:
        review = Review.objects.get(rid=rid)
    except Review.DoesNotExist:
        return ResponseDto(status=404, msg=message['ReviewNotFound'])
        
    try:
        cheered_review = Cheered_Review.objects.get(writer=user, review=review)
        cheered_review.delete()
        return ResponseDto(status=204, msg=message['CancelCheeringSuccess'])
    except Cheered_Review.DoesNotExist:
        return ResponseDto(status=400, msg=message['CancelCheeringFail'])