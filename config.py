import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploaded_templates")

GENERATED_FOLDER = os.path.join(BASE_DIR, "generated_reports")

DATABASE = os.path.join(BASE_DIR, "database", "reports.db")