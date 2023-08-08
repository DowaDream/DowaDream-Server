from .response import *
from .serializers import *
from .s3_manager import *


### 리뷰 관련 메소드
# 리뷰 생성
def post_review(request) -> ResponseDto:
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return ResponseDto(status=400, msg=message["TooManyImages"])
    
    mutable_data = request.data.copy()
    mutable_data['writer'] = request.user.id    # 현재 로그인된 user를 writer로
    serializer = ReviewSerializer(data=mutable_data)
    
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    review_instance = serializer.save()     # review를 DB에 저장
    s3_urls = save_images_db(images, review_instance.rid)   # image를 DB에 저장
    
    if s3_urls is None:
        return ResponseDto(status=400, msg=message['ImageFormatError'])
    
    data = serializer.data
    data["images"] = s3_urls
    return ResponseDto(status=201, data=data, msg=message['ReviewCreateSuccess'])


# 리뷰 수정
def put_review(request, review) -> ResponseDto:
    images = request.data.getlist('images', [])  # 기본 값을 빈 리스트로 지정
    if len(images[0]) == 0:     # 자동으로 ['']이 들어가기 때문에 한번 더 체크
        images = []
    elif len(images) > 5:
        return ResponseDto(status=400, msg=message["TooManyImages"])
    
    mutable_data = request.data.copy()
    mutable_data['writer'] = request.user.id    # 현재 로그인된 user를 writer로
    serializer = ReviewSerializer(review, data=mutable_data)
    
    if not serializer.is_valid():
        return ResponseDto(status=400, msg=serializer.errors)
    review_instance = serializer.save()     # review를 DB에 저장
    
    print(mutable_data['images'])
    delete_image_s3(mutable_data['images'])
    s3_urls = save_images_db(images, review_instance.rid)   # image를 DB에 저장
    
    if s3_urls is None:
        return ResponseDto(status=400, msg=message['ImageFormatError'])
    
    data = serializer.data
    data["images"] = s3_urls
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