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

    # ===== Bus Riding
    busCountSQL = 'SELECT count(*) as count, bus_stop FROM Applications WHERE bus_rider AND status in (\'ACCEPTED\', \'CONFIRMED\') GROUP BY bus_stop;'
    busInfo = exec_get_all(busCountSQL)
    if busInfo is not None:
        statistics["busStops"] = {}
        for row in busInfo:
            statistics["busStops"][row['bus_stop']] = row['count']
    else:
        statistics["busStops"] = None

    # ===== Dietary Restrictions and Special accommodations
    accomodationsSQL = 'SELECT dietary_restrictions, special_accommodations FROM Applications WHERE (dietary_restrictions IS NOT NULL OR special_accommodations IS NOT NULL) AND status in (\'ACCEPTED\', \'CONFIRMED\');'
    accomodationInfo = exec_get_all(accomodationsSQL)
    if accomodationInfo is not None:
        statistics['dietaryRestrictions'] = []
        statistics['specialAccommodations'] = []
        for row in accomodationInfo:
            if row['dietary_restrictions'] is not None:
                statistics['dietaryRestrictions'].append(row['dietary_restrictions'])
            if row['special_accommodations'] is not None:
                statistics['specialAccommodations'].append(row['special_accommodations'])
    else:
        statistics['dietaryRestrictions'] = None
        statistics['specialAccommodations'] = None

    return statistics
