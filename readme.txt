# 🌱 CivicSense

## AI-Powered Smart Civic Complaint Management System

CivicSense is an AI-powered civic complaint management system designed to help citizens report and track common civic issues such as garbage, road damage, streetlight problems, water leakage, and drainage issues.

The system allows users to submit complaints with images and locations. AI-based image analysis helps identify the type of civic issue, while an interactive map helps visualize complaint locations.

---

##  Features

- 📋 Submit civic complaints
- 📸 Upload images of civic issues
- 🤖 AI-based image analysis
- 📍 Location selection and detection
- 🗺️ Interactive map using Leaflet.js
- 📌 Complaint location markers
- 📊 Complaint analytics dashboard
- 🍩 Complaint status visualization
- ⚡ Priority-based complaint management
- 📄 Complaint reports
- 👤 Admin dashboard
- ⚙️ Application settings
- 🔄 Complaint status tracking

---

## 🏙️ Civic Issues Supported

The system can be used to report issues such as:

- 🗑️ Garbage
- 🛣️ Road Damage
- 💡 Streetlight Problems
- 💧 Water Leakage
- 🚰 Drainage Issues
- ⚠️ Other Civic Issues

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript
- Leaflet.js
- Chart.js

### Backend
- Python
- Flask

### AI / Machine Learning
- YOLO
- Ultralytics

### Maps
- Leaflet.js
- OpenStreetMap

### Other Tools
- Git
- GitHub
- VS Code

---

## 📂 Project Structure

```text
CivicSense/
│
├── app.py
├── civic_model.pt
├── download_model.py
├── requirements.txt
├── readme.txt
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── add_complaint.html
│   ├── complaints.html
│   ├── map.html
│   ├── analytics.html
│   ├── reports.html
│   ├── settings.html
│   └── admin.html
│
├── uploads/
│
└── .venv/
