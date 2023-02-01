import boto3
from typing import List


class AWSCloud:
    def __init__():
        self.s3_resource = boto3.resource('s3')
        self.bucket_for_files = self.s3_resource.Bucket("files-from-the-test-rest-api")
        if not "files-from-the-test-rest-api" in [i.name for i in self.s3_resource.buckets.all()]:
            self.bucket_for_files.create()
 
    def get_files_keys(self) -> List[str]:
        files = [obj for obj in self.bucket_for_files.objects.all()]
        return files

    @classmethod
    def get_file(self, _key: str) -> bytes:
        return self.bucket_for_files.Object(_key).get()["Body"].read()

    @classmethod
    def put_file(self, _key: str, body_file: bytes) -> None:
        self.bucket_for_files.put_object(Key=_key, Body=body_file)

    @classmethod
    def delete_file(self, _key: str) -> None:
        self.bucket_for_files.Object(_key).delete()

