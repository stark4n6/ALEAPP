__artifacts_v2__ = {
    "cff_searched_places": {
        "name": "SBB Mobile - Searched places",
        "description": "",
        "author": "jerome.arn@vd.ch",
        "creation_date": "2026-03-26",
        "last_update_date": "2026-03-26",
        "requirements": "none",
        "category": "Travel",
        "notes": "",
        "paths": ('*/data/ch.sbb.*/databases/SbbMobile.db'),
        "output_types": "standard",
        "html_columns": ['location of places (link)'],
        "artifact_icon": "search"
    },
    "cff_search_history": {
        "name": "SBB Mobile - Search History",
        "description": "",
        "author": "jerome.arn@vd.ch",
        "creation_date": "2026-03-26",
        "last_update_date": "2026-03-26",
        "requirements": "none",
        "category": "Travel",
        "notes": "",
        "paths": ('*/data/ch.sbb.*/databases/SbbMobile.db'),
        "output_types": "standard",
        "html_columns": ['location of search (link)'],
        "artifact_icon": "search"
    },
    "cff_travel_cards": {
        "name": "SBB Mobile - Travel Cards",
        "description": "",
        "author": "jerome.arn@vd.ch",
        "creation_date": "2026-03-26",
        "last_update_date": "2026-03-26",
        "requirements": "none",
        "category": "Travel",
        "notes": "",
        "paths": ('*/data/ch.sbb.*/databases/SbbMobile.db'),
        "output_types": "standard",
        "artifact_icon": "user"
    },
        "cff_purchased_tickets": {
        "name": "SBB Mobile - Ticket Purchased recently",
        "description": "",
        "author": "jerome.arn@vd.ch",
        "creation_date": "2026-03-26",
        "last_update_date": "2026-03-26",
        "requirements": "none",
        "category": "Travel",
        "notes": "",
        "paths": ('*/data/ch.sbb.*/databases/SbbMobile.db'),
        "output_types": "standard",
        "artifact_icon": "star"
    }
}

from scripts.ilapfuncs import artifact_processor, get_file_path, \
    get_sqlite_db_records, logfunc, open_sqlite_db_readonly

@artifact_processor
def cff_purchased_tickets(files_found, _report_folder, _seeker, _wrap_text):
    source_path = get_file_path(files_found, "SbbMobile.db")
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)

    if files_found[0].endswith('SbbMobile.db'):
        query = '''
            SELECT
                traveler,
                validFrom,
                validUntil,
                CASE 
                    WHEN refundState == "NORMAL" THEN "Not Refunded"
                    WHEN refundState == "COMPLETE" THEN "Refunded"
                    ELSE refundState
                END AS refundState,
                paymentMethodType,
                displayInfo_ticketType,
                displayInfo_titleLine_firstSegment,
                displayInfo_titleLine_lastSegment
            FROM
                PurchasedTickets
        '''

        data_headers = ('Traveler', "Valid from", "Valid until", "is Refunded", "Payment method", "Ticket description", "Ticket departure", "Ticket destination")
        db_records = get_sqlite_db_records(files_found[0], query)

        for record in db_records:
            data_list.append(record)
        return data_headers, data_list, source_path
    else:
        logfunc('No Data')

@artifact_processor
def cff_searched_places(files_found, _report_folder, _seeker, _wrap_text):
    source_path = get_file_path(files_found, "SbbMobile.db")
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)

    if files_found[0].endswith('SbbMobile.db'):
        query = '''
            SELECT
                datetime(timestamp/1000, 'unixepoch', 'localtime'),
                title,
                CASE 
                    WHEN favorite THEN "True"
                    ELSE "False"
                END AS favorite,
                CASE 
                    WHEN type == "a" THEN "Address"
                    WHEN type == "p" THEN "POI"
                    WHEN type == "c" THEN "Coordinate"
                    WHEN type == "s" THEN "Station"
                    ELSE type
                END AS type,
                latitude,
                longitude
            FROM 
                SearchedPlaces
        '''

        data_headers = ('Searched timestamp', "Title", "Is favorite", "Type", "location of places (link)")
        db_records = get_sqlite_db_records(files_found[0], query)

        for record in db_records:
            tmp = coordinate_to_osm(record[4], record[5])
            data_list.append((record[0], record[1], record[2], record[3], tmp))
        return data_headers, data_list, source_path
    else:
        logfunc('No Data')

@artifact_processor
def cff_search_history(files_found, _report_folder, _seeker, _wrap_text):
    source_path = get_file_path(files_found, "SbbMobile.db")
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)

    if files_found[0].endswith('SbbMobile.db'):
        query = '''
                SELECT
                datetime(timestamp/1000, 'unixepoch', 'localtime'),
                departure,
				target,
                CASE 
                    WHEN departureType == "a" THEN "Address"
                    WHEN departureType == "p" THEN "POI"
                    WHEN departureType == "c" THEN "Coordinate"
                    WHEN departureType == "s" THEN "Station"
                    ELSE departureType
                END AS departureType,
				CASE 
                    WHEN targetType == "a" THEN "Address"
                    WHEN targetType == "p" THEN "POI"
                    WHEN targetType == "c" THEN "Coordinate"
                    WHEN targetType == "s" THEN "Station"
                    ELSE targetType
                END AS targetType,
                latitude,
                longitude
            FROM 
                SearchHistory
        '''

        data_headers = ('Search timestamp', "Departure", "Departure (type)", "Destination", "Destination (type)", "location of search (link)")
        db_records = get_sqlite_db_records(files_found[0], query)

        for record in db_records:
            if record[5] and record[6]:
                tmp = coordinate_to_osm(record[5], record[6])
                data_list.append((record[0], record[1], record[2], record[3], record[4], tmp))
            else:
                data_list.append((record[0], record[1], record[2], record[3], record[4], ""))
        return data_headers, data_list, source_path
    else:
        logfunc('No Data')

@artifact_processor
def cff_travel_cards(files_found, _report_folder, _seeker, _wrap_text):
    source_path = get_file_path(files_found, "SbbMobile.db")
    data_list = []

    for file_found in files_found:
        file_found = str(file_found)

    if files_found[0].endswith('SbbMobile.db'):
        query = '''
            SELECT
                name,
                type,
                contract_id,
                valid_from,
                valid_to,
                contract_state
            FROM
                SwissPassTravelCards
        '''

        data_headers = ('Name', "Type", "Contract ID", "Valid From", "Valid To", "Contract state")
        db_records = get_sqlite_db_records(files_found[0], query)

        for record in db_records:
            data_list.append((record[0], record[1], record[2], record[3], record[4], record[5]))
        return data_headers, data_list, source_path
    else:
        logfunc('No Data')

def coordinate_to_osm(lat, lon): 
    return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15"
