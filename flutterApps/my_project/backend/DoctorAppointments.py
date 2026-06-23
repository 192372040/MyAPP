from flask import request, jsonify
from db import get_db_connection

def get_doctor_appointments():

    try:

        doctor_name = request.args.get(
            "doctor_name"
        )
        print("DOCTOR NAME =", doctor_name)
        conn = get_db_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM appointments
            WHERE doctor_name = %s
            ORDER BY appointment_date
            """,
            (doctor_name,)
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })