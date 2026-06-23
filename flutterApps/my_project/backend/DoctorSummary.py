from flask import request, jsonify
from db import get_db_connection

def get_doctor_summary():

    try:

        doctor_id = request.args.get(
            "doctor_id"
        )

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            d.doctor_id,
            d.full_name,
            p.specialization,
            p.license_number,
            p.consultation_fee,
            h.hospital_name,
            h.department,
            h.working_days,
            h.start_time,
            h.end_time,
            h.consultation_mode

        FROM doctor_details d

        JOIN doctor_professional_details p
        ON d.doctor_id = p.doctor_id

        JOIN doctor_hospital_details h
        ON d.doctor_id = h.doctor_id

        WHERE d.doctor_id = %s
        """

        cursor.execute(
            query,
            (doctor_id,)
        )

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })