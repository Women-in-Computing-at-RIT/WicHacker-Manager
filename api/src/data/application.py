# @TODO: Consider adding support for update in place

from db.db_utils import exec_commit_link, exec_commit, exec_get_one


def createApplication(auth0_id, major, year, birthday, resumeLink, shirtSize, hasPreviouslyAttended, university) -> int:
    """
    Create application, add application_id to user
    :param auth0_id:
    :param major:
    :param year:
    :param birthday:
    :param resumeLink:
    :param shirtSize:
    :param hasPreviouslyAttended:
    :param university:
    :return: bool True if successful, False if failed, or None if error
    """
    createApplicationSQL = "INSERT INTO Applications (major, year, birthday, resume, shirt_size, has_attended, university) " \
                           "VALUES (%(major)s, %(year)s, %(birthday)s, %(resume)s, %(shirtSize)s, %(hasAttendedWiCHacks)s, %(university)s)"
    applicationArgs = {"major": major, "year": year, "birthday": birthday, "resume": resumeLink,
                       "shirtSize": shirtSize, "hasAttendedWiCHacks": hasPreviouslyAttended, "university": university}

    linkApplicationSQL = "UPDATE Users set application_id = %(added_id)s WHERE auth0_id = %(auth0_id)s"
    linkApplicationArgs = {"auth0_id": auth0_id}

    rowsAffected = exec_commit_link(insertSQL=createApplicationSQL, linkSql=linkApplicationSQL, insertArgs=applicationArgs, linkArgs=linkApplicationArgs)
    if rowsAffected is None:
        return None
    elif rowsAffected == 1:
        # created application and linked to one account - successful
        return True
    return False

def updateApplication(applicationId, major, year, birthday, resumeLink, shirtSize, hasPreviouslyAttended, university):
    """
    Update all values for application id, return number of rows affected
    :param applicationId:
    :param major:
    :param year:
    :param birthday:
    :param resumeLink:
    :param shirtSize:
    :param hasPreviouslyAttended:
    :param university:
    :return:
    """
    createApplicationSQL = "UPDATE Applications " \
                           "SET major = %(major)s, year = %(year)s, birthday = %(birthday)s, resume = %(resume)s, shirt_size = %(shirtSize)s, " \
                           "has_attended = %(hasAttendedWiCHacks)s, university = %(university)s " \
                           "WHERE application_id = %(applicationId)s"
    applicationArgs = {"major": major, "year": year, "birthday": birthday, "resume": resumeLink,
                       "shirtSize": shirtSize, "hasAttendedWiCHacks": hasPreviouslyAttended, "university": university,
                       "applicationId": applicationId}

    return exec_commit(createApplicationSQL, applicationArgs)


def getApplicationSelectSQL():
    """
    Accessor for reuse of Application query
    :return:
    """
    return "SELECT app.major, app.year, app.birthday, app.resume, app.shirt_size, app.has_attended, app.university FROM Applications as app "


def getApplicationByApplicationId(applicationId):
    """
    Retrieve application by application id
    :param applicationId:
    :return: dictionary with application data, None if the query errored, or {} (empty dictionary) if application was not found
    """
    getApplicationSQL = getApplicationSelectSQL() + "WHERE application_id = %(applicationId)s"
    getApplicationArgs = {"applicationId": applicationId}

    applicationData, didError = exec_get_one(getApplicationSQL, getApplicationArgs)

    if didError:
        return None
    elif applicationData is None:
        return {}
    return applicationData


def getApplicationByUserId(userId):
    """
    Wrapper to get application by a user's id
    :param userId:
    :return:
    """
    return getApplicationById(userId=userId)


def getApplicationByAuth0Id(auth0Id):
    """
    Wrapper to get an application by a user's auth0 id
    :param auth0Id:
    :return:
    """
    return getApplicationById(auth0Id=auth0Id)


def getApplicationById(userId=None, auth0Id=None):
    """
    Get applicaiton by userId, auth0 id or both
    :param userId:
    :param auth0Id:
    :return: dictionary with application data, None if the query errored, or {} (empty dictionary) if application was not found
    """
    getApplicationSql = getApplicationSelectSQL()
    getApplicationSql += " INNER JOIN Users as u on u.application_id = app.application_id "

    args = ()
    if auth0Id is not None:
        getApplicationSql += " WHERE u.auth0_id = %s"
        args = args + (auth0Id,)
    if userId is not None:
        getApplicationSql += " WHERE u.user_id = %s"
        args = args + (userId,)

    applicationData, didError = exec_get_one(getApplicationSql, args)
    if didError:
        return None
    elif applicationData is None:
        return {}
    return applicationData
