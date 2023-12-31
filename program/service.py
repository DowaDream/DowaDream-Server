from datetime import datetime
from django.db.models import Count
import json
from pathlib import Path
from django.conf import settings

from .response import *
from .models import *
from .serializers import *
from .dto import ProgramDto
from .search_service import *



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



def get_cheer_recommend():
    interactions = Program_Interaction.objects.filter(cheered=True).annotate(cheer_count=Count('cheered')).order_by('-cheer_count')
    progrmList = list(interactions.values_list('progrmRegistNo', flat=True))
    
    data = []
    for program in progrmList[:4]:
        p_data = callByRegistNo(program)
        program_dto_data = ProgramDto(tagName=p_data['tagName'], title=p_data['title'], registerInstitute=p_data['registerInstitute'], \
                                        recruitStart=p_data['recruitStart'], recruitEnd=p_data['recruitEnd'], actStart=p_data['actStart'], actEnd=p_data['actEnd'])
        data.append(program_dto_data.to_json())
    return ResponseDto(status=200, data=data, msg=message['PrgrmRecommendCheer'])

def get_user_gauge(user):
    # 내가 한 봉사 점수(100점)
    participated_count = Program_Interaction.objects.filter(user=user, participated=True).count()
    # 내가 응원한 봉사 점수(30점)
    cheered_count = Program_Interaction.objects.filter(user=user, cheered=True).count()
    
    my_gauge = participated_count*100 + cheered_count*30
    
    users = User.objects.all()
    best_gauge = 0
    total_gauge = 0
    for user in users:
        participated_count = Program_Interaction.objects.filter(user=user, participated=True).count()
        cheered_count = Program_Interaction.objects.filter(user=user, cheered=True).count()
        current_gauge = participated_count*100 + cheered_count*30
        best_gauge = max(best_gauge, current_gauge)
        total_gauge += current_gauge
    data = {
        "my_gauge": my_gauge,
        "best_gauge": best_gauge,
        "total_gauge": total_gauge
    }
    return ResponseDto(status=200, data=data, msg=message['UserGaugeGetSuccess'])