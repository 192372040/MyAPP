import random

from flask import request, jsonify

from db import get_db_connection

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_admin_otp():

    try:

        data = request.get_json()

        email = data.get("email")

        otp = str(
            random.randint(
                100000,
                999999,
            )
        )

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM otp_verification WHERE email=%s",
            (email,)
        )

        query = """
        INSERT INTO otp_verification
        (email, otp)
        VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (email, otp)
        )

        conn.commit()

        message = Mail(

            from_email=
            'varunprabha999@gmail.com',

            to_emails=email,

            subject=
            'Admin OTP Verification',

            plain_text_content=
            f"Your Admin OTP is {otp}",
        )

        sg = SendGridAPIClient(

            "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"
        )

        response = sg.send(message)

        print(
            response.status_code,
        )

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "OTP sent successfully"
        })

    except Exception as e:

        return jsonify({
            "error":
            str(e)
        })