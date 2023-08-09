import datetime
from config import settings
import boto3
from botocore.exceptions import ClientError


s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                  region_name=settings.AWS_REGION)

bucket_name = settings.AWS_STORAGE_BUCKET_NAME


# S3에 이미지 저장
def save_image_s3(image, rid):
    try:
        # 현재 시간을 밀리초(ms) 단위로 포맷팅하여 파일 이름에 추가
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        file_path = f"{current_time}_{image.name}"
        
        s3.upload_fileobj(image, bucket_name, file_path)
        s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
        return s3_url
        
    except:
        print("s3 이미지 업로드 불가")
        return None


# s3 이미지 삭제
def delete_image_s3(images_queryset):
    try:
        for image in images_queryset:
            image_path = str(image.image)
            s3_path = image_path.replace(f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/", "")   # 이미지 URL에서 S3 버킷 내의 경로 추출
            s3.delete_object(Bucket=bucket_name, Key=s3_path)  # S3에서 이미지 삭제
    except:
        print("S3 이미지 삭제 실패")