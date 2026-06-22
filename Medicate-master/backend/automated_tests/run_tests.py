import json
import csv
import os
import sys
from unittest.mock import patch, MagicMock

# Ensure the parent directory is on the path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.utils.auth_middleware import generate_token

class DynamicTestRunner:
    def __init__(self):
        # Patch init_db so Flask boots without MySQL
        self.db_patcher = patch('app.models.database.init_db')
        self.mock_init_db = self.db_patcher.start()
        
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # List to track active patchers for clean termination
        self.active_patchers = []
        
    def cleanup(self):
        # Stop all dynamically started patchers
        for patcher in reversed(self.active_patchers):
            patcher.stop()
        self.app_context.pop()
        self.db_patcher.stop()

    def start_patcher(self, target, **kwargs):
        patcher = patch(target, **kwargs)
        mock_obj = patcher.start()
        self.active_patchers.append(patcher)
        return mock_obj

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_json_path = os.path.join(current_dir, 'input.json')
        report_csv_path = os.path.join(current_dir, 'test_run_report.csv')
        
        if not os.path.exists(input_json_path):
            print(f"Error: {input_json_path} does not exist.")
            return
            
        with open(input_json_path, 'r') as f:
            data = json.load(f)
            
        test_cases = data.get('test_cases', [])
        results = []
        
        print("\n" + "="*60)
        print("          STARTING AUTOMATED BACKEND API TESTS          ")
        print("="*60)
        
        # Register and start all mock patchers programmatically to prevent static nesting limit errors
        mock_hosp_create = self.start_patcher('app.models.hospital.Hospital.create')
        mock_hosp_find_email = self.start_patcher('app.models.hospital.Hospital.find_by_email')
        mock_hosp_find_id = self.start_patcher('app.models.hospital.Hospital.find_by_id')
        mock_hosp_verify_pass = self.start_patcher('app.models.hospital.Hospital.verify_password')
        
        mock_doc_create = self.start_patcher('app.models.doctor.Doctor.create')
        mock_doc_find_email = self.start_patcher('app.models.doctor.Doctor.find_by_email')
        mock_doc_find_id = self.start_patcher('app.models.doctor.Doctor.find_by_id')
        mock_doc_verify_pass = self.start_patcher('app.models.doctor.Doctor.verify_password')
        mock_doc_add_slot = self.start_patcher('app.models.doctor.Doctor.add_availability_slot')
        
        mock_pat_find_email = self.start_patcher('app.models.patient.Patient.find_by_email')
        mock_pat_create = self.start_patcher('app.models.patient.Patient.create')
        mock_pat_find_id = self.start_patcher('app.models.patient.Patient.find_by_id')
        mock_pat_verify_pass = self.start_patcher('app.models.patient.Patient.verify_password')
        
        # Patch verify_otp and generate_otp in the auth_controller namespace directly
        mock_gen_otp = self.start_patcher('app.controllers.auth_controller.generate_otp')
        mock_verify_otp = self.start_patcher('app.controllers.auth_controller.verify_otp')
        
        mock_app_create = self.start_patcher('app.models.appointment.Appointment.create')
        mock_app_find_id = self.start_patcher('app.models.appointment.Appointment.find_by_id')
        mock_app_update_status = self.start_patcher('app.models.appointment.Appointment.update_status')
        mock_presc_create = self.start_patcher('app.models.prescription.Prescription.create')
        
        # Additional mocks to cover 50 test cases
        mock_doc_add_to_hosp = self.start_patcher('app.models.doctor.Doctor.add_to_hospital')
        mock_doc_get_by_hosp = self.start_patcher('app.models.doctor.Doctor.get_by_hospital')
        mock_pat_get_by_hosp = self.start_patcher('app.models.patient.Patient.get_by_hospital')
        mock_doc_get_all_slots = self.start_patcher('app.models.doctor.Doctor.get_all_slots')
        mock_hosp_get_all = self.start_patcher('app.models.hospital.Hospital.get_all')
        mock_app_get_by_pat = self.start_patcher('app.models.appointment.Appointment.get_by_patient')
        mock_app_get_by_doc = self.start_patcher('app.models.appointment.Appointment.get_by_doctor')
        mock_app_get_by_hosp = self.start_patcher('app.models.appointment.Appointment.get_by_hospital')
        mock_doc_get_avail_slots = self.start_patcher('app.models.doctor.Doctor.get_available_slots')
        mock_presc_get_by_pat = self.start_patcher('app.models.prescription.Prescription.get_by_patient')
        mock_presc_get_by_doc = self.start_patcher('app.models.prescription.Prescription.get_by_doctor')
        mock_presc_find_id = self.start_patcher('app.models.prescription.Prescription.find_by_id')
        mock_generate_pdf = self.start_patcher('app.utils.pdf_generator.generate_prescription_pdf')
        
        mock_gemini = self.start_patcher('google.generativeai.GenerativeModel')

        # Setup standard mock behaviors
        mock_hosp_find_email.return_value = None
        mock_hosp_create.return_value = 'HOSP001'
        mock_hosp_find_id.return_value = {'id': 'HOSP001', 'name': 'City General Hospital', 'password_hash': 'hash'}
        mock_hosp_verify_pass.return_value = True
        
        mock_doc_find_email.return_value = None
        mock_doc_create.return_value = 'DOC001'
        mock_doc_find_id.return_value = {'id': 'DOC001', 'name': 'Dr. Sarah Connor', 'password_hash': 'hash'}
        mock_doc_verify_pass.return_value = True
        mock_doc_add_slot.return_value = True
        
        mock_pat_find_email.return_value = None
        mock_pat_create.return_value = 42
        mock_pat_find_id.return_value = {'id': 42, 'name': 'John Doe', 'email': 'john.doe@gmail.com'}
        mock_pat_verify_pass.return_value = True
        mock_gen_otp.return_value = '112233'
        mock_verify_otp.return_value = True
        
        mock_app_create.return_value = 101
        mock_app_find_id.return_value = {'id': 101, 'patient_id': 42, 'doctor_id': 'DOC001'}
        mock_app_update_status.return_value = 1
        mock_presc_create.return_value = 501
        
        mock_doc_add_to_hosp.return_value = True
        mock_doc_get_by_hosp.return_value = [{'id': 'DOC001', 'name': 'Dr. Sarah Connor'}]
        mock_pat_get_by_hosp.return_value = [{'id': 42, 'name': 'John Doe'}]
        mock_doc_get_all_slots.return_value = [{'id': 1, 'slot_date': '2026-06-15', 'slot_time': '10:30:00', 'is_booked': False}]
        mock_hosp_get_all.return_value = [{'id': 'HOSP001', 'name': 'City General Hospital'}]
        mock_app_get_by_pat.return_value = [{'id': 101, 'doctor_id': 'DOC001', 'hospital_id': 'HOSP001'}]
        mock_app_get_by_doc.return_value = [{'id': 101, 'patient_id': 42, 'hospital_id': 'HOSP001'}]
        mock_app_get_by_hosp.return_value = [{'id': 101, 'patient_id': 42, 'doctor_id': 'DOC001'}]
        mock_doc_get_avail_slots.return_value = [{'id': 1, 'slot_date': '2026-06-15', 'slot_time': '10:30:00', 'is_booked': False}]
        mock_presc_get_by_pat.return_value = [{'id': 501, 'diagnosis': 'Seasonal Allergies'}]
        mock_presc_get_by_doc.return_value = [{'id': 501, 'diagnosis': 'Seasonal Allergies'}]
        mock_presc_find_id.return_value = {'id': 501, 'appointment_id': 101, 'patient_id': 42, 'doctor_id': 'DOC001', 'diagnosis': 'Seasonal Allergies', 'medicines': 'Cetirizine 10mg'}
        
        import io
        mock_generate_pdf.return_value = io.BytesIO(b"PDF data")
        
        # Mock Gemini AI model response
        mock_chat_session = MagicMock()
        mock_chat_session.send_message.return_value.text = "This is a simulated health guidance message."
        mock_gemini.return_value.start_chat.return_value = mock_chat_session

        # Iterate through the test cases
        for tc in test_cases:
            tc_id = tc.get('id')
            name = tc.get('name')
            endpoint = tc.get('endpoint')
            method = tc.get('method', 'POST')
            payload = tc.get('payload', {})
            expected_status = tc.get('expected_status')
            role = tc.get('role')
            
            # Reset default mock values per test case to avoid state leakage
            mock_hosp_find_email.return_value = None
            mock_doc_find_email.return_value = None
            mock_pat_find_email.return_value = None
            mock_hosp_verify_pass.return_value = True
            mock_doc_verify_pass.return_value = True
            mock_pat_verify_pass.return_value = True
            mock_verify_otp.return_value = True
            
            # Context-specific mock adjustments
            if tc_id == "TC003": # Admin Login - Success
                mock_hosp_find_id.return_value = {'id': 'HOSP001', 'name': 'City General Hospital', 'password_hash': 'hash'}
                mock_hosp_verify_pass.return_value = True
            elif tc_id == "TC004": # Admin Login - Invalid Credentials
                mock_hosp_find_id.return_value = {'id': 'HOSP001', 'name': 'City General Hospital', 'password_hash': 'hash'}
                mock_hosp_verify_pass.return_value = False
            elif tc_id == "TC007": # Doctor Login - Success
                mock_doc_find_id.return_value = {'id': 'DOC001', 'name': 'Dr. Sarah Connor', 'password_hash': 'hash'}
                mock_doc_verify_pass.return_value = True
            elif tc_id == "TC011": # Patient Registration - Success
                mock_pat_find_email.return_value = None
                mock_verify_otp.return_value = True
            elif tc_id == "TC012": # Patient Registration - Invalid OTP
                mock_verify_otp.return_value = False
            elif tc_id == "TC013": # Patient Login - Success
                mock_pat_find_email.return_value = {'id': 42, 'name': 'John Doe', 'email': 'john.doe@gmail.com', 'password_hash': 'hash'}
                mock_pat_verify_pass.return_value = True
            
            # Prepare headers
            headers = {}
            if role:
                # Generate a JWT token dynamically based on role
                if role == 'admin':
                    token = generate_token('HOSP001', 'admin', 'City General Hospital')
                elif role == 'doctor':
                    token = generate_token('DOC001', 'doctor', 'Dr. Sarah Connor')
                elif role == 'patient':
                    token = generate_token(42, 'patient', 'John Doe')
                else:
                    token = ""
                headers['Authorization'] = f'Bearer {token}'
            
            # Execute request using test client
            print(f"Running [{tc_id}] {name}...", end="")
            sys.stdout.flush()
            
            try:
                response = self.client.open(
                    endpoint,
                    method=method,
                    data=json.dumps(payload),
                    headers=headers,
                    content_type='application/json'
                )
                
                actual_status = response.status_code
                response_data = json.loads(response.data.decode('utf-8')) if response.data else {}
                if isinstance(response_data, dict):
                    message = response_data.get('message', str(response_data))
                else:
                    message = str(response_data)
                
                verdict = "PASS" if actual_status == expected_status else "FAIL"
                print(f" {verdict} (Expected {expected_status}, Got {actual_status})")
                sys.stdout.flush()
                
                results.append({
                    'id': tc_id,
                    'name': name,
                    'endpoint': endpoint,
                    'method': method,
                    'expected_status': expected_status,
                    'actual_status': actual_status,
                    'verdict': verdict,
                    'message': message
                })
            except Exception as ex:
                print(f" ERROR: {str(ex)}")
                sys.stdout.flush()
                results.append({
                    'id': tc_id,
                    'name': name,
                    'endpoint': endpoint,
                    'method': method,
                    'expected_status': expected_status,
                    'actual_status': 500,
                    'verdict': "FAIL",
                    'message': f"Internal Test Framework Error: {str(ex)}"
                })
                
        # Write results report spreadsheet
        headers = ['Test Case ID', 'Test Case Name', 'API Endpoint', 'HTTP Method', 'Expected Status', 'Actual Status', 'Verdict', 'Response Message']
        
        try:
            f = open(report_csv_path, 'w', newline='', encoding='utf-8')
            file_written_to = report_csv_path
        except PermissionError:
            fallback_path = report_csv_path.replace('.csv', '_pass_fail.csv')
            print(f"Permission denied on {report_csv_path}. Trying: {fallback_path}")
            try:
                f = open(fallback_path, 'w', newline='', encoding='utf-8')
                file_written_to = fallback_path
            except PermissionError:
                i = 1
                while True:
                    candidate = report_csv_path.replace('.csv', f'_pass_fail_{i}.csv')
                    try:
                        f = open(candidate, 'w', newline='', encoding='utf-8')
                        file_written_to = candidate
                        break
                    except PermissionError:
                        i += 1
                        
        with f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for res in results:
                writer.writerow([
                    res['id'],
                    res['name'],
                    res['endpoint'],
                    res['method'],
                    res['expected_status'],
                    res['actual_status'],
                    res['verdict'],
                    res['message']
                ])
                
        print("="*60)
        print(f"Backend API tests completed. Report generated at: {file_written_to}")
        print("="*60 + "\n")

if __name__ == '__main__':
    runner = DynamicTestRunner()
    try:
        runner.run()
    finally:
        runner.cleanup()
