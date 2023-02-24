import logging

from db.db_utils import exec_commit, exec_get_all

logger = logging.getLogger("Discord")

def saveDiscordId(auth0Id, discordId) -> bool:
    """
    Save discord id for user by auth0 ID
    :param auth0Id:
    :param discordId:
    :return:
    """
    saveSQL = "UPDATE Users set Users.discord_id = %(discordId)s WHERE auth0_id = %(auth0Id)s;"
    args = {"discordId": discordId, "auth0Id": auth0Id}

    numberOfRowsAffected = exec_commit(saveSQL, args)
    if numberOfRowsAffected is None:
        return None
    if numberOfRowsAffected != 1:
        logger.error("Discord Update Affected Multiple Hackers: %s", numberOfRowsAffected)
        return False
    return True


def getHackerDataByDiscordId(discordId) -> dict:
    """
    Retrieve data for discord bots based on user's discordId
    :param discordId:
    :return: dictionary with user data or None if error, empty dictionary if no user found
    """
    selectSQL = "SELECT u.first_name, u.last_name, app.status FROM Users u " \
    " INNER JOIN Applications app on u.application_id = app.application_id " \
    "WHERE u.discord_id = %(discordId)s;"
    args = {"discordId": discordId}

    userData = exec_get_all(selectSQL, args)
    if userData is None:
        return None
    elif len(userData) > 1:
        logger.error("Multiple Users Found for Discord ID. DiscordID=%s", discordId)
        return None
    elif len(userData) == 0:
        logger.info("No User found for discord id. DiscordID=%s", discordId)
        return None
    return userData[0]
