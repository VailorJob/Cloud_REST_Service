import boto3
    
boto3.setup_default_session(aws_access_key_id="AKIA4P2WYEPXYKQ6RE54", aws_secret_access_key="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")

s3_resource = boto3.resource('s3')

bucket_for_test = s3_resource.Bucket("bucket-for-test-flask")

print(bucket_for_test)

def create_temp_file(size, file_name, file_content):
    random_file_name = file_name
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name

first_file_name = create_temp_file(300, 'secondfile.txt', 'f')

with open(first_file_name, "rb") as binary:
    data = binary.read()

print(bucket_for_test.put_object(Key=f"{first_file_name}", Body=data))
print(s3_resource.Object("bucket-for-test-flask", f"{first_file_name}").delete())

# print(bucket_for_test.Object(f"{first_file_name}").download_file(f'tmp/{first_file_name}'))

for obj in bucket_for_test.objects.all():
    print(obj.key)

# For list files with filter
# client = boto3.client("s3")
# objects = client.list_objects_v2(Bucket='bucket-for-test-flask')
# for obj in objects['Contents']:
#     if obj['Size'] > 0 and obj['Key'].count('/') == 0:
#         print(obj['Key'])



# print(bucket_for_test.Object(first_file_name).delete())

class AWSCloud:
    boto3.setup_default_session(aws_access_key_id="AKIA4P2WYEPXYKQ6RE54", aws_secret_access_key="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")
    s3_resource = boto3.resource('s3')
    bucket_for_files = s3_resource.Bucket("files-for-flask")

    @classmethod
    def get_files_keys(cls) -> list[str]:
        files = [obj for obj in bucket_for_files.objects.all()]
        return files

    @classmethod
    def get_file(cls, _key) -> bytes:
        cls.bucket_for_files.put_object(Key=_key, Body=body_file)

    @classmethod
    def put_file(cls, _key, body_file) -> None:
        cls.bucket_for_files.put_object(Key=_key, Body=body_file)

    @classmethod
    def delete_file(cls, _key) -> None:
        cls.bucket_for_files.delete(Key=_key)

