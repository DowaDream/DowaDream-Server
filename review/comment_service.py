from .models import *
from .response import *
from .serializers import CommentSerializer


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