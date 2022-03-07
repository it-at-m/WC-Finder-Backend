import jwt
import json
from flask import jsonify, request, abort
import functools
from db_connection import get_connection, execute_sql
import traceback

def authorize(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print('inside authorize')
        cookie = request.cookies.get('auth_token', None)
        if not cookie:
            return jsonify({
                "message": "Unauthorized Request",
                "success": False
            }), 401
        else:
            try:
                # decode the auth_token
                cookie_cleaned = cookie.split(',')[0]
                auth_data = jwt.decode(cookie_cleaned, 'SECRET', algorithms='HS256')
                print(auth_data)
                
                user_email = auth_data['email']
                user_id = auth_data['user_id']

                # check if user with this email and user_id exists or not
                # postgres connection object
                pg = get_connection()
                query = """
                    SELECT * FROM users
                    WHERE id = {user_id}
                    AND email = '{email}'
                """.format(user_id=user_id, email=user_email)
                # gather result
                result = execute_sql(sql=query, fetchone=True)
                # reject api call if user does not exists
                if len(result) == 0:
                    return jsonify({
                        "message": "Unauthorized Request",
                        "success": False
                    }), 401
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                return jsonify({
                    "message": "Token expired, login again",
                    "success": False
                }), 401
    return decorated_function
