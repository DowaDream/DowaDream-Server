from .models import *
from .response import *
from .serializers import ImageSerializer
from .s3_manager import *


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


def delete_images_db(rid):
    try:
        review = Review.objects.get(rid=rid)
        images = Image.objects.filter(review=review)
        delete_image_s3(images)
        images.delete()
        return 204
    except Review.DoesNotExist:
        return 404
    except Exception as e:
        print("기존 이미지 삭제 에러 발생:", e)
        return 500  # 삭제 실패 또는 예외 발생