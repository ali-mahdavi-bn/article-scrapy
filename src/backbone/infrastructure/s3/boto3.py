import boto3
from botocore.exceptions import ClientError

from backbone.configs import config
from backbone.infrastructure.log.logger import LoggerFactory


class S3Exception(Exception):
    pass


class S3Service:
    _client = None
    _resource = None
    logger = LoggerFactory.get_logger("S3Service")

    def __init__(self):
        self.logger = LoggerFactory.get_logger(self.__class__)

    @property
    def base_url(self):
        return config.S3_ENDPOINT + "/" + config.S3_BUCKET

    @classmethod
    def get_resource(cls):
        if cls._resource is None:
            try:
                s3_resource = boto3.resource(
                    's3',
                    endpoint_url=config.S3_ENDPOINT,
                    aws_access_key_id=config.S3_ACCESS_KEY,
                    aws_secret_access_key=config.S3_SECRET_KEY,
                )
                cls._resource = s3_resource
            except S3Exception as e:
                cls.logger.exception(e)

        return cls._resource

    def upload_file_with_path(self, file_path, object_name, bucket_name=config.S3_BUCKET, acl='private'):
        with open(file_path, "rb") as file:
            self.upload_file(file, object_name, bucket_name, acl)

    def upload_file(self, file, object_name, bucket_name=config.S3_BUCKET, acl='public-read'):
        try:
            bucket = self.get_resource().Bucket(bucket_name)
            return bucket.put_object(
                ACL=acl,
                Body=file,
                Key=object_name
            )
        except ClientError as e:
            self.logger.exception(e)

    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                s3_resource = boto3.client(
                    's3',
                    endpoint_url=config.S3_ENDPOINT,
                    aws_access_key_id=config.S3_ACCESS_KEY,
                    aws_secret_access_key=config.S3_SECRET_KEY,
                )
                cls._client = s3_resource
            except S3Exception as e:
                cls.logger.exception(e)

        return cls._client

    def get_list_objects(self, bucket_name=config.S3_BUCKET):
        client = self.get_client()
        buck = client.list_objects_v2(Bucket=bucket_name)
        keys = []
        for obj in buck['Contents']:
            keys.append(obj)
        return keys

    def delete_object(self, object_name, bucket_name=config.S3_BUCKET):
        try:
            client = self.get_client()
            response = client.delete_object(Bucket=bucket_name, Key=object_name)
        except ClientError as e:
            self.logger.exception(e)
        else:
            return response

    def download_obj(self, object_name, bucket_name=config.S3_BUCKET):
        with open(object_name, 'wb') as f:
            client = self.get_client()
            client.download_fileobj(bucket_name, object_name, f)
            return object_name
