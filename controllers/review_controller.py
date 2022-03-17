from db_connection import execute_sql

def review_controller(payload, db_conn):
    print('Inside Review')

    query = """
        INSERT INTO review (toiletID, Experience, CleanToilet, LocateToilet, Photo, Accuracy, MoreInfo)
        VALUES ('{toiletID}', '{experience}', '{CleanToilet}', '{LocateToilet}', '{photo}', '{Accuracy}', '{MoreInfo}')
        RETURNING id;
    """.format(
        toiletID = payload['toiletID'],
        Experience = payload['Experience'],
        CleanToilet = payload['CleanToilet'],
        LocateToilet = payload['LocateToilet'],
        Photo = payload['Photo'],
        Accuracy = payload['Accuracy'],
        MoreInfo = payload['MoreInfo'],
    )
    data = execute_sql(sql=query, fetchone=True)
    return {
        "success": True,
        "message": "review added"
    }
