from minio import Minio
from minio.error import S3Error

from backbone.configs import config


class MinioBucketManager:
    def __init__(self, minio_driver):
        self.minio_client = minio_driver
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
            self.create_bucket("articles")
            self.minio_client.fput_object(bucket_name, object_name, file_path)
            print(f"File {object_name} uploaded successfully to {bucket_name}")
            file_url = self.minio_client.presigned_get_object(bucket_name, object_name)
            return file_url
        except S3Error as e:
            print(f"Error uploading file: {e}")

    def get_file(self, bucket_name, object_name):
        file_url = self.minio_client.presigned_get_object(bucket_name, object_name)
        return file_url


minio_endpoint = config.MINIO_HOST + ":" + config.MINIO_PORT
access_key = config.MINIO_ACCESS_KEY
secret_key = config.MINIO_SECRET_KEY
minio_driver = Minio(minio_endpoint, access_key=access_key, secret_key=secret_key, secure=False)

minio_manager = MinioBucketManager(minio_driver)