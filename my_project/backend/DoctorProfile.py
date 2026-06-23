from flask import request, jsonify
from db import get_db_connection


def get_doctor_profile():

    doctor_id = request.args.get("doctor_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        d.full_name,
        d.doctor_id,
        d.email,
        d.age,
        d.gender,
        d.phone,
        d.dob,
        p.specialization,
        p.qualification,
        p.experience,
        p.license_number,
        p.consultation_fee,
        h.hospital_name,
        h.department,
        h.working_days,
        h.start_time,
        h.end_time,
        h.hospital_address,
        h.consultation_mode

    FROM doctor_details d

    JOIN doctor_professional_details p
        ON d.doctor_id = p.doctor_id

    JOIN doctor_hospital_details h
        ON d.doctor_id = h.doctor_id

    WHERE d.doctor_id = %s
    """

    cursor.execute(query, (doctor_id,))

    doctor = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(doctor)