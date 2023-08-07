from config import settings
import boto3
from botocore.exceptions import ClientError


# S3에 이미지 저장
def save_image_s3(image, rid):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        file_path = image.name
        s3.upload_fileobj(image, bucket_name, file_path)
        s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{rid}/{file_path}"
        return s3_url
        
    except:
        print("s3 이미지 업로드 불가")
        return None


# s3 이미지 삭제
def delete_image_s3(image_url):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)
        
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        image_key = image_url.split(settings.AWS_S3_CUSTOM_DOMAIN + '/')[1]
        
        # 이미지 존재 여부 확인
        try:
            s3.head_object(Bucket=bucket_name, Key=image_key)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print("이미지가 존재하지 않습니다.")
                return
        
        # 이미지 삭제
        s3.delete_object(Bucket=bucket_name, Key=image_key)
        print("S3 이미지 삭제 성공")
        
    except:
        print("S3 이미지 삭제 실패")