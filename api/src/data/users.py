from db.db_utils import exec_get_one, exec_commit_return_autoincremented_id

def createUser(auth0_id, firstName, lastName, pronouns, is_virtual) -> bool:
    sql = "INSERT INTO Users (auth0_id, first_name, last_name, pronouns, is_virtual) " \
          "VALUES (%(auth0_id)s, %(firstName)s, %(lastName)s, %(pronouns)s, %(is_virtual)s);"
    values = {"auth0_id": auth0_id, "firstName": firstName, "lastName": lastName, "pronouns": pronouns, "is_virtual": is_virtual}
    return exec_commit_return_autoincremented_id(sql, values)


def getUserByAuthID(auth_id) -> dict:
    return None


def getUserByUserID(user_id) -> dict:
    sql = "SELECT u.user_id, u.auth0_id, u.first_name, u.last_name, u.pronouns, a.address_id, a.address1, a.address2, a.city, a.subdivision, a.country, app.application_id, app.major, app.year, app.birthday, app.resume, app.shirt_id, app.has_attended, u.is_virtual, s.sponsor_id, s.company_name, u.status_id FROM " \
          "Users as u LEFT JOIN Addresses as a ON u.address_id = a.address_id " \
          "LEFT JOIN Applications as app ON u.application_id = app.application_id " \
          "LEFT JOIN Sponsors as s ON u.sponsor_id = s.sponsor_id " \
          "WHERE u.user_id = %s"
    return exec_get_one(sql, (user_id,))
