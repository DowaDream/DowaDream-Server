from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from .service import *
from .response import *


def responseFactory(res: ResponseDto):
    if res.data is None:
        return JsonResponse(status=res.status, data={ "msg": res.msg })
    else:
        return JsonResponse(
            status=res.status,
            data={ "msg": res.msg, "data": res.data }
        )


class PrgmInteractUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    ### put 메소드: Swagger 주석 꼭 필요함 ###
    # reviewed, participated, cheered 필드 필수 아님!
    def put(self, request):
        request.data['user'] = request.user.id
        res = post_progrm_interact(request.data, request.user)
        return responseFactory(res)
