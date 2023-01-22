from utils.aws import getS3Client, getS3BucketName
import logging
from botocore.errorfactory import ClientError

logger = logging.getLogger("Resume")
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
                            Key=WICHACKS_YEAR + '/' + str(userId),
                            ContentType=contentType,
                            ServerSideEncryption='aws:kms')
    except ClientError as e:
        s3ErrorObject = e.response['Error']
        if s3ErrorObject is None:
            # don't know how we get here, adding to prevent accessing None
            logger.error("upload resume unexpected response")
            return False
        if s3ErrorObject['Code'] == "403" or s3ErrorObject['AccessDenied'] == "403":
            logger.error("API Cannot add object to resume S3 bucket")
            return False
        return False
    except Exception as e:
        logger.error("Resume Upload Failure: %s", e)
        return False
    return True


def checkIfUserHasResume(userId) -> bool:
    """
    Return bool if user with userId has a resume already uploaded
    :param userId:
    :return:
    """
    s3Client = getS3Client()
    try:
        s3Client.head_object(Bucket=getS3BucketName(),
                             Key=WICHACKS_YEAR + '/' + str(userId))
    except ClientError as e:
        s3ErrorObject = e.response['Error']
        if s3ErrorObject is None:
            # don't know how we get here, adding to prevent accessing None
            logger.error("head_object for resumes unexpected response")
            return False
        if s3ErrorObject['Code'] == "404":
            # user does not have a resume uploaded
            return False
        if s3ErrorObject['Code'] == "403":
            logger.error("API Cannot access resume S3 bucket")
            return False
    except Exception as e:
        # generic error checking S3 Bucket
        logger.error("Resume Verification Failure: %s", e)
        return False

    # Getting resume metadata didn't error, therefore resume exists
    return True
