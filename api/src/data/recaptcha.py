import logging
import os
from utils.aws import getRecaptchaAPIKey

import requests
from json import loads

logger = logging.getLogger("Recaptcha")

CAPTCHA_DOMAIN = "https://www.google.com/recaptcha/api/siteverify"


def getCaptchaResults(captchaToken) -> bool:
    response = requests.post(
        CAPTCHA_DOMAIN,
        data={
            'secret': getCaptchaKey(),
            'response': captchaToken
        }
    )
    if response is not None and response.json().get("success", False):
        return True
    return False


def getCaptchaKey():
    key = getRecaptchaAPIKey()
    if key is None:
        logger.error("RECAPTCHA SECRET Key Retrieval Failure")
    return key
