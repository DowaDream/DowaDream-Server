from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from config.permissions import IsWriterOrReadOnly
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .response import *
from .comment_service import *
from .review_service import *
from .serializers import *


def responseFactory(res: ResponseDto):
    if res.data is None:
        return JsonResponse(status=res.status, data={ "msg": res.msg })
    else:
        return JsonResponse(
            status=res.status,
            data={ "msg": res.msg, "data": res.data }
        )

parameter_token = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description = "access_token",
    type = openapi.TYPE_STRING
)


### Review ###
# 로그인한 사용자의 리뷰 리스트 반환
class AuthenticatedUserGetList(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['UserReviewListGetSuccess'],
            401: '권한 없음'
        })
    def get(self, request):
        '''
            ## 로그인한 유저가 쓴 리뷰 리스트 조회
        '''
        user = request.user  # 로그인한 사용자 정보 가져오기
        res = get_user_review_list(user)
        return responseFactory(res)


class UserReviewList(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    
    @swagger_auto_schema(
        request_body = ReviewSwaggerSerializer, 
        manual_parameters = [parameter_token],
        responses= {
            201: message['ReviewCreateSuccess'],
            400: 'Bad Request',
            401: '권한 없음'
        })
    @transaction.atomic     # 오류 생기면 롤백
    def post(self, request):
        '''
            ## 리뷰 생성
            - 필수 필드: images, title, content, is_public, progrmRegistNo
            - rid, writer, tag, region 등의 필드는 백엔드에서 자동으로 넣습니다
            (현재 이미지는 Swagger로 못 보냄, Postman으로 테스트 가능)
            - 유저는 봉사 당 하나의 리뷰만 남길 수 있음
            - '내가 한 봉사 목록'에 있는 봉사에만 리뷰를 남길 수 있음
        '''
        res = post_review(request)
        if res.status >= 400:
            transaction.set_rollback(True)
        return responseFactory(res)
    
    
    @swagger_auto_schema(
        responses= {
            200: '리뷰 리스트 조회 성공',
            400: 'Bad Request'
        })
    def get(self, request):
        '''
            ## 리뷰 리스트 조회(신규순으로 정렬)
            - 모든 리뷰 조회하기: `/review/`
            - 특정 봉사에 대한 리뷰 조회: `/review?progrmRegistNo=xxx`
        '''
        progrmRegistNo = request.GET.get('progrmRegistNo')
        if progrmRegistNo is None:
            data = get_all_review_list()
        else:
            data = get_review_list_in_progrm(progrmRegistNo)
        return responseFactory(data)


class UserReviewDetail(GenericAPIView):
    permission_classes = [IsWriterOrReadOnly]
    serializer_class = ReviewSerializer
    
    @swagger_auto_schema(
        responses= {
            200: '리뷰 리스트 조회 성공',
            400: 'Bad Request',
            404: message['ReviewNotFound']
        })
    def get(self, request, rid):
        '''
            ## 특정 리뷰 조회
            - `rid`: 리뷰 ID
        '''
        data = get_one_review(rid)
        return responseFactory(data)
    
    
    @transaction.atomic     # 오류 생기면 롤백
    @swagger_auto_schema(
        request_body = ReviewSwaggerSerializer, 
        manual_parameters = [parameter_token],
        responses= {
            200: message['ReviewPutSuccess'],
            400: 'Bad Request',
            401: '권한 없음',
            404: message['ReviewNotFound']
        })
    def put(self, request, rid):
        '''
            ## 리뷰 수정
            - 필수 필드: images, title, content, is_public, progrmRegistNo
            - rid, writer, tag, region 등의 필드는 백엔드에서 자동으로 넣습니다
            (현재 이미지는 Swagger로 못 보냄, Postman으로 테스트 가능)
        '''
        review = get_object_or_404(Review, rid=rid)
        self.check_object_permissions(self.request, review) # 인가 체크
        res = put_review(request, review)
        
        if res.status >= 400:
            transaction.set_rollback(True)
        return responseFactory(res)


    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            204: message['ReviewDeleteSuccess'],
            401: '권한 없음',
            404: message['ReviewNotFound']
        }
    )
    def delete(self, request, rid):
        '''
            ## 리뷰 삭제
            - `rid`: 리뷰 ID
        '''
        review = get_object_or_404(Review, rid=rid)
        self.check_object_permissions(self.request, review)
        res = delete_review(review)
        return responseFactory(res)



### Comment ###
class CommentList(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        responses= {
            200: message['CommentGetSuccess'],
            404: message['ReviewNotFound']
        }
    )
    def get(self, request, rid):
        '''
            ## 특정 리뷰의 댓글 리스트 조회
            - rid: 리뷰 ID
        '''
        data = get_comment(rid)
        return responseFactory(data)

    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        response = {
            201: message['CommentCreateSuccess'],
            400: 'Bad Request',
            401: '권한 없음',
            404: message['ReviewNotFound']
        }
    )
    def post(self, request, rid):
        '''
            ## 리뷰에 댓글 달기
            - rid: 리뷰 ID
            - request body에는 content만 적으면 됩니다(밑에 writer, review 적혀 있는건 무시)
        '''
        res = save_comment(request, rid, None)
        return responseFactory(res)


class CommentDetail(GenericAPIView):
    permission_classes = [IsWriterOrReadOnly]
    serializer_class = CommentSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        response = {
            200: message['CommentPutSuccess'],
            400: 'Bad Request',
            401: '권한 없음',
            404: message['ReviewNotFound']
        }
    )
    def put(self, request, rid, cid):
        '''
            ## 댓글 수정
            - rid: 리뷰 ID
            - cid: 댓글 ID
            - request body에는 content만 적으면 됩니다(밑에 writer, review 적혀 있는건 무시)
        '''
        comment = get_object_or_404(Comment, cid=cid)
        self.check_object_permissions(self.request, comment)
        res = save_comment(request, rid, comment)
        return responseFactory(res)
    
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        response = {
            204: message['CommentDeleteSuccess'],
            401: '권한 없음',
            404: 'Not Found'
        }
    )
    def delete(self, request, rid, cid):
        '''
            ## 댓글 삭제
            - rid: 리뷰 ID
            - cid: 댓글 ID
        '''
        comment = get_object_or_404(Comment, cid=cid)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return JsonResponse(status=204, data={'msg': message['CommentDeleteSuccess']})


### 리뷰 응원하기 ###
class ReviewCheerGetView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DefaultSwaggerSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        response = {
            200: message['CheeredReviewListGetSuccess'],
            401: '권한 없음',
            404: 'Not Found'
        }
    )
    def get(self, request):
        '''
            ## 로그인한 유저가 응원한 리뷰 리스트 조회
        '''
        cheered_reviews = Cheered_Review.objects.filter(writer=request.user)
        review_id_list = list(cheered_reviews.values_list('review', flat=True))
        res = ResponseDto(status=200, data=review_id_list, msg=message["CheeredReviewListGetSuccess"])
        return responseFactory(res)


class ReviewCheerView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DefaultSwaggerSerializer
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        response = {
            201: message['CheerReviewSuccess'],
            400: 'Bad Request',
            401: '권한 없음',
            404: message['ReviewNotFound']
        }
    )
    def post(self, request, rid):
        '''
            ## (로그인한 유저가) 특정 리뷰를 응원하기
        '''
        user = request.user
        res = cheer_review(user, rid)
        return responseFactory(res)
    
    
    @swagger_auto_schema(
        manual_parameters = [parameter_token],
        response = {
            200: message['CancelCheeringSuccess'],
            400: 'Bad Request',
            401: '권한 없음',
            404: message['ReviewNotFound']
        }
    )
    def delete(self, request, rid):
        '''
            ## (로그인한 유저가) 특정 리뷰 응원 취소하기
        '''
        user = request.user
        res = cancel_cheering_review(user, rid)
        return responseFactory(res)