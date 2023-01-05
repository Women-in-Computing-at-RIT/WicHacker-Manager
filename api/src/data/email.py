from enum import Enum
from users import getUserByUserID
from emailTemplates.applied import getAppliedEmail, getAppliedSubjectLine
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Union, List

logger = logging.getLogger("email")
WICHACKS_EMAIL = "organizers@wichacks.io"


def sendAppliedEmail(userId) -> bool:
    """
    Wrapper of send email for applied email
    :param userId:
    :return: bool success
    """
    userData = getUserByUserID(userId)
    emailAddress = userData.get("email", None)
    firstName = userData.get("first_name", None)
    lastName = userData.get("last_name", None)
    if emailAddress is None or firstName is None or lastName is None:
        logger.error("All User Data Not Found- UserId: %s, Email: %s, FirstName: %s, LastName: %s", userId,
                     emailAddress, firstName, lastName)
        return False
    messageContent = getAppliedEmail(firstName, lastName)
    subjectLine = getAppliedSubjectLine()
    return sendEmail(emailAddresses=emailAddress, subject=subjectLine, content=messageContent)


def sendConfirmedEmail(userId) -> bool:
    """
        Wrapper of send email for confirmed email
        :param userId:
        :return: bool success
        """
    return False


def sendAcceptedEmail(userId) -> bool:
    """
        Wrapper of send email for accepted email
        :param userId:
        :return: bool success
        """
    return False


def sendRejectedEmail(userId) -> bool:
    """
        Wrapper of send email for rejected email
        :param userId:
        :return: bool success
        """
    return False


def sendEmail(emailAddresses: Union[List[str], str], subject, content) -> bool:
    """
    Send emailType to user based on id
    :param emailAddresses:  single or list of string email addresses to send email to
    :param content: HTML to send
    :return:
    """

    message = Mail(
        from_email=WICHACKS_EMAIL,
        to_emails=emailAddresses,
        subject=subject,
        html_content=content
    )

    client = getSendGridClient()
    try:
        response = client.send(message)
        logger.info("Email Sent - Response status: %s, body: %s", str(response.status_code), response.body)
    except Exception as e:
        logger.error("Send Email Error: %s", e)
        return False
    return True


def getSendGridClient():
    """
    Return Send Grid Api Client
    :return:
    """
    return SendGridAPIClient('SendGridApiKey')
