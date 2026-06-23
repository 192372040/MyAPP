"""
=============================================================================
  Medicate API — Baseline / Load Test
  Tool   : Locust (https://locust.io)
  Config : 100 virtual users, 1-minute ramp-up + sustain

  HOW TO RUN (preferred — uses load_test_server.py with mocked DB):
      python run_load_test.py

  HOW TO RUN (manual, against a live server):
      locust -f locustfile.py --headless -u 100 -r 10 -t 1m \
             --host http://localhost:5000 --csv load_results
=============================================================================
"""

import os
import sys
import random
from locust import HttpUser, task, between

# ---------------------------------------------------------------------------
# Pre-generate JWT tokens via the app's own utility so every virtual user
# starts authenticated immediately — no register/login round-trip needed.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from unittest.mock import patch
    with patch('app.models.database.init_db'):
        from app.utils.auth_middleware import generate_token

    _ADMIN_TOKEN   = generate_token('HOSP001', 'admin',   'City General Hospital')
    _DOCTOR_TOKEN  = generate_token('DOC001',  'doctor',  'Dr. Sarah Connor')
    _PATIENT_TOKEN = generate_token(42,        'patient', 'John Doe')

    print("[locustfile] JWT tokens pre-generated successfully.")

except Exception as e:
    # Fallback: if app can't be imported (e.g. external live server),
    # tokens will remain None and tasks will run unauthenticated.
    print(f"[locustfile] Could not pre-generate tokens: {e}")
    _ADMIN_TOKEN   = None
    _DOCTOR_TOKEN  = None
    _PATIENT_TOKEN = None


# ---------------------------------------------------------------------------
# Virtual User Behaviour
# ---------------------------------------------------------------------------
class MedicateUser(HttpUser):
    """
    Simulates a realistic mixed workload across all three user roles.
    wait_time = think-time between consecutive requests per user (0.5–2 s).
    """
    wait_time = between(0.5, 2.0)

    def on_start(self):
        """Assign pre-generated tokens — no HTTP setup calls needed."""
        self._admin_hdr   = {"Authorization": f"Bearer {_ADMIN_TOKEN}"}   if _ADMIN_TOKEN   else {}
        self._doctor_hdr  = {"Authorization": f"Bearer {_DOCTOR_TOKEN}"}  if _DOCTOR_TOKEN  else {}
        self._patient_hdr = {"Authorization": f"Bearer {_PATIENT_TOKEN}"} if _PATIENT_TOKEN else {}

    # ================================================================== #
    #  TASKS  — weight = relative selection frequency
    # ================================================================== #

    # ── Health-check (lightest, highest weight) ────────────────────────
    @task(5)
    def health_check(self):
        with self.client.get("/", catch_response=True, name="Health Check (/)") as r:
            r.success() if r.status_code == 200 else r.failure(f"Got {r.status_code}")

    # ── Auth endpoints (public, weight 3) ─────────────────────────────
    @task(3)
    def login_admin(self):
        with self.client.post(
            "/api/admin/login",
            json={"email": "admin@medicate.com", "password": "Admin@123"},
            catch_response=True, name="Admin Login"
        ) as r:
            r.success() if r.status_code in (200, 400, 401) else r.failure(f"Got {r.status_code}")

    @task(3)
    def login_doctor(self):
        with self.client.post(
            "/api/doctor/login",
            json={"email": "doctor@medicate.com", "password": "Doctor@123"},
            catch_response=True, name="Doctor Login"
        ) as r:
            r.success() if r.status_code in (200, 400, 401) else r.failure(f"Got {r.status_code}")

    @task(3)
    def login_patient(self):
        with self.client.post(
            "/api/patient/login",
            json={"email": "patient@medicate.com", "password": "Patient@123"},
            catch_response=True, name="Patient Login"
        ) as r:
            r.success() if r.status_code in (200, 400, 401) else r.failure(f"Got {r.status_code}")

    # ── Admin dashboard (weight 2) ─────────────────────────────────────
    @task(2)
    def admin_view_doctors(self):
        with self.client.get(
            "/api/admin/doctors", headers=self._admin_hdr,
            catch_response=True, name="Admin: View Doctors"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(2)
    def admin_view_patients(self):
        with self.client.get(
            "/api/admin/patients", headers=self._admin_hdr,
            catch_response=True, name="Admin: View Patients"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(2)
    def admin_view_appointments(self):
        with self.client.get(
            "/api/admin/appointments", headers=self._admin_hdr,
            catch_response=True, name="Admin: View Appointments"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    # ── Doctor dashboard (weight 3) ────────────────────────────────────
    @task(3)
    def doctor_view_appointments(self):
        with self.client.get(
            "/api/doctor/appointments", headers=self._doctor_hdr,
            catch_response=True, name="Doctor: View Appointments"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(3)
    def doctor_view_prescriptions(self):
        with self.client.get(
            "/api/doctor/prescriptions", headers=self._doctor_hdr,
            catch_response=True, name="Doctor: View Prescriptions"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(2)
    def doctor_view_slots(self):
        with self.client.get(
            "/api/doctor/slots", headers=self._doctor_hdr,
            catch_response=True, name="Doctor: View Slots"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(1)
    def doctor_add_slot(self):
        payload = {
            "slot_date": "2026-08-01",
            "slot_time": f"{random.randint(8, 17):02d}:00:00"
        }
        with self.client.post(
            "/api/doctor/slots", json=payload, headers=self._doctor_hdr,
            catch_response=True, name="Doctor: Add Slot"
        ) as r:
            r.success() if r.status_code in (200, 201, 400, 401, 403) else r.failure(f"Got {r.status_code}")

    # ── Patient dashboard (weight 4 — highest traffic) ─────────────────
    @task(4)
    def patient_view_hospitals(self):
        with self.client.get(
            "/api/patient/hospitals", headers=self._patient_hdr,
            catch_response=True, name="Patient: View Hospitals"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(4)
    def patient_view_appointments(self):
        with self.client.get(
            "/api/patient/appointments", headers=self._patient_hdr,
            catch_response=True, name="Patient: View Appointments"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(3)
    def patient_view_prescriptions(self):
        with self.client.get(
            "/api/patient/prescriptions", headers=self._patient_hdr,
            catch_response=True, name="Patient: View Prescriptions"
        ) as r:
            r.success() if r.status_code in (200, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(2)
    def patient_view_hospital_doctors(self):
        with self.client.get(
            "/api/patient/hospital/HOSP001/doctors", headers=self._patient_hdr,
            catch_response=True, name="Patient: View Hospital Doctors"
        ) as r:
            r.success() if r.status_code in (200, 404, 401, 403) else r.failure(f"Got {r.status_code}")

    @task(2)
    def patient_get_doctor_slots(self):
        with self.client.get(
            "/api/patient/doctor/DOC001/slots", headers=self._patient_hdr,
            catch_response=True, name="Patient: Get Doctor Slots"
        ) as r:
            r.success() if r.status_code in (200, 404, 401, 403) else r.failure(f"Got {r.status_code}")
