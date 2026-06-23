from flask import request, jsonify
from db import get_db_connection

def save_professional_details():
    try:
        data = request.get_json()

        doctor_id = data.get("doctor_id")
        qualification = data.get("qualification")
        specialization = data.get("specialization")
        experience = data.get("experience")
        license_number = data.get("license_number")
        consultation_fee = data.get("consultation_fee")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # GET DOCTOR NAME
        cursor.execute(
            """
            SELECT full_name
            FROM doctor_details
            WHERE doctor_id = %s
            """,
            (doctor_id,)
        )

        doctor = cursor.fetchone()
        if doctor is None:
            cursor.close()
            conn.close()
            return jsonify({"error": "Doctor not found"}), 404

        full_name = doctor["full_name"]

        # VERIFY DOCTOR
        # VERIFY DOCTOR
        cursor.execute(
    """
    SELECT *
    FROM verified_doctors

    WHERE license_number = %s
    """,

    (license_number,)
)
        verified_doctor = cursor.fetchone()
        if not verified_doctor:
            cursor.close()
            conn.close()
            return jsonify({"error": "Doctor not verified"}), 400

        # CHECK DUPLICATE LICENSE
        cursor.execute(
            """
            SELECT *
            FROM doctor_professional_details
            WHERE license_number = %s
            """,
            (license_number,)
        )

        existing_license = cursor.fetchone()
        if existing_license:
            cursor.close()
            conn.close()
            return jsonify({"error": "License already registered"}), 400

        query = """
        INSERT INTO doctor_professional_details
        (
            doctor_id,
            qualification,
            specialization,
            experience,
            license_number,
            consultation_fee
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            doctor_id,
            qualification,
            specialization,
            experience,
            license_number,
            consultation_fee,
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Professional details saved"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
