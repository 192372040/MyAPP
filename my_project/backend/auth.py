
import random
from flask import request, jsonify
from db import get_db_connection
# pyrefly: ignore [missing-import]
from sendgrid import SendGridAPIClient
# pyrefly: ignore [missing-import]
from sendgrid.helpers.mail import Mail
def send_otp():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email or not email.strip():
            return jsonify({"error": "Email is required"}), 400

        email = email.strip()
        otp = str(random.randint(100000, 999999))

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO otp_verification (email, otp) VALUES (%s, %s)"
        cursor.execute(query, (email, otp))
        conn.commit()

        # ✅ Send Email using SendGrid
        message = Mail(
            from_email='varunprabha999@gmail.com',
            to_emails=email,
            subject='MediConnect OTP Verification Code',
            plain_text_content=f"Your MediConnect OTP is {otp}",
            html_content=f"""
            <p>Hello,</p>
            <p>Your <b>MediConnect</b> OTP is:</p>
            <h2>{otp}</h2>
            <p>This OTP is valid for 5 minutes.</p>
            <p>If you did not request this, please ignore this email.</p>
            <br>
            <p>Thanks,<br>MediConnect Team</p>
            """
        )

        try:
            sg = SendGridAPIClient("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")
            response = sg.send(message)
            print("Status Code:", response.status_code)
            if response.status_code >= 400:
                return jsonify({"error": "Failed to send email. Please check the email address and try again."}), 500
        except Exception as e:
            print("Email Error:", e)
            cursor.close()
            conn.close()
            return jsonify({"error": f"Email Error: {e}"}), 500

        cursor.close()
        conn.close()

        return jsonify({"message": "OTP sent to email"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
def verify_otp():
    try:
        data = request.get_json()
        email = data.get("email")
        otp = data.get("otp").strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Step 1: get latest OTP
        query = """
        SELECT otp FROM otp_verification 
        WHERE email=%s 
        ORDER BY id DESC LIMIT 1
        """
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            stored_otp = str(result["otp"]).strip()

            print("ENTERED OTP:", otp)
            print("STORED OTP:", stored_otp)

            if otp == stored_otp:

                # Step 2: check user
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()

                if user:
                    cursor.close()
                    conn.close()

                    return jsonify({
                        "message": "Login successful",
                        "user": user
                    })
                else:
                    cursor.close()
                    conn.close()

                    return jsonify({
                        "message": "OTP verified but user not registered"
                    })

        cursor.close()
        conn.close()

        return jsonify({"error": "Invalid OTP"})

    except Exception as e:
        return jsonify({"error": str(e)})
def generate_patient_id(conn):
    temp_cursor = conn.cursor()
    temp_cursor.execute("SELECT MAX(id) FROM users")
    result = temp_cursor.fetchone()
    temp_cursor.close()

    max_id = result[0]
    next_id = 1 if max_id is None else max_id + 1

    return f"MED-PAT-2026-{str(next_id).zfill(5)}"
def update_profile():
    
    try:
        data = request.get_json()
        print("Incoming data:", data)
        email = data.get("email").strip().lower()
        phone = data.get("phone")
        name = data.get("name")
        age = data.get("age")
        blood_group = data.get("blood_group")
        gender = data.get("gender")
    

        medical_history = data.get("medical_history", [])
        medical_history_str = ",".join(medical_history) if medical_history else ""

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 🔍 Check if user exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            # 🔄 UPDATE existing user
            query = """
            UPDATE users 
            SET name=%s, phone=%s, age=%s, blood_group=%s, gender=%s, medical_history=%s
            WHERE email=%s
            """
            cursor.execute(query, (
                name, phone, age, blood_group, gender, medical_history_str, email
            ))

        else:
            # ✅ Generate patient ID
            patient_id = generate_patient_id(conn)

            query = """
            INSERT INTO users (email, name, phone, age, blood_group, gender, medical_history, patient_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                email, name, phone, age, blood_group, gender, medical_history_str, patient_id
            ))

        conn.commit()

        # ✅ Fetch updated user (important for frontend)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        updated_user = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Profile saved successfully",
            "user": updated_user
        })

    except Exception as e:
      print("BACKEND ERROR:", e)
      return jsonify({"error": str(e)})

def delete_account():
    try:
        data = request.get_json()
        email = data.get("email")
        if not email:
            return jsonify({"success": False, "error": "Email is required"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM prescriptions WHERE patient_email = %s", (email,))
        cursor.execute("DELETE FROM appointments WHERE patient_email = %s", (email,))
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Account deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})