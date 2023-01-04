import boto3

session = boto3.Session()
s3Client = None

S3_RESUME_BUCKET_NAME = "wichacks-resumes"


def initializeAWSClients():
    global s3Client
    try:
        s3Client = session.client('s3')
    except Exception as e:
        return False
    return True


def getS3Client():
    return s3Client

def getS3BucketName():
    return S3_RESUME_BUCKET_NAME
