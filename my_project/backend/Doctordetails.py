from flask import request, jsonify
from db import get_db_connection

def save_doctor_details():

    try:

        data = request.get_json()

        email = data.get("email")
        full_name = data.get("full_name")
        age = data.get("age")
        gender = data.get("gender")
        phone = data.get("phone")
        dob = data.get("dob")

        conn = get_db_connection()
        cursor = conn.cursor()
# Generate unique doctor ID

        cursor.execute(
             "SELECT COUNT(*) FROM doctor_details"
               )

        count = cursor.fetchone()[0] + 1

        doctor_id = (
         f"MED-DOC-2026-{count:05d}"
                  )
        query = """
        INSERT INTO doctor_details
        (
        doctor_id,
            email,
            full_name,
            age,
            gender,
            phone,
            dob
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            doctor_id,
            email,
            full_name,
            age,
            gender,
            phone,
            dob
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Doctor details saved",
            "doctor_id":
        doctor_id
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })