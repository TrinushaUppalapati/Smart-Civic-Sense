from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
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


def model_label(class_id):

    if model is not None and hasattr(model, "names"):

        names = model.names

        if isinstance(names, dict):

            return str(
                names.get(
                    class_id,
                    f"Civic Issue {class_id}"
                )
            )

        if isinstance(names, list):

            if 0 <= class_id < len(names):

                return str(
                    names[class_id]
                )

    fallback = {

        0: "Pothole",
        1: "Road Damage",
        2: "Garbage",
        3: "Streetlight",
        4: "Water Leakage",
        5: "Drainage"

    }

    return fallback.get(
        class_id,
        "Civic Issue"
    )


def score_for_issue(issue):

    text = issue.lower()

    if (
        "pothole" in text
        or "road" in text
    ):

        return "HIGH", 90

    if "water" in text:

        return "HIGH", 85

    if (
        "garbage" in text
        or "drain" in text
    ):

        return "MEDIUM", 72

    return "MEDIUM", 65


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
# AI IMAGE ANALYSIS
# ---------------------------------------------------------

@app.route(
    "/analyze-image",
    methods=["POST"]
)
def analyze_image():

    if "image" not in request.files:

        return jsonify(
            success=False,
            message="Please upload an image."
        ), 400


    image = request.files["image"]


    if not image.filename:

        return jsonify(
            success=False,
            message="Please select an image."
        ), 400


    if not allowed_file(
        image.filename
    ):

        return jsonify(
            success=False,
            message="Use JPG, JPEG, PNG or WEBP."
        ), 400


    if model is None:

        return jsonify(
            success=False,
            message="civic_model.pt was not found or could not be loaded."
        ), 500


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    safe_name = (
        f"{uuid.uuid4().hex}_"
        f"{secure_filename(image.filename)}"
    )


    path = os.path.join(
        "uploads",
        safe_name
    )


    image.save(path)


    try:

        results = model(
            path,
            conf=0.20,
            verbose=False
        )


        boxes = results[0].boxes


        if boxes is None or len(boxes) == 0:

            return jsonify(
                success=True,
                detected=False,
                message="No civic issue detected."
            )


        best = max(
            boxes,
            key=lambda b: float(
                b.conf[0]
            )
        )


        class_id = int(
            best.cls[0]
        )


        confidence = round(
            float(best.conf[0]) * 100,
            2
        )


        issue = model_label(
            class_id
        )


        severity, score = score_for_issue(
            issue
        )


        return jsonify(

            success=True,

            detected=True,

            issue=issue,

            confidence=confidence,

            severity=severity,

            priority_score=score

        )


    except Exception as e:

        return jsonify(
            success=False,
            message=f"AI analysis failed: {e}"
        ), 500


    finally:

        try:

            os.remove(path)

        except OSError:

            pass


# ---------------------------------------------------------
# SUBMIT COMPLAINT
# ---------------------------------------------------------

@app.route(
    "/submit-complaint",
    methods=["POST"]
)
def submit_complaint():

    data = request.get_json(
        silent=True
    ) or {}


    ai = data.get(
        "ai_analysis"
    ) or {}


    category = (
        data.get("category")
        or ai.get("issue")
        or "Civic Issue"
    )


    issue = (
        ai.get("issue")
        or category
    )


    description = data.get(
        "description",
        ""
    )


    location = data.get(
        "location",
        "Location not provided"
    )


    latitude = data.get(
        "latitude"
    )


    longitude = data.get(
        "longitude"
    )


    confidence = float(
        ai.get("confidence") or 0
    )


    severity = (
        ai.get("severity")
        or "MEDIUM"
    )


    score = int(
        float(
            ai.get(
                "priority_score"
            )
            or 50
        )
    )


    priority = priority_from_score(
        score
    )


    complaint = {

        "id":
            f"CS-{10000 + len(complaints) + 1}",

        "title":
            issue,

        "category":
            category,

        "description":
            description,

        "location":
            location,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "priority":
            priority,

        "status":
            "Submitted",

        "ai_confidence":
            confidence,

        "severity":
            severity,

        "priority_score":
            score,

        "time":
            datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )

    }


    complaints.insert(
        0,
        complaint
    )


    return jsonify(

        success=True,

        message=
            "Complaint submitted successfully.",

        complaint=
            complaint

    )


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
