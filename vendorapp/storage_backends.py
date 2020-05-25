from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    bucket_name = 'django-career-files-resized'
    custom_domain = '{}.s3.amazonaws.com'.format(bucket_name)
    file_overwrite = False


class StaticStorage(S3Boto3Storage):
    bucket_name = 'django-career-files-resized'
    location = 'static'