from rest_framework import serializers
from .models import *

# 유효한 이미지 파일인지 검사
def is_image(image):
    image_name = str(image)
    file_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_extension = image_name.split('.')[-1].lower()  # 이미지의 확장자
    
    if file_extension not in file_extensions:
        return False
    return True


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image    # 어떤 모델을 serialize할 것인지
        fields = "__all__"  # 모든 필드를 가져오기
    
    # validate image
    def validate(self, data):
        image = data['image']
        if not is_image(image):
            raise serializers.ValidationError('Not an image file')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
    
    def validate(self, data):
        # 봉사 당 하나의 리뷰만 남길 수 있음
        writer = data.get('writer')
        progrmRegistNo = data.get('progrmRegistNo')
        review = Review.objects.filter(writer=writer, progrmRegistNo=progrmRegistNo)
        if review.exists():
            raise serializers.ValidationError("이미 객체가 존재함")
        
        # 
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CheeredReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheered_Review
        fields = "__all__"


### Swagger를 위한 Serializer
class ReviewSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('rid', 'writer')

class DefaultSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheered_Review
        fields = []