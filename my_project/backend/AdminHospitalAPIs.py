from flask import request, jsonify
from db import get_db_connection

def get_hospital_appointments():
    try:
        hospital_id = request.args.get("hospital_id")
        appointment_date = request.args.get("appointment_date") # Optional
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # We need to map hospital_id to hospital_name if appointments are saved by hospital_name
        # Or if appointments table has hospital_id. Looking at hospitalbooking.py, it uses hospital_name.
        # But we get hospital_id from frontend. Let's fetch hospital_name first.
        cursor.execute("SELECT hospital_name FROM admin_hospitals WHERE hospital_id = %s", (hospital_id,))
        h_data = cursor.fetchone()
        
        if not h_data:
            return jsonify({"success": False, "error": "Hospital not found"}), 404
            
        hospital_name = h_data['hospital_name']
        
        if appointment_date:
            query = """
            SELECT * FROM appointments 
            WHERE hospital_name = %s AND appointment_date = %s
            ORDER BY appointment_slot
            """
            cursor.execute(query, (hospital_name, appointment_date))
        else:
            query = """
            SELECT * FROM appointments 
            WHERE hospital_name = %s
            ORDER BY appointment_date DESC, appointment_slot ASC
            """
            cursor.execute(query, (hospital_name,))
            
        appointments = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "appointments": appointments})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_hospital_beds():
    try:
        hospital_id = request.args.get("hospital_id")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM hospital_beds WHERE hospital_id = %s"
        cursor.execute(query, (hospital_id,))
        beds = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "beds": beds})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def update_hospital_beds():
    try:
        data = request.get_json()
        hospital_id = data.get("hospital_id")
        ward_name = data.get("ward_name")
        available_beds = data.get("available_beds")
        occupied_beds = data.get("occupied_beds")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if ward exists
        cursor.execute("SELECT id FROM hospital_beds WHERE hospital_id = %s AND ward_name = %s", (hospital_id, ward_name))
        existing = cursor.fetchone()
        
        if existing:
            query = "UPDATE hospital_beds SET available_beds = %s, occupied_beds = %s WHERE id = %s"
            cursor.execute(query, (available_beds, occupied_beds, existing[0]))
        else:
            query = "INSERT INTO hospital_beds (hospital_id, ward_name, available_beds, occupied_beds) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (hospital_id, ward_name, available_beds, occupied_beds))
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Beds updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_hospital_analytics():
    try:
        hospital_id = request.args.get("hospital_id")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT hospital_name FROM admin_hospitals WHERE hospital_id = %s", (hospital_id,))
        h_data = cursor.fetchone()
        if not h_data:
            return jsonify({"success": False, "error": "Hospital not found"}), 404
        hospital_name = h_data['hospital_name']
        
        # 1. Total Doctors
        cursor.execute("SELECT COUNT(*) as total_doctors FROM hospital_doctors WHERE hospital_id = %s", (hospital_id,))
        total_doctors = cursor.fetchone()['total_doctors']
        
        # 2. Total Beds
        cursor.execute("SELECT SUM(available_beds + occupied_beds) as total_beds, SUM(occupied_beds) as total_occupied FROM hospital_beds WHERE hospital_id = %s", (hospital_id,))
        bed_stats = cursor.fetchone()
        total_beds = bed_stats['total_beds'] or 0
        total_occupied = bed_stats['total_occupied'] or 0
        
        # 3. Appointments Today
        from datetime import date
        today = date.today().isoformat()
        
        cursor.execute("SELECT COUNT(*) as today_appointments FROM appointments WHERE hospital_name = %s AND appointment_date = %s", (hospital_name, today))
        today_appointments = cursor.fetchone()['today_appointments']
        
        # 4. Revenue Today
        cursor.execute("SELECT SUM(CAST(REPLACE(consultation_fee, 'Rs ', '') AS DECIMAL(10,2))) as today_revenue FROM appointments WHERE hospital_name = %s AND appointment_date = %s", (hospital_name, today))
        today_revenue = cursor.fetchone()['today_revenue'] or 0
        
        # 5. Department wise patients (All time or today? Let's do all time)
        cursor.execute("SELECT specialization, COUNT(*) as count FROM appointments WHERE hospital_name = %s GROUP BY specialization", (hospital_name,))
        dept_stats = cursor.fetchall()
        
        total_departments = len(dept_stats)
        
        # 6. Revenue Trend (Monthly)
        cursor.execute("SELECT SUBSTRING(appointment_date, 1, 7) as month, SUM(CAST(REPLACE(consultation_fee, 'Rs ', '') AS DECIMAL(10,2))) as revenue FROM appointments WHERE hospital_name = %s GROUP BY month ORDER BY month", (hospital_name,))
        revenue_trend = cursor.fetchall()
        
        # 7. Patient visits trend (Daily)
        cursor.execute("SELECT appointment_date as date, COUNT(*) as count FROM appointments WHERE hospital_name = %s GROUP BY date ORDER BY date LIMIT 30", (hospital_name,))
        visits_trend = cursor.fetchall()
        
        # 8. Top Performance Doctors
        cursor.execute("SELECT doctor_name, COUNT(*) as appointments_count FROM appointments WHERE hospital_name = %s GROUP BY doctor_name ORDER BY appointments_count DESC LIMIT 5", (hospital_name,))
        top_doctors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "total_doctors": total_doctors,
            "total_beds": total_beds,
            "total_occupied": total_occupied,
            "total_departments": total_departments,
            "today_appointments": today_appointments,
            "today_revenue": float(today_revenue),
            "dept_stats": dept_stats,
            "revenue_trend": revenue_trend,
            "visits_trend": visits_trend,
            "top_doctors": top_doctors
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
