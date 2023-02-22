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
    shirtCountSQL = 'SELECT count(*) as count, shirt_size FROM Applications WHERE status in (\'ACCEPTED\', \'CONFIRMED\') AND NOT is_virtual ' \
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


    # ==== Is Virtual
    irVirtualSQL = 'SELECT count(*) as count, is_virtual FROM Applications WHERE status in (\'ACCEPTED\', \'CONFIRMED\') GROUP BY is_virtual;'
    virtualInfo = exec_get_all(irVirtualSQL)
    if virtualInfo is not None:
        statistics["isVirtual"] = {}
        for row in virtualInfo:
            statistics["isVirtual"][row["is_virtual"]] = row["count"]
    else:
        statistics["isVirtual"] = None

    return statistics


def getHackerAccommodations() -> dict:
    accommodations = []
    accommodationsWrapper = {"accommodations": accommodations}

    # ===== Dietary Restrictions and Special accommodations
    accomodationsSQL = 'SELECT dietary_restrictions, special_accommodations, email, first_name, last_name FROM Applications a INNER JOIN Users u ON a.application_id = u.application_id WHERE (dietary_restrictions IS NOT NULL OR special_accommodations IS NOT NULL) AND status in (\'ACCEPTED\', \'CONFIRMED\');'
    accomodationInfo = exec_get_all(accomodationsSQL)
    if accomodationInfo is not None:
        for row in accomodationInfo:
            accommodations.append({'dietaryRestrictions': row['dietary_restrictions'], 'specialAccommodations': row['special_accommodations'], 'email': row['email'], 'firstName': row['first_name'], 'lastName': row['last_name']})

    return accommodationsWrapper
