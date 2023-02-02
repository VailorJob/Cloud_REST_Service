import boto3
from typing import List
from traceback import format_exc

from botocore.exceptions import NoCredentialsError, ClientError


def safe_request(foo):
    def wrapper(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except NoCredentialsError:
            return {"status_code": 401, "message": "AWS Exception. Unauthorised"}
        except ClientError as ex:
            if ex.response['Error']['Code'] == "NoSuchKey":
                return {"status_code": 404, "message": "Not Found"}
            else:
                return {"status_code": 500, "message": f"AWS Client Exception: {format_exc()}"}
        except Exception:
            return {"status_code": 500, "message": f"Server Error: {format_exc()}"}

    return wrapper


class AWSCloud:
    def __init__(self):
        self.s3_resource = None
        self.bucket_for_files = None

    @safe_request
    def login(self, _login: bool) -> None:
        self.s3_resource = boto3.resource('s3')
        self.bucket_for_files = self.s3_resource.Bucket("files-from-the-test-rest-api")
        if "files-from-the-test-rest-api" not in [i.name for i in self.s3_resource.buckets.all()] and not _login:
            self.bucket_for_files.create()
        else:
            self.s3_resource = None
            self.bucket_for_files = None
            boto3.setup_default_session(aws_access_key_id=None,
                                        aws_secret_access_key=None)
        return None

    @safe_request
    def get_files_keys(self) -> List[str]:
        files = [obj.key for obj in self.bucket_for_files.objects.all()]
        return files

    @safe_request
    def get_file(self, _key: str) -> bytes:
        return self.bucket_for_files.Object(_key).get()["Body"].read()

    @safe_request
    def put_file(self, _key: str, body_file: bytes) -> None:
        self.bucket_for_files.put_object(Key=_key, Body=body_file)
        return None

    @safe_request
    def delete_file(self, _key: str) -> None:
        self.bucket_for_files.Object(_key).delete()

    def logout(self):
        self.s3_resource = None
        self.bucket_for_files = None
        boto3.setup_default_session(aws_access_key_id=None,
                                    aws_secret_access_key=None)
