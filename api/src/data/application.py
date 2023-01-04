# @TODO: Consider adding support for update in place

from db.db_utils import exec_commit_link, exec_commit, exec_get_one


def createApplication(auth0_id, major, levelOfStudy, birthday, shirtSize, hasAttendedWiCHacks, hasAttendedHackathons,
                      university, gender, busRider, busStop, dietaryRestrictions, specialAccommodations,
                      affirmedAgreements, isVirtual) -> int:
    """
    Create application, add application_id to user
    :param specialAccommodations:
    :param isVirtual:
    :param affirmedAgreements:
    :param dietaryRestrictions:
    :param busStop:
    :param busRider:
    :param hasAttendedWiCHacks:
    :param hasAttendedHackathons:
    :param gender:
    :param auth0_id:
    :param major:
    :param levelOfStudy:
    :param birthday:
    :param shirtSize:
    :param university:
    :return: bool True if successful, False if failed, or None if error
    """
    createApplicationSQL = "INSERT INTO Applications (major, level_of_study, birthday, shirt_size, has_attended_wichacks, has_attended_hackathons, " \
                           "university, gender, bus_rider, bus_stop, dietary_restrictions, special_accommodations, affirmed_agreements, status, is_virtual) " \
                           "VALUES (%(major)s, %(level_of_study)s, %(birthday)s, %(shirtSize)s, %(has_attended_wichacks)s, %(has_attended_hackathons)s, " \
                           "%(university)s, %(gender)s, %(bus_rider)s, %(bus_stop)s, %(dietary_restrictions)s, %(special_accommodations)s, %(affirmed_agreements)s," \
                           "%(status)s, %(is_virtual)s)"
    applicationArgs = {"major": major, "level_of_study": levelOfStudy, "birthday": birthday,
                       "shirtSize": shirtSize, "has_attended_wichacks": hasAttendedWiCHacks,
                       "has_attended_hackathons": hasAttendedHackathons, "university": university,
                       "gender": gender, "bus_rider": busRider, "bus_stop": busStop,
                       "dietary_restrictions": dietaryRestrictions, "special_accommodations": specialAccommodations,
                       "affirmed_agreements": affirmedAgreements, "status": "APPLIED", "is_virtual": isVirtual}

    linkApplicationSQL = "UPDATE Users set application_id = %(added_id)s WHERE auth0_id = %(auth0_id)s"
    linkApplicationArgs = {"auth0_id": auth0_id}

    rowsAffected = exec_commit_link(insertSQL=createApplicationSQL, linkSql=linkApplicationSQL,
                                    insertArgs=applicationArgs, linkArgs=linkApplicationArgs)
    if rowsAffected is None:
        return None
    elif rowsAffected == 1:
        # created application and linked to one account - successful
        return True
    return False


def updateApplication(applicationId, major, levelOfStudy, birthday, shirtSize, hasAttendedWiCHacks,
                      hasAttendedHackathons,
                      university, gender, busRider, busStop, dietaryRestrictions, specialAccommodations,
                      affirmedAgreements, status, isVirtual):
    """
    Update all values for application id, return number of rows affected
    :param status:
    :param affirmedAgreements:
    :param dietaryRestrictions:
    :param busStop:
    :param busRider:
    :param gender:
    :param hasAttendedHackathons:
    :param hasAttendedWiCHacks:
    :param levelOfStudy:
    :param applicationId:
    :param major:
    :param birthday:
    :param shirtSize:
    :param university:
    :return:
    """
    createApplicationSQL = "UPDATE Applications " \
                           " SET major = %(major)s, level_of_study = %(level_of_study)s, birthday = %(birthday)s, shirt_size = %(shirtSize)s, " \
                           " has_attended_wichacks = %(has_attended_wichacks)s, has_attended_hackathons = %(has_attended_hackathons)s, university = %(university)s, " \
                           " status = %(status)s, gender = %(gender)s, bus_rider = %(bus_rider)s, bus_stop = %(bus_stop)s, dietary_restrictions = %(dietary_restrictions)s, " \
                           " special_accommodations = %(special_accommodations)s, affirmed_agreements = %(affirmed_agreements)s, is_virtual = %(is_virtual)s " \
                           " WHERE application_id = %(applicationId)s"
    applicationArgs = {"major": major, "level_of_study": levelOfStudy, "birthday": birthday,
                       "shirtSize": shirtSize, "has_attended_wichacks": hasAttendedWiCHacks,
                       "has_attended_hackathons": hasAttendedHackathons, "university": university,
                       "gender": gender, "bus_rider": busRider, "bus_stop": busStop,
                       "dietary_restrictions": dietaryRestrictions, "special_accommodations": specialAccommodations,
                       "affirmed_agreements": affirmedAgreements, "status": status, "is_virtual":isVirtual, "applicationId": applicationId}

    return exec_commit(createApplicationSQL, applicationArgs)


def getApplicationSelectSQL():
    """
    Accessor for reuse of Application query
    :return:
    """
    return "SELECT app.major, app.level_of_study, app.birthday, app.shirt_size, app.has_attended_wichacks, app.has_attended_hackathons, app.university, app.gender, app.bus_stop, app.bus_rider, app.dietary_restrictions, app.special_accommodations, app.affirmed_agreements, app.status, app.is_virtual FROM Applications as app "


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
