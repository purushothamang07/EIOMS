from modules.google_drive import list_templates
from flask import Flask, render_template, request, send_from_directory
import os

from modules.placeholder_reader import get_placeholders
from modules.word_generator import generate_word

app = Flask(__name__)

# -----------------------------
# Folder Settings
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_FOLDER = os.path.join(BASE_DIR, "word_templates")
GENERATED_FOLDER = os.path.join(BASE_DIR, "generated_reports")

os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    @app.route("/test_drive")
def test_drive():

    files = list_templates()

    return {
        "templates": files
    }
    return render_template("index.html")


# -----------------------------
# Select Template
# -----------------------------
@app.route("/generate_report")
def generate_report():

    templates = []

    for file in os.listdir(TEMPLATE_FOLDER):
        if file.endswith(".docx"):
            templates.append(file)

    templates.sort()

    return render_template(
        "select_template.html",
        templates=templates
    )


# -----------------------------
# Read Placeholders
# -----------------------------
@app.route("/select_template", methods=["POST"])
def select_template():

    filename = request.form["template"]

    filepath = os.path.join(TEMPLATE_FOLDER, filename)

    placeholders = get_placeholders(filepath)

    return render_template(
        "generate.html",
        placeholders=placeholders,
        template_path=filepath
    )


# -----------------------------
# Generate Word Report
# -----------------------------
# -----------------------------
# Generate Word Report
# -----------------------------
@app.route("/generate", methods=["POST"])
def generate():

    from datetime import datetime

    data = {}

    for key in request.form:

        value = request.form[key]

        # Convert HTML date (yyyy-mm-dd) to dd-mm-yyyy
        if "date" in key.lower() and value:
            try:
                value = datetime.strptime(
                    value,
                    "%Y-%m-%d"
                ).strftime("%d-%m-%Y")
            except:
                pass

        data[key] = value

    template = request.form["template_path"]

    letter_no = data.get("letter_no")

    if not letter_no:
        letter_no = "Report"

    output_file = f"VLR_{letter_no}.docx"

    output_path = os.path.join(
        GENERATED_FOLDER,
        output_file
    )

    generate_word(
        template,
        output_path,
        data
    )

    return render_template(
        "success.html",
        filename=output_file
    )

# -----------------------------
# Download Report
# -----------------------------
@app.route("/download/<filename>")
def download(filename):

    return send_from_directory(
        GENERATED_FOLDER,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)