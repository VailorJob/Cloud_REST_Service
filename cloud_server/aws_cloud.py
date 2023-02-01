import boto3

class AWSCloud:
    s3_resource = boto3.resource('s3')
    bucket_for_files = s3_resource.Bucket("files-from-the-test-rest-api")
    if not "files-from-the-test-rest-api" in [i.name for i in s3_resource.buckets.all()]:
        bucket_for_files.create()

    @classmethod    
    def get_files_keys(cls) -> list[str]:
        files = [obj for obj in cls.bucket_for_files.objects.all()]
        return files

    @classmethod
    def get_file(cls, _key: str) -> bytes:
        return cls.bucket_for_files.Object(_key).get()["Body"].read()

    @classmethod
    def put_file(cls, _key: str, body_file: bytes) -> None:
        cls.bucket_for_files.put_object(Key=_key, Body=body_file)

    @classmethod
    def delete_file(cls, _key: str) -> None:
        cls.bucket_for_files.Object(_key).delete()

