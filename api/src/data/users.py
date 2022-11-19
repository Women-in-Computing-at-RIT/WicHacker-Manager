from db.db_utils import exec_get_one, exec_commit_return_autoincremented_id, exec_get_all


def createUser(auth0_id, firstName, lastName, pronouns, is_virtual) -> dict:
    """
    Creates a new user and attatches their auth0 id
    :param auth0_id:
    :param firstName:
    :param lastName:
    :param pronouns:
    :param is_virtual:
    :return: user id or None if unsuccessful
    """
    sql = "INSERT INTO Users (auth0_id, first_name, last_name, pronouns, is_virtual) " \
          "VALUES (%(auth0_id)s, %(firstName)s, %(lastName)s, %(pronouns)s, %(is_virtual)s);"
    values = {"auth0_id": auth0_id, "firstName": firstName, "lastName": lastName, "pronouns": pronouns,
              "is_virtual": is_virtual}
    userIdDict = exec_commit_return_autoincremented_id(sql, values)
    if userIdDict is None:
        return None
    return userIdDict


def getUserQuery():
    """
    Accessor for reuse of user query
    :return:
    """
    return "SELECT u.user_id, u.first_name, u.last_name, u.pronouns, a.address_id, a.address1, a.address2, a.city, a.subdivision, a.country, app.application_id, app.major, app.year, app.birthday, app.resume, app.shirt_size, app.has_attended, u.is_virtual, s.sponsor_id, s.company_name, u.status FROM " \
           "Users as u LEFT JOIN Addresses as a ON u.address_id = a.address_id " \
           "LEFT JOIN Applications as app ON u.application_id = app.application_id " \
           "LEFT JOIN Sponsors as s ON u.sponsor_id = s.sponsor_id "


def getUsers(status=None, is_virtual=None) -> list:
    """
    Get a filtered list of all users in json/dictionary format
    :param status: string matching user application status
    :param is_virtual: boolean for if you want all virtual/in person users
    :return: list of dictionaries with user information
    """

    sql = getUserQuery()
    args = ()
    if status is not None:
        sql += "WHERE status = %s"
        args = args + (status,)
        if is_virtual is not None:
            sql += "AND WHERE is_virtual = %s"
            args = args + (is_virtual,)
    elif is_virtual is not None:
        sql += "WHERE is_virtual = %s"
        args = args + (is_virtual,)

    return exec_get_all(sql, args)


def getUserByAuthID(auth_id) -> dict:
    """
    wrapper for getting user using auth0 id
    :param auth_id:
    :return:
    """
    return getUserById(auth_id=auth_id)


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
    if user_id is not None:
        sql += "WHERE u.user_id = %s"
        args = args + (user_id,)

    userData, didError = exec_get_one(sql, args)
    if didError:
        return None
    elif userData is None:
        return {}
    return userData
