from flask import request, jsonify
from db import get_db_connection

def get_patient_profile():

    try:

        email = request.args.get("email")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        patient = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(patient)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })