SMART CIVIC SENSE
==================

HACKATHON PROTOTYPE


PROJECT STRUCTURE
-----------------

Smart Civic Sense/

    app.py

    civic_model.pt

    requirements.txt

    templates/

        index.html

        add_complaint.html

        complaints.html

        map.html

    static/

        style.css

    uploads/

    .venv/


INSTALLATION
------------

Open terminal inside:

C:\Smart Civic Sense


Activate virtual environment:

.venv\Scripts\activate


Install libraries:

pip install -r requirements.txt


RUN
---

python app.py


Open browser:

http://127.0.0.1:5000


FEATURES
--------

1. CivicSense Dashboard

2. Add Civic Complaint

3. Image Upload

4. AI Image Analysis

5. AI Confidence

6. Severity Detection

7. Priority Score

8. Priority Classification

9. Manual Location Search

10. Browser Location

11. Leaflet Map

12. Complaint Submission

13. Complaint ID Generation

14. Complaint List

15. Complaint Status Update

16. Complaint Map


IMPORTANT
---------

Keep civic_model.pt in the project root.

The model file is required for AI image analysis.


NOTE
----

This hackathon prototype stores complaints
temporarily in memory.

Restarting Flask will remove newly
submitted complaints.