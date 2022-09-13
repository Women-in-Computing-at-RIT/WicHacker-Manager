import db_utils
import glob
import logging

FORMAT = '%(level)s %(asctime)s %(message)s %(err)s %(migrationFile)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Migrations")

version = None
dirtyVersion = False


def initializeMigrations() -> bool:
    global version
    global dirtyVersion
    sql = "SELECT version, dirtyVersion FROM migrations WHERE migration_id=1;"
    (version, dirtyVersion) = db_utils.exec_get_one(sql)
    return dirtyVersion


def up() -> bool:
    global version
    global dirtyVersion
    upScripts = []
    for file in glob.glob("scripts/*.up.sql"):
        upScripts.append(file)
    upScripts.sort()
    for script in upScripts:
        # Safely Get Version
        versionList = script.split()
        if len(versionList) != 2:
            logInfo = {"level": "CRITICAL", "err": None, "migrationFile": script}
            logger.error(
                "Migration File Format Incorrect. Aborting Further Migration, shut down application to avoid conflicts",
                extra=logInfo)
            return False
        scriptVersion = versionList[1]

        # If newer than current version, execute
        if scriptVersion > version:
            if db_utils.exec_migration(script):
                # migration successful
                version = scriptVersion
            else:
                dirtyVersion = True
                return False

    # Migrations Successful
    logInfo = {"level": "INFO", "err": None, "migrationFile": None}
    logger.error(
        "Database up migration successful. Currently at version %s", version, extra=logInfo)
    return True


def down(rollbackNumber=1) -> bool:
    global version
    global dirtyVersion
    downScripts = []
    for file in glob.glob("scripts/*.down.sql"):
        downScripts.append(file)
    downScripts.sort(reverse=True)
    for idx in range(rollbackNumber):
        script = downScripts[idx]
        # Safely Get Version
        versionList = script.split()
        if len(versionList) != 2:
            logInfo = {"level": "CRITICAL", "err": None, "migrationFile": script}
            logger.error(
                "Migration File Format Incorrect. Aborting Further Migration, shut down application to avoid conflicts",
                extra=logInfo)
            return False
        scriptVersion = versionList[1]

        if db_utils.exec_migration(script):
            # migration successful
            version = scriptVersion
        else:
            dirtyVersion = True
            return False

    # Migrations Successful
    logInfo = {"level": "INFO", "err": None, "migrationFile": None}
    logger.error(
        "Database down migration successful. Currently at version %s", version, extra=logInfo)
    return True
