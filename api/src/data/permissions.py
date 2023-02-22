import logging

from db.db_utils import exec_get_one

logger = logging.Logger("Permissions")

# Types
READ = "READ"
WRITE = "WRITE"

# Permissions
HACKER_DATA = "Hackers"
PERMISSIONS = "Permissions"
CHECKIN = "CheckIn"
STATISTICS = "Statistics"
MANAGE_CONSOLE = "Console"


def canAccessUserData(auth0Id) -> bool:
    return checkUserPermissionsByAuth0Id(auth0Id, HACKER_DATA, READ)


def canUpdateApplicationStatus(auth0Id) -> bool:
    return checkUserPermissionsByAuth0Id(auth0Id, HACKER_DATA, WRITE)


def canChangeUserPermissions(auth0Id) -> bool:
    return checkUserPermissionsByAuth0Id(auth0Id, PERMISSIONS, WRITE)


def canViewStatistics(auth0Id) -> bool:
    return checkUserPermissionsByAuth0Id(auth0Id, STATISTICS, READ)


def canSendEmails(auth0Id) -> bool:
    # TODO: update to have its own permission at some point
    return checkUserPermissionsByAuth0Id(auth0Id, HACKER_DATA, WRITE)


def checkUserPermissionsByAuth0Id(auth0Id, permission, accessType) -> bool:
    """
    Check if user has a certain permission based on auth0 id
    :param auth0Id: user's auth0 id
    :param permission: string for permission you want to check
    :param accessType: READ or WRITE for permission
    :return:
    """
    sql = 'SELECT p.permission_id FROM Permissions AS p ' \
          'INNER JOIN UserPermissions up on p.permission_id = up.permission_id ' \
          'INNER JOIN Users u on up.user_id = u.user_id ' \
          'WHERE u.auth0_id = %(authId)s AND p.permission = %(permission)s AND p.type = %(type)s'
    args = {"authId": auth0Id, "permission": permission, "type": accessType}

    result, err = exec_get_one(sql, args)
    if err:
        return None
    if len(result) > 0:
        # check if there are keys in result, if there are then user has permission
        return True
    return False
