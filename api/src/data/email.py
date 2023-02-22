import os

from data.users import getUserByAuthID, getUserByUserID, getUserEmailsWithFilter
from data.emailTemplates.applied import getAppliedEmail, getAppliedSubjectLine
from data.emailTemplates.accepted import getAcceptedEmail, getAcceptedSubjectLine
from data.emailTemplates.rejected import getRejectedEmail, getRejectedSubjectLine
from data.emailTemplates.confirmed import getConfirmedEmail, getConfirmedSubjectLine, getRequestConfirmedEmail, \
    getRequestConfirmedSubjectLine
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Bcc
from typing import Union, List, Tuple
from utils.aws import getSendgridAPIKey

logger = logging.getLogger("email")
WICHACKS_EMAIL = "organizers@wichacks.io"

ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"
CONFIRMED = "CONFIRMED"


def sendPresetEmail(emailName) -> Tuple[List[str], bool]:
    """
    Send preset email
    :param emailName:
    :return:
    """
    if emailName == "requestConfirmation":
        return sendRequestConfirmedEmail()

    # default behavior mimic crash
    return None, False


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
    return sendEmailToSingleRecipient(emailAddress=emailAddress, subject=subjectLine, content=messageContent)


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
    return sendEmailToSingleRecipient(emailAddress=emailAddress, subject=subjectLine, content=messageContent)


def sendRequestConfirmedEmail() -> Tuple[List[str], bool]:
    """
        Wrapper of send email for requesting confirmation email
        :param: applicationStatusFilterList list of application statuses that will receive the email, default is email goes to nobody
        :return: list of failed email addresses
        """
    """
        Wrapper of send email for applied email
        :return: bool success
        """
    userEmails = getUserEmailsWithFilter([ACCEPTED])
    messageContent = getRequestConfirmedEmail()
    subjectLine = getRequestConfirmedSubjectLine()

    return sendGroupEmail(emailAddresses=userEmails, subject=subjectLine, content=messageContent)


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
    return sendEmailToSingleRecipient(emailAddress=emailAddress, subject=subjectLine, content=messageContent)


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
    return sendEmailToSingleRecipient(emailAddress=emailAddress, subject=subjectLine, content=messageContent)


def sendEmailToSingleRecipient(emailAddress: str, subject, content) -> bool:
    """
    Send email with subject line and content to email address
    :param subject: subject line of the email
    :param emailAddress:  single email address to send email to
    :param content: HTML to send
    :return:
    """

    message = Mail(
        from_email=WICHACKS_EMAIL,
        to_emails=emailAddress,
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


def sendGroupEmail(emailAddresses: List[str], subject, content) -> Tuple[List[str], bool]:
    """
    Send email to group of users
    :param subject: subject line of the email
    :param emailAddresses:  single or list of string email addresses to send email to
    :param content: HTML to send
    :return: list of emails that the email failed to send to
    """
    failedEmailList = []
    for email in emailAddresses:
        emailSuccessfullySent = sendEmailToSingleRecipient(emailAddress=email, subject=subject, content=content)
        if not emailSuccessfullySent:
            failedEmailList.append(email)
    emailsSuccessful = True
    if len(failedEmailList) > 0:
        emailsSuccessful = False
        logger.error("Sending Group Email Failed. Email errors for: %s", failedEmailList)
    return failedEmailList, emailsSuccessful


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
