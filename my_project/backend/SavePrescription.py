from flask import request, jsonify
from db import get_db_connection

def save_prescription():

    data = request.json

    patient_name = data.get("patient_name")
    patient_email = data.get("patient_email")
    doctor_name = data.get("doctor_name")
    diagnosis = data.get("diagnosis")
    medicines = data.get("medicines")
    doctor_notes = data.get("doctor_notes")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prescriptions
        (
            patient_name,
            patient_email,
            doctor_name,
            diagnosis,
            medicines,
            doctor_notes
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        patient_name,
        patient_email,
        doctor_name,
        diagnosis,
        medicines,
        doctor_notes
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Prescription saved"
    })