from flask import request, jsonify
from db import get_db_connection


def doctor_login():

    data = request.json

    doctor_id = data["doctor_id"]
    password = data["password"]

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM doctor_login

    WHERE doctor_id = %s
    AND password = %s
    """

    cursor.execute(
        query,
        (
            doctor_id,
            password,
        )
    )

    doctor = cursor.fetchone()

    cursor.close()
    conn.close()

    if doctor:

        return jsonify({
            "message":
            "Login success"
        })

    else:

        return jsonify({
            "error":
            "Invalid credentials"
        })