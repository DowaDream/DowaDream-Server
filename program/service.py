import requests
from django.conf import settings
from django.http import JsonResponse
from user.models import User

from .response import *
from .models import *
from .serializers import *


def update_progrm_interact(data, user) -> ResponseDto:
    progrmRegistNo = data.get('progrmRegistNo')
    
    try:
        interact = Program_Interaction.objects.get(progrmRegistNo=progrmRegistNo, user=user)
    
    except Program_Interaction.DoesNotExist:
        # 해당하는 progrmRegistNo가 없으면 새로운 튜플 생성
        interact = Program_Interaction(progrmRegistNo=progrmRegistNo, user=user)
    
    # request body에서 해당 필드의 값을 가져오고, 필드 값이 없으면 기존값을 넣음
    cheered = data.get('cheered', interact.cheered)
    participated = data.get('participated', interact.participated)
    clipped = data.get('clipped', interact.clipped)
    
    # 필드 값 설정
    interact.cheered = cheered
    interact.participated = participated
    interact.clipped = clipped
    interact.user = user
    
    serializer = PrgmInteractSerializer(interact, data=data)
    if serializer.is_valid():
        serializer.save()
        return ResponseDto(status=200, data=serializer.data, msg=message['PrgmInteractSuccess'])
    
    return ResponseDto(status=400, data=serializer.errors, msg=message['PrgmInteractFail'])


def get_interactions_list(user, field_name):
    interactions = Program_Interaction.objects.filter(user=user, **{field_name: True})
    interations_list = list(interactions.values_list('progrmRegistNo', flat=True))  # flat=False: value 하나를 list로 저장
    return interations_list