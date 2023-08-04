from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.permissions import IsWriterOrReadOnly
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *
from .response import *
from .service import *


class ReviewList(APIView):
    @transaction.atomic     # 오류 생기면 롤백
    def post(self, request):
        try:
            review_serializer_data = save_review(request)
            if isinstance(review_serializer_data, JsonResponse):
                response = review_serializer_data
                raise Exception()
            response = JsonResponse(ReviewCreateSuccessed(review_serializer_data), status=201)
        except:
            transaction.set_rollback(True)
        finally:
            return response
    
    def get(self, request):
        return


class ReviewDetail(APIView):
    def get(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        serializer = ReviewSerializer(review)
        return JsonResponse(ReviewDetailGetSuccess(serializer.data), status=200)
    
    @transaction.atomic     # 오류 생기면 롤백
    def put(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        try:
            review_serializer_data = put_review(request, review)
            if isinstance(review_serializer_data, JsonResponse):
                response = review_serializer_data
                raise Exception()
            response = JsonResponse(ReviewPutSuccess(review_serializer_data), status=200)
        except:
            transaction.set_rollback(True)
        finally:
            return response

    def delete(self, request, rid):
        review = get_object_or_404(Review, rid=rid)
        review.delete()
        return JsonResponse(ReviewDeleteSuccess(rid), status=204)