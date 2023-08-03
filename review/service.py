from config import settings
import boto3


def save_image(image):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        file_path = image.name
        s3.upload_fileobj(image, bucket_name, file_path)
        s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
        return s3_url
        
    except:
        return Exception("s3 이미지 업로드 실패")