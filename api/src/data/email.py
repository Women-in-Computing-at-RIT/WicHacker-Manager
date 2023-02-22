import os

from data.users import getUserByAuthID, getUserByUserID, getUserEmailsWithFilter
from data.emailTemplates.applied import getAppliedEmail, getAppliedSubjectLine
from data.emailTemplates.accepted import getAcceptedEmail, getAcceptedSubjectLine
from data.emailTemplates.rejected import getRejectedEmail, getRejectedSubjectLine
from data.emailTemplates.confirmed import getConfirmedEmail, getConfirmedSubjectLine, getRequestConfirmedEmail, \
    getRequestConfirmedSubjectLine
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Union, List
from utils.aws import getSendgridAPIKey

logger = logging.getLogger("email")
WICHACKS_EMAIL = "organizers@wichacks.io"

ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"
CONFIRMED = "CONFIRMED"
def sendEmailByStatus(userID, status) -> bool:
    if status == ACCEPTED:
        return sendAcceptedEmail(userID)
    elif status == REJECTED:
        return sendRejectedEmail(userID)
    elif status == CONFIRMED:
        return sendConfirmedEmail(userID)
    else:
        logger.error("Application Status Change, Status not recognized: %s for user %s", status, userID)


def sendAppliedEmail(auth0ID) -> bool:
    """
    Wrapper of send email for applied email
    :param auth0ID:
    :return: bool success
    """
    userData = getUserByAuthID(auth0ID)
    emailAddress = userData.get("email", None)
    firstName = userData.get("first_name", None)
    lastName = userData.get("last_name", None)
    if emailAddress is None or firstName is None or lastName is None:
        logger.error("All User Data Not Found- UserId: %s, Email: %s, FirstName: %s, LastName: %s", auth0ID,
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
    """
        Wrapper of send email for applied email
        :param auth0ID:
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
    messageContent = getConfirmedEmail(firstName, lastName)
    subjectLine = getConfirmedSubjectLine()
    return sendEmail(emailAddresses=emailAddress, subject=subjectLine, content=messageContent)


def sendRequestConfirmedEmail(applicationStatusFilterList: List[str]) -> bool:
    """
        Wrapper of send email for requesting confirmation email
        :param: applicationStatusFilterList list of application statuses that will receive the email, default is email goes to nobody
        :return: bool success
        """
    """
        Wrapper of send email for applied email
        :return: bool success
        """
    userEmails = getUserEmailsWithFilter(applicationStatusFilterList)
    messageContent = getRequestConfirmedEmail()
    subjectLine = getRequestConfirmedSubjectLine()

    return sendEmail(emailAddresses=userEmails, subject=subjectLine, content=messageContent)


def sendAcceptedEmail(userId) -> bool:
    """
        Wrapper of send email for accepted email
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
    messageContent = getAcceptedEmail(firstName, lastName)
    subjectLine = getAcceptedSubjectLine()
    return sendEmail(emailAddresses=emailAddress, subject=subjectLine, content=messageContent)


def sendRejectedEmail(userId) -> bool:
    """
        Wrapper of send email for rejected email
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
    messageContent = getRejectedEmail(firstName, lastName)
    subjectLine = getRejectedSubjectLine()
    return sendEmail(emailAddresses=emailAddress, subject=subjectLine, content=messageContent)


def sendEmail(emailAddresses: Union[List[str], str], subject, content) -> bool:
    """
    Send emailType to user based on id
    :param subject: subject line of the email
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
    except Exception as e:
        logger.error("Send Email Error: %s", e)
        return False
    return True


def getSendGridClient():
    """
    Return Send Grid Api Client
    :return:
    """
    return SendGridAPIClient(getSendGridApiKey())


def getSendGridApiKey():
    key = getSendgridAPIKey()
    if key is None:
        logger.error("SENDGRID API Key Retrieval Failure")
    return key
