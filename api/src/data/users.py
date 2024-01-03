from typing import List

from db.db_utils import exec_get_one, exec_get_all
import logging

logger = logging.getLogger("User Data")


def getUserQuery():
    """
    Accessor for reuse of user query
    :return:
    """
    # Dev note, when updating this query please update the Swagger model in utils/swagger.py UserModel
    return "SELECT u.user_id, u.first_name, u.last_name, u.email, u.phone_number, a.address_id, a.address1, a.address2, a.city, a.subdivision, a.country, " \
           "app.application_id, app.major, app.level_of_study, app.age, app.shirt_size, app.has_attended_wichacks, app.has_attended_hackathons, app.is_virtual, " \
           "s.sponsor_id, s.company_name, app.university, app.status, app.bus_rider, app.bus_stop, app.dietary_restrictions, app.special_accommodations, app.affirmed_agreements, " \
           "app.gender, app.allowMlhEmails FROM " \
           "Users as u LEFT JOIN Addresses as a ON u.address_id = a.address_id " \
           "LEFT JOIN Applications as app ON u.application_id = app.application_id " \
           "LEFT JOIN Sponsors as s ON u.sponsor_id = s.sponsor_id "


def getUsers(applicationStatusFilterList: List[str] = None, is_virtual=None, firstName=None, lastName=None, userId=None,
             email=None, applicationId=None) -> list:
    """
    Get a filtered list of all users in json/dictionary format
    :param applicationId:
    :param email:
    :param userId:
    :param lastName:
    :param firstName:
    :param applicationStatusFilterList: list of statuses to match
    :param is_virtual: boolean for if you want all virtual/in person users
    :return: list of dictionaries with user information, None if error
    """
    sql = getUserQuery()
    firstWhereClause = True
    args = ()

    if applicationStatusFilterList is not None:
        sql += f" WHERE app.status in ({','.join(['%s'] * len(applicationStatusFilterList))}) "
        for status in applicationStatusFilterList:
            args = args + (status,)
    if is_virtual is not None:
        sql += getOptionalAnd(firstWhereClause) + " WHERE app.is_virtual = %s "
        args = args + (is_virtual,)
    if firstName is not None:
        sql += getOptionalAnd(firstWhereClause) + " WHERE u.first_name = %s "
        args = args + (firstName,)
    if lastName is not None:
        sql += getOptionalAnd(firstWhereClause) + " WHERE u.last_name = %s "
        args = args + (lastName,)
    if userId is not None:
        sql += getOptionalAnd(firstWhereClause) + " WHERE u.user_id = %s "
        args = args + (userId,)
    if email is not None:
        sql += getOptionalAnd(firstWhereClause) + " WHERE u.email = %s "
        args = args + (email,)
    if applicationId is not None:
        sql += getOptionalAnd(firstWhereClause) + " WHERE app.application_id = %s "
        args = args + (applicationId,)

    return exec_get_all(sql, args)


def getOptionalAnd(isFirstWhereClause) -> str:
    """
    Helper function, returns "AND " if clause isn't the first and empty string if it is
    :param isFirstWhereClause:
    :return:
    """
    if isFirstWhereClause:
        return ""
    else:
        return " AND "


def getUserByAuthID(auth_id) -> dict:
    """
    wrapper for getting user using auth0 id
    :param auth_id:
    :return:
    """
    return getUserById(auth_id=auth_id)


def getUserIdFromAuthID(auth_id) -> int:
    """
    Get user id from auth0 id
    Wraps getUserById
    :param auth_id:
    :return: user id or None
    """
    return getUserById(auth_id=auth_id).get("user_id", None)


def getEmailFromUserID(userId) -> str:
    """
    Get email from UserID
    Wraps getUserById
    :param userId:
    :return:
    """
    return getUserById(user_id=userId).get("email", None)


def getUserByUserID(user_id) -> dict:
    """
    wrapper for getting user using user id
    :param user_id:
    :return:
    """
    return getUserById(user_id=user_id)


def getUserById(auth_id=None, user_id=None) -> dict:
    """
    Returns user data based on auth0 id, user id or both
    :param auth_id:
    :param user_id:
    :return: dictionary with user data, None if the query errored, or {} (empty dictionary) if user was not found
    """
    sql = getUserQuery()

    args = ()
    if auth_id is not None:
        sql += "WHERE u.auth0_id = %s"
        args = args + (auth_id,)
    elif user_id is not None:
        sql += "WHERE u.user_id = %s"
        args = args + (user_id,)

    userData, didError = exec_get_one(sql, args)
    if didError:
        return None
    elif userData is None:
        return {}
    return userData


def getUserEmailsWithFilter(applicationStatusFilterList: List[str]):
    """
    Gets users' emails from those whose application status is in the filter list
    :param applicationStatusFilterList:
    :return:
    """
    emailSql = getUserQuery() + f" WHERE app.status in ({','.join(['%s'] * len(applicationStatusFilterList))})"
    args = tuple(applicationStatusFilterList)

    users = exec_get_all(emailSql, args)
    emailList = []
    for u in users:
        if len(u['email']) > 1:
            emailList.append(u['email'])
    return emailList
