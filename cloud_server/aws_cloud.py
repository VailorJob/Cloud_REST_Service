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

first_file_name = create_temp_file(300, 'firstfil123e.txt', 'f')

# print(bucket_for_test.Object(f"test/{first_file_name}").upload_file(first_file_name))

# print(bucket_for_test.Object(first_file_name).download_file(f'tmp/{first_file_name}'))

for obj in bucket_for_test.objects.all():
    print(obj.key)



# print(bucket_for_test.Object(first_file_name).delete())

class AWS_cloud:
    boto3.setup_default_session(aws_access_key_id="AKIA4P2WYEPXYKQ6RE54", aws_secret_access_key="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")
    s3_resource = boto3.resource('s3')
    bucket_for_files = s3_resource.Bucket("files-for-flask")

    @classmethod
    def file_list(cls):
        pass

    @classmethod
    def upload_file(cls, first_file_name):
        cls.bucket_for_files.Object(first_file_name).upload_file(first_file_name)

