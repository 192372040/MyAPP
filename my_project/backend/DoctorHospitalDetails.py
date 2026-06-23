from flask import request, jsonify
from db import get_db_connection

def save_hospital_details():

    try:

        data = request.get_json()

        doctor_id = data.get("doctor_id")
        hospital_name = data.get("hospital_name")
        department = data.get("department")
        working_days = data.get("working_days")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        hospital_address = data.get("hospital_address")
        consultation_mode = data.get("consultation_mode")

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO doctor_hospital_details
        (
            doctor_id,
            hospital_name,
            department,
            working_days,
            start_time,
            end_time,
            hospital_address,
            consultation_mode
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            doctor_id,
            hospital_name,
            department,
            ",".join(working_days),
            start_time,
            end_time,
            hospital_address,
            ",".join(consultation_mode)
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Hospital details saved"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })