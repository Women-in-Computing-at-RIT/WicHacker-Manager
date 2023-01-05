from db.db_utils import exec_commit_return_autoincremented_id
from data.email import sendAppliedEmail
import logging

logger = logging.getLogger("Create User")


def createUser(auth0_id, firstName, lastName, email, phoneNumber) -> int:
    """
    Creates a new user and attaches their auth0 id, then sends applied email
    :param phoneNumber:
    :param email:
    :param auth0_id:
    :param firstName:
    :param lastName:
    :return: user id or None if unsuccessful
    """
    sql = "INSERT INTO Users (auth0_id, first_name, last_name, email, phone_number) " \
          "VALUES (%(auth0_id)s, %(firstName)s, %(lastName)s, %(email)s, %(phone_number)s);"
    values = {"auth0_id": auth0_id, "firstName": firstName, "lastName": lastName, "email": email,
              "phone_number": phoneNumber}
    userId = exec_commit_return_autoincremented_id(sql, values)
    if userId is None:
        return None

    emailSuccess = sendAppliedEmail(userId)
    if not emailSuccess:
        # If email fails, log it out but don't cause user registration to fail
        logger.error("Applied Email Not Successful")
    return userId
