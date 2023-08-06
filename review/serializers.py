from rest_framework import serializers
from .models import Review, Image

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