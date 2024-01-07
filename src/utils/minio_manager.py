from minio import Minio
from minio.error import S3Error


class MinioBucketManager:
    def __init__(self, endpoint, access_key, secret_key):
        self.minio_client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)

    def is_valid_bucket_name(self, bucket_name):
        if not (3 <= len(bucket_name) <= 63) or not bucket_name.islower() or not bucket_name.isalnum():
            return False
        return True

    def create_bucket(self, bucket_name):
        if not self.is_valid_bucket_name(bucket_name):
            raise ValueError(f'Invalid bucket name: {bucket_name}. Please follow MinIO naming conventions.')

        try:
            self.minio_client.make_bucket(bucket_name)

            print(f"Bucket '{bucket_name}' created successfully.")

        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def upload_file(self, bucket_name, object_name, file_path):
        try:
            self.minio_client.fput_object(bucket_name, object_name, file_path)
            print(f"File {object_name} uploaded successfully to {bucket_name}")
            file_url = self.minio_client.presigned_get_object(bucket_name, object_name)
            return file_url
        except S3Error as e:
            print(f"Error uploading file: {e}")

    def get_file(self, bucket_name, object_name):
        file_url = self.minio_client.presigned_get_object(bucket_name, object_name)
        return file_url


# Replace these values with your MinIO server information
minio_endpoint = 'localhost:9000'
access_key = 'raBUZpe7KpGWPUUU0t6e'
secret_key = '8xT3vutJZXSlrTeqjSYepztXRZLfOnPnmJ4Owx2L'

minio_manager = MinioBucketManager(minio_endpoint, access_key, secret_key)
