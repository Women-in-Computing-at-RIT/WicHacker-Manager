import logging
import os

import boto3

session = boto3.Session()
s3Client = None
ssmClient = None

environment = None

S3_RESUME_BUCKET_NAME = "wichacks-rit-resumes"
logger = logging.getLogger("aws")


def initializeAWSClients():
    global s3Client, ssmClient, environment
    try:
        s3Client = session.client('s3')
        ssmClient = session.client('ssm')
        environment = os.environ.get("ENV", None)
    except Exception as e:
        logger.error("AWS Client Creation Failure: %s", str(e))
        return False
    return True


def getS3Client():
    return s3Client


def getS3BucketName():
    return S3_RESUME_BUCKET_NAME


def getDatabaseSecrets() -> dict:
    """
    Returns database secrets as dict
    :return:
    """
    dbSecretsResponse = None
    try:
        dbSecretsResponse = ssmClient.get_parameters_by_path(
            Path='/' + environment + '/DB',
            WithDecryption=True
        )
    except Exception as e:
        logger.error("SSM Parameter Retrieval Failure: %s", str(e))
        return None
    dbSecrets = {}
    for parameter in dbSecretsResponse['Parameters']:
        # param comes back as /DEV|PROD/DB/name
        dbSecrets[parameter['Name'].split('/')[3]] = parameter['Value']
    return dbSecrets


def getRecaptchaAPIKey() -> str:
    return getSSMSecureParameter('RECAPTCHA_SECRET_KEY')


def getSendgridAPIKey() -> str:
    return getSSMSecureParameter('SENDGRID_API_KEY')


def getAuth0ClientID() -> str:
    return getSSMSecureParameter('AUTH0_CLIENT_ID')


def getDiscordClientID() -> str:
    return getSSMSecureParameter('DISCORD_CLIENT_ID')


def getDiscordClientSecret() -> str:
    return getSSMSecureParameter('DISCORD_CLIENT_SECRET')


def getRedirectDomain() -> str:
    return getSSMSecureParameter(f'/{environment}/REDIRECT_URL')


def getSSMSecureParameter(parameterName) -> str:
    ssmResponse = None
    try:
        ssmResponse = ssmClient.get_parameter(
            Name=parameterName,
            WithDecryption=True
        )
    except Exception as e:
        logger.error("SSM Parameter Retrieval Failure for Parameter %s: %s", parameterName, str(e))
        return None
    return ssmResponse['Parameter']['Value']
