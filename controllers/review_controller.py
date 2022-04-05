from db_connection import execute_sql

def review_controller(payload, db_conn):
    print('Inside Review')

    query = """
        INSERT INTO review (toiletName, Experience, CleanToilet, LocateToilet, Photo, Accuracy, MoreInfo, accuracydetails)
        VALUES ('{toiletName}', '{Experience}', '{CleanToilet}', '{LocateToilet}', '{Photo}', '{Accuracy}', '{MoreInfo}', ARRAY {accuracydetail})
        RETURNING id;
    """.format(
        toiletName = payload['toiletName'],
        Experience = payload['Experience'],
        CleanToilet = payload['CleanToilet'],
        LocateToilet = payload['LocateToilet'],
        Photo = payload['Photo'],
        Accuracy = payload['Accuracy'],
        MoreInfo = payload['MoreInfo'],
        accuracydetail=payload['accuracydetail']
    )
    data = execute_sql(sql=query, fetchone=True)
    return {
        "success": True,
        "message": "review added"
    }
