from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  
# ---------------------------------------------------------
# DEMO COMPLAINT DATA
# ---------------------------------------------------------

complaints = [

    {
        "id": "CS-00120",
        "title": "Garbage Accumulation",
        "category": "Garbage",
        "description": "Garbage dumped near residential area",
        "location": "Lakshmi Nagar",
        "latitude": 16.5062,
        "longitude": 80.6480,
        "priority": "High",
        "status": "In Progress",
        "ai_confidence": 91,
        "severity": "HIGH",
        "priority_score": 82,
        "time": "Today"
    },

    {
        "id": "CS-00119",
        "title": "Road Damage",
        "category": "Road Damage",
        "description": "Large pothole found on main road",
        "location": "Main Road",
        "latitude": 16.5120,
        "longitude": 80.6420,
        "priority": "Critical",
        "status": "Under Review",
        "ai_confidence": 94,
        "severity": "HIGH",
        "priority_score": 94,
        "time": "Today"
    },

    {
        "id": "CS-00118",
        "title": "Streetlight Issue",
        "category": "Streetlight",
        "description": "Streetlight not working",
        "location": "College Road",
        "latitude": 16.5010,
        "longitude": 80.6500,
        "priority": "Medium",
        "status": "Assigned",
        "ai_confidence": 0,
        "severity": "MEDIUM",
        "priority_score": 64,
        "time": "Yesterday"
    }

]


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def priority_from_score(score):

    if score >= 90:
        return "Critical"

    if score >= 75:
        return "High"

    if score >= 50:
        return "Medium"

    return "Low"


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

@app.route("/")
def dashboard():

    return render_template(

        "index.html",

        complaints=complaints,

        total=len(complaints),

        new_count=sum(
            c["status"] == "Submitted"
            for c in complaints
        ),

        high=sum(
            c["priority"] == "High"
            for c in complaints
        ),

        resolved=sum(
            c["status"] == "Resolved"
            for c in complaints
        ),

        critical=sum(
            c["priority"] == "Critical"
            for c in complaints
        )

    )


# ---------------------------------------------------------
# COMPLAINTS PAGE
# ---------------------------------------------------------

@app.route("/complaints")
def complaints_page():

    return render_template(
        "complaints.html",
        complaints=complaints
    )


# ---------------------------------------------------------
# MAP PAGE
# ---------------------------------------------------------

@app.route("/map")
def map_page():

    return render_template(
        "map.html",
        complaints=complaints
    )

@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        complaints=complaints
    )


@app.route("/reports")
def reports():
    return render_template(
        "reports.html",
        complaints=complaints
    )


@app.route("/settings")
def settings():
    return render_template(
        "settings.html"
    )


@app.route("/admin")
def admin():
    return render_template(
        "admin.html",
        complaints=complaints
    )
# ---------------------------------------------------------
# ADD COMPLAINT
# ---------------------------------------------------------

@app.route("/add-complaint")
def add_complaint():

    return render_template(
        "add_complaint.html"
    )


# ---------------------------------------------------------
# API
# ---------------------------------------------------------

@app.route("/api/complaints")
def api_complaints():

    return jsonify(complaints)


# ---------------------------------------------------------
# SUBMIT COMPLAINT
# ---------------------------------------------------------

@app.route("/submit-complaint", methods=["POST"])
def submit_complaint():

    try:
        data = request.get_json(silent=True) or {}

        category = data.get("category") or "Civic Issue"
        description = data.get("description") or ""
        location = data.get("location") or "Location not provided"

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        ai = data.get("ai_analysis") or {}

        issue = ai.get("issue") or category

        try:
            confidence = float(ai.get("confidence") or 0)
        except:
            confidence = 0

        severity = ai.get("severity") or "MEDIUM"

        try:
            score = int(float(ai.get("priority_score") or 50))
        except:
            score = 50

        priority = priority_from_score(score)

        complaint = {
            "id": f"CS-{10000 + len(complaints) + 1}",
            "title": issue,
            "category": category,
            "description": description,
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "priority": priority,
            "status": "Submitted",
            "ai_confidence": confidence,
            "severity": severity,
            "priority_score": score,
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p")
        }

        complaints.insert(0, complaint)

        return jsonify({
            "success": True,
            "message": "Complaint submitted successfully.",
            "complaint": complaint
        })

    except Exception as e:

        print("SUBMIT COMPLAINT ERROR:", repr(e))

        return jsonify({
            "success": False,
            "message": "Complaint submission failed.",
            "error": str(e)
        }), 500
# ---------------------------------------------------------
# UPDATE STATUS
# ---------------------------------------------------------

@app.route(
    "/update-status/<complaint_id>",
    methods=["POST"]
)
def update_status(
    complaint_id
):

    data = request.get_json(
        silent=True
    ) or {}


    status = data.get(
        "status"
    )


    allowed = [

        "Submitted",
        "Under Review",
        "Assigned",
        "In Progress",
        "Resolved"

    ]


    if status not in allowed:

        return jsonify(
            success=False,
            message="Invalid status."
        ), 400


    for complaint in complaints:

        if complaint["id"] == complaint_id:

            complaint["status"] = status

            return jsonify(
                success=True,
                complaint=complaint
            )


    return jsonify(
        success=False,
        message="Complaint not found."
    ), 404


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )
