"""
load_test_server.py
-------------------
Starts the Medicate Flask app with all database calls mocked out,
so the load test can run without a live MySQL instance.

Usage (from backend/ directory):
    python load_tests/load_test_server.py
"""

import sys
import os
import io
from unittest.mock import patch, MagicMock

# ── ensure 'backend/' is on the path ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── patch every DB / external call before importing app ──────────────
patches = [
    patch('app.models.database.init_db'),
    # Hospital (admin)
    patch('app.models.hospital.Hospital.create',           return_value='HOSP001'),
    patch('app.models.hospital.Hospital.find_by_email',    return_value=None),
    patch('app.models.hospital.Hospital.find_by_id',       return_value={
        'id': 'HOSP001', 'name': 'City General Hospital', 'password_hash': 'hash'
    }),
    patch('app.models.hospital.Hospital.verify_password',  return_value=True),
    patch('app.models.hospital.Hospital.get_all',          return_value=[
        {'id': 'HOSP001', 'name': 'City General Hospital', 'location': 'Test City'}
    ]),
    # Doctor
    patch('app.models.doctor.Doctor.create',               return_value='DOC001'),
    patch('app.models.doctor.Doctor.find_by_email',        return_value=None),
    patch('app.models.doctor.Doctor.find_by_id',           return_value={
        'id': 'DOC001', 'name': 'Dr. Sarah Connor', 'password_hash': 'hash',
        'specialization': 'General Medicine'
    }),
    patch('app.models.doctor.Doctor.verify_password',      return_value=True),
    patch('app.models.doctor.Doctor.add_availability_slot',return_value=True),
    patch('app.models.doctor.Doctor.add_to_hospital',      return_value=True),
    patch('app.models.doctor.Doctor.get_by_hospital',      return_value=[
        {'id': 'DOC001', 'name': 'Dr. Sarah Connor', 'specialization': 'General Medicine'}
    ]),
    patch('app.models.doctor.Doctor.get_all_slots',        return_value=[
        {'id': 1, 'slot_date': '2026-08-01', 'slot_time': '10:00:00', 'is_booked': False}
    ]),
    patch('app.models.doctor.Doctor.get_available_slots',  return_value=[
        {'id': 1, 'slot_date': '2026-08-01', 'slot_time': '10:00:00', 'is_booked': False}
    ]),
    # Patient
    patch('app.models.patient.Patient.create',             return_value=42),
    patch('app.models.patient.Patient.find_by_email',      return_value=None),
    patch('app.models.patient.Patient.find_by_id',         return_value={
        'id': 42, 'name': 'John Doe', 'email': 'john@test.com'
    }),
    patch('app.models.patient.Patient.verify_password',    return_value=True),
    patch('app.models.patient.Patient.get_by_hospital',    return_value=[
        {'id': 42, 'name': 'John Doe', 'email': 'john@test.com'}
    ]),
    # OTP
    patch('app.controllers.auth_controller.generate_otp',  return_value='123456'),
    patch('app.controllers.auth_controller.verify_otp',    return_value=True),
    # Appointment
    patch('app.models.appointment.Appointment.create',         return_value=101),
    patch('app.models.appointment.Appointment.find_by_id',     return_value={
        'id': 101, 'patient_id': 42, 'doctor_id': 'DOC001', 'hospital_id': 'HOSP001'
    }),
    patch('app.models.appointment.Appointment.update_status',  return_value=1),
    patch('app.models.appointment.Appointment.get_by_patient', return_value=[
        {'id': 101, 'doctor_id': 'DOC001', 'hospital_id': 'HOSP001', 'status': 'scheduled'}
    ]),
    patch('app.models.appointment.Appointment.get_by_doctor',  return_value=[
        {'id': 101, 'patient_id': 42, 'hospital_id': 'HOSP001', 'status': 'scheduled'}
    ]),
    patch('app.models.appointment.Appointment.get_by_hospital',return_value=[
        {'id': 101, 'patient_id': 42, 'doctor_id': 'DOC001', 'status': 'scheduled'}
    ]),
    # Prescription
    patch('app.models.prescription.Prescription.create',        return_value=501),
    patch('app.models.prescription.Prescription.find_by_id',    return_value={
        'id': 501, 'appointment_id': 101, 'patient_id': 42,
        'doctor_id': 'DOC001', 'diagnosis': 'Seasonal Allergies',
        'medicines': 'Cetirizine 10mg'
    }),
    patch('app.models.prescription.Prescription.get_by_patient',return_value=[
        {'id': 501, 'diagnosis': 'Seasonal Allergies', 'medicines': 'Cetirizine 10mg'}
    ]),
    patch('app.models.prescription.Prescription.get_by_doctor', return_value=[
        {'id': 501, 'diagnosis': 'Seasonal Allergies', 'medicines': 'Cetirizine 10mg'}
    ]),
    # PDF
    patch('app.utils.pdf_generator.generate_prescription_pdf',
          return_value=io.BytesIO(b'%PDF mock')),
    # Gemini AI
    patch('google.generativeai.GenerativeModel'),
]

started = [p.start() for p in patches]

# ── create the Flask app and run ──────────────────────────────────────
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n[LOAD-TEST SERVER] Flask API running on port {port} (DB fully mocked)")
    print("[LOAD-TEST SERVER] Press Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
