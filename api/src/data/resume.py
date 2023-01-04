from utils.aws import getS3Client, getS3BucketName
import logging

logger = logging.getLogger("ResumeUpload")
WICHACKS_YEAR = "2023"

def uploadResume(userId, file, contentType) -> bool:
    """
    Upload hacker resume to S3 bucket
    :param userId:
    :param file:
    :param contentType:
    :return:
    """
    s3Client = getS3Client()
    try:
        s3Client.put_object(Body=file,
                            Bucket=getS3BucketName(),
                            Key=WICHACKS_YEAR+'/'+str(userId),
                            ContentType=contentType)
    except Exception as e:
        logger.info(e)
        return False
    return True
