import os

import db.db_utils as db_utils
import glob
import logging
logger = logging.getLogger("Migrations")

version = None
dirtyVersion = False


def initializeMigrations() -> bool:
    """
    Checks if current version is dirty, returns True if version is clean
    :return:
    """
    global version
    global dirtyVersion
    (version, dirtyVersion) = getCurrentMigration()
    return not dirtyVersion

def getCurrentMigration() -> (str, bool):
    sql = "SELECT version, dirtyVersion FROM Migrations ORDER BY version DESC LIMIT 1;"
    migrationInformation = db_utils.exec_get_one(sql)
    if migrationInformation is None:
        logger.error("Migration Information is None")
        return None, True
    return migrationInformation

def up() -> bool:
    global version
    global dirtyVersion

    for file in glob.glob("**.up.sql"):
        print(file)

    # get current state of migrations
    (version, dirtyVersion) = getCurrentMigration()

    if dirtyVersion:
        return False

    upScripts = []
    for file in glob.glob("src/db/migration/scripts/*.up.sql"):
        upScripts.append(file)
    upScripts.sort()
    logger.info("Upscripts Found: %s", upScripts)
    ifExecutedUpdates = False
    for script in upScripts:
        # Safely Get Version
        versionList = script.split(sep='/')
        if len(versionList) != 5:
            logger.error(
                "Migration File Format or Location Incorrect. Aborting Further Migration, shut down application to avoid conflicts"
                "\nmigrationFile:%s", script)
            return False
        scriptVersion = versionList[4]

        # If newer than current version, execute
        if scriptVersion > version:
            ifExecutedUpdates = True
            logger.info("Executing: %s", script)
            if db_utils.exec_migration(scriptVersion):
                # migration successful
                version = scriptVersion
            else:
                dirtyVersion = True
                return False

    # Migrations Successful
    if ifExecutedUpdates:
        logger.info("Database up migration successful. Currently at version %s", version)
    else:
        logger.info("Database is up to date. Currently at version %s", version)
    return True


def down(rollbackNumber=1) -> bool:
    global version
    global dirtyVersion

    # get current state of migrations
    (version, dirtyVersion) = getCurrentMigration()

    if dirtyVersion:
        return False

    downScripts = []
    for file in glob.glob("db/migration/scripts/*.up.sql"):
        downScripts.append(file)
    downScripts.sort(reverse=True)
    for idx in range(rollbackNumber):
        script = downScripts[idx]
        # Safely Get Version
        versionList = script.split(sep='/')
        if len(versionList) != 4:
            logger.error(
                "Migration File Format or Location Incorrect. Aborting Further Migration, shut down application to avoid conflicts"
                "\nmigrationFile:%s", script)
            return False
        scriptVersion = versionList[3]

        if db_utils.exec_migration(scriptVersion):
            # migration successful
            version = scriptVersion
        else:
            dirtyVersion = True
            return False

    # Migrations Successful
    logger.error(
        "Database down migration successful. Currently at version %s", version)
    return True
