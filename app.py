import os
import json
import csv
import io
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
from database import (
    init_db, save_response, get_all_responses, get_response_by_id, 
    clear_all_responses, get_faculty_by_dept, get_roster_departments,
    get_faculty_tracking
)
from analytics_engine import compute_analytics
from sync_roster import sync_roster_to_db
from seed_data import generate_sample_responses

app = Flask(__name__)
app.config['SECRET_KEY'] = 'faculty-feedback-secret-key-2025-26'

# Ensure DB & Faculty Roster are initialized on startup
init_db()
sync_roster_to_db()

# ----------------- FACULTY VIEW ROUTES (NO ANALYTICS VISIBLE) ----------------- #

@app.route("/")
@app.route("/feedback")
def faculty_form_view():
    departments = get_roster_departments()
    return render_template("faculty_form.html", departments=departments)

@app.route("/submitted")
def faculty_submitted_view():
    return render_template("faculty_success.html")

@app.route("/api/faculty", methods=["GET"])
def api_get_faculty_by_dept():
    department = request.args.get("department", "")
    faculty_list = get_faculty_by_dept(department=department)
    return jsonify({"success": True, "count": len(faculty_list), "faculty": faculty_list})

@app.route("/api/submit", methods=["POST"])
def api_submit():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400
        
        # Validation
        if not data.get("department") or not data.get("faculty_name") or not data.get("course_level"):
            return jsonify({"success": False, "error": "Department, Faculty Name, and Course Level are required"}), 400
        
        response_id = save_response(data)
        return jsonify({
            "success": True,
            "message": "Feedback submitted successfully! Thank you for contributing to the 2025-26 Curricular Revision.",
            "response_id": response_id
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ----------------- ADMIN PORTAL ROUTES (ANALYTICS & TRACKING) ----------------- #

@app.route("/admin")
@app.route("/admin/tracking")
def admin_tracking_view():
    departments = get_roster_departments()
    return render_template("admin_tracking.html", departments=departments)

@app.route("/admin/dashboard")
def admin_dashboard_view():
    departments = get_roster_departments()
    return render_template("dashboard.html", departments=departments)

@app.route("/admin/responses")
def admin_responses_view():
    departments = get_roster_departments()
    return render_template("responses.html", departments=departments)

@app.route("/admin/report")
def admin_report_view():
    department = request.args.get("department", "All")
    course_level = request.args.get("course_level", "All")
    analytics = compute_analytics(department=department, course_level=course_level)
    departments = get_roster_departments()
    return render_template("report.html", analytics=analytics, department=department, course_level=course_level, departments=departments)

# ----------------- ADMIN REST APIS & EXPORTS ----------------- #

@app.route("/api/faculty/tracking", methods=["GET"])
def api_faculty_tracking():
    department = request.args.get("department", "All")
    status = request.args.get("status", "ALL")
    search = request.args.get("search", "")
    shift = request.args.get("shift", "All")
    
    tracking_data = get_faculty_tracking(department=department, status=status, search=search, shift=shift)
    return jsonify({"success": True, **tracking_data})

@app.route("/api/analytics", methods=["GET"])
def api_analytics():
    department = request.args.get("department", "All")
    course_level = request.args.get("course_level", "All")
    analytics = compute_analytics(department=department, course_level=course_level)
    return jsonify(analytics)

@app.route("/api/responses", methods=["GET"])
def api_get_responses():
    department = request.args.get("department", "All")
    course_level = request.args.get("course_level", "All")
    responses = get_all_responses(department=department, course_level=course_level)
    return jsonify({"success": True, "count": len(responses), "responses": responses})

@app.route("/api/responses/<int:response_id>", methods=["GET"])
def api_get_single_response(response_id):
    resp = get_response_by_id(response_id)
    if not resp:
        return jsonify({"success": False, "error": "Response not found"}), 404
    return jsonify({"success": True, "response": resp})

@app.route("/api/export/pending", methods=["GET"])
def api_export_pending():
    department = request.args.get("department", "All")
    tracking = get_faculty_tracking(department=department, status="PENDING")
    pending_list = [f for f in tracking["faculty_list"] if f["status"] == "PENDING"]
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["S.No", "Department", "Faculty Name", "Designation", "Shift", "Email Address", "Status"])
    
    for f in pending_list:
        writer.writerow([
            f.get("s_no", ""),
            f.get("department", ""),
            f.get("name", ""),
            f.get("designation", ""),
            f.get("shift", ""),
            f.get("email", ""),
            "PENDING"
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=pending_faculty_feedback_list.csv"}
    )

@app.route("/api/export/csv", methods=["GET"])
def api_export_csv():
    department = request.args.get("department", "All")
    course_level = request.args.get("course_level", "All")
    responses = get_all_responses(department=department, course_level=course_level)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    headers = [
        "Response ID", "Timestamp", "Department", "Faculty Name", "Faculty Email", "Course Level",
        "Multidisciplinary Rating (1-5)", "Electives Rating", "NEP Challenges",
        "NSQF Alignment", "NSQF Redesign Courses", "Overlapping Courses",
        "Overlapping Details", "IKS Effectiveness (1-5)", "Courses to Revise", "Other Recommendations"
    ]
    writer.writerow(headers)
    
    for r in responses:
        writer.writerow([
            r.get("id"),
            r.get("timestamp"),
            r.get("department"),
            r.get("faculty_name"),
            r.get("faculty_email"),
            r.get("course_level"),
            r.get("multidisciplinary_rating"),
            r.get("electives_rating"),
            r.get("nep_challenges"),
            r.get("nsqf_alignment"),
            r.get("nsqf_courses"),
            r.get("overlapping_courses"),
            r.get("overlapping_details"),
            r.get("iks_effectiveness"),
            r.get("courses_to_revise"),
            r.get("other_recommendations")
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=faculty_feedback_curriculum_2025_26.csv"}
    )

@app.route("/api/export/json", methods=["GET"])
def api_export_json():
    department = request.args.get("department", "All")
    course_level = request.args.get("course_level", "All")
    responses = get_all_responses(department=department, course_level=course_level)
    return Response(
        json.dumps(responses, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=faculty_feedback_raw.json"}
    )

@app.route("/api/seed", methods=["POST"])
def api_seed_data():
    try:
        count = int(request.json.get("count", 25) if request.is_json else 25)
        generate_sample_responses(count)
        return jsonify({"success": True, "message": f"Added {count} sample faculty feedback records."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/clear", methods=["POST"])
def api_clear_data():
    try:
        clear_all_responses()
        return jsonify({"success": True, "message": "All feedback records cleared."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
