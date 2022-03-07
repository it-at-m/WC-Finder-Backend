from controllers.utils import encrypt, decrypt
from db_connection import execute_sql
from flask import make_response, jsonify
import jwt
from datetime import datetime, timedelta

def register_controller(payload, db_conn):
    print('Inside registration')
    try:
        # check if password and confirm password matches
        if payload['password'] != payload['confirm_password']:
            return {
                "success": False,
                "message": "Password and Confirm Password didn't match"
            }
        # check if incoming email already exists
        query = """
            SELECT * FROM users
            WHERE email = '{email}'
        """.format(email=payload['email'])
        data = execute_sql(sql=query, fetchone=True)
        if len(data) != 0:
            return {
                "success": False,
                "message": "Email already exists"
            }

        sql = """
            INSERT INTO users (email, firstname, lastname, password)
            VALUES ('{email}', '{firstname}', '{lastname}', '{password}')
            RETURNING id;
        """.format(
            email = payload['email'],
            firstname = payload['first_name'],
            lastname = payload['last_name'],
            password = encrypt(payload['password']).decode('ascii')
        )
        data = execute_sql(sql=sql, fetchone=True)
        return {
            "success": True,
            "message": "registration successful"
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error in api: " + str(e)
        }


def login_controller(payload, db_conn):
    print('Inside Login')
    try:
        if not payload['password'] or not payload['email']:
            return {
                "success": False,
                "message": "Password or Email missing"
            }
        # get id and password of this user
        sql = """
            SELECT id, email, password 
            FROM users
            WHERE email = '{email}'
        """.format(
            email = payload['email'],
        )
        result = execute_sql(sql=sql, fetchone=True)
        # if there is no row with this email then respond with user does not exist
        if len(result) == 0:
            return {
                "success": False,
                "message": "User does not exist"
            }
        # parse data
        user_id = result[0]
        email = result[1]
        password_db = result[2]

        # compare if password is correct
        password_match = decrypt(password_db.encode('ascii'), payload['password'])
        if not password_match:
            return {
                "success": False,
                "message": "Incorrect Password"
            }
        
        response = make_response(jsonify({
            "success": True,
            "user_id": user_id,
            "message": "Login successful"
        }))
        # set the values in cookie
        encode = jwt.encode({
                'iat': datetime.now(),
                'email': email,
                'user_id': str(user_id),
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, 'SECRET', algorithm='HS256'
        )
        token = str(encode)
        response.set_cookie('auth_token', token)
        return response

    except Exception as e:
        return {
            "success": False,
            "message": "Error in api: " + str(e)
        }
    