import logging
import os

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
    key = os.environ.get("RECAPTCHA_SECRET_KEY")
    if key is None:
        logger.error("RECAPTCHA SECRET Key Retrieval Failure")
    return key
