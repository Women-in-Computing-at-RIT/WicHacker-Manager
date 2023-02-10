from db.db_utils import exec_get_all


def getHackerStatistics() -> dict:
    statistics = {}

    # ======= Application counts by status =============
    hackerCountSQL = 'SELECT count(*) as count, status FROM Applications GROUP BY status'
    hackerCount = exec_get_all(hackerCountSQL)
    if hackerCount is not None:
        statistics["applications"] = {}
        for row in hackerCount:
            statistics["applications"][row['status']] = row['count']
    else:
        statistics["applications"] = None

    # ===== Accepted and Confirmed Hackers by School ========
    schoolCountSQL = 'SELECT count(*) as count, university FROM Applications WHERE status in (\'ACCEPTED\', \'CONFIRMED\')  ' \
                     'GROUP BY university ORDER BY count DESC;'
    schools = exec_get_all(schoolCountSQL)
    if schools is not None:
        statistics["schools"] = {}
        for row in schools:
            statistics["schools"][row['university']] = row['count']
        statistics["schoolCount"] = len(schools)
    else:
        statistics["schools"] = None

    # ===== T Shirt Sizes
    shirtCountSQL = 'SELECT count(*) as count, shirt_size FROM Applications WHERE status in (\'ACCEPTED\', \'CONFIRMED\')  ' \
                     'GROUP BY shirt_size ORDER BY count DESC;'
    shirts = exec_get_all(shirtCountSQL)
    if shirts is not None:
        statistics["shirts"] = {}
        for row in shirts:
            statistics["shirts"][row['shirt_size']] = row['count']
    else:
        statistics["shirts"] = None

    return statistics
