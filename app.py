import os
import tempfile

from flask import Flask, render_template, request, send_from_directory

from modules.google_drive import (
    list_templates,
    test_connection,
    download_template,
    get_template
)

from modules.placeholder_reader import get_placeholders
from modules.template_generator import generate_template


app = Flask(__name__)


# --------------------------------------------------
# Folder Settings
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GENERATED_FOLDER = os.path.join(
    BASE_DIR,
    "generated_reports"
)

os.makedirs(GENERATED_FOLDER, exist_ok=True)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# Test Google Drive
# --------------------------------------------------

@app.route("/test_drive")
def test_drive():

    result = test_connection()

    return result


# --------------------------------------------------
# Select Template
# --------------------------------------------------

@app.route("/generate_report")
def generate_report():

    try:

        templates = list_templates()

        # Only show DOCX and XLSX templates
        templates = [
            file for file in templates
            if file.get("name", "").lower().endswith(
                (".docx", ".xlsx")
            )
        ]

        # Sort templates alphabetically
        templates.sort(
            key=lambda x: x.get("name", "").lower()
        )

        return render_template(
            "select_template.html",
            templates=templates
        )

    except Exception as e:

        return f"""
        <h2>Google Drive Error</h2>
        <p>{str(e)}</p>
        """, 500


# --------------------------------------------------
# Select Template
# --------------------------------------------------

@app.route("/select_template", methods=["POST"])
def select_template():

    file_id = request.form.get("template")

    if not file_id:

        return "No template selected.", 400


    try:

        # Get selected Google Drive file information
        template_info = get_template(file_id)

        filename = template_info["name"]

        extension = os.path.splitext(
            filename
        )[1].lower()


        # Check file type
        if extension not in [".docx", ".xlsx"]:

            return "Unsupported template type.", 400


        # ------------------------------------------
        # Download template temporarily
        # ------------------------------------------

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        )

        temp_file.close()

        template_path = temp_file.name


        download_template(
            file_id,
            template_path
        )


        # ------------------------------------------
        # Read placeholders
        # ------------------------------------------

        placeholders = get_placeholders(
            template_path
        )


        # ------------------------------------------
        # Show input form
        # ------------------------------------------

        return render_template(
            "generate.html",
            placeholders=placeholders,
            template_id=file_id,
            template_name=filename
        )


    except Exception as e:

        return f"""
        <h2>Template Error</h2>
        <p>{str(e)}</p>
        """, 500


# --------------------------------------------------
# Generate Report
# --------------------------------------------------

@app.route("/generate", methods=["POST"])
def generate():

    from datetime import datetime

    data = {}


    # ----------------------------------------------
    # Read form data
    # ----------------------------------------------

    for key, value in request.form.items():

        if key == "template_id":
            continue

        if "date" in key.lower() and value:

            try:

                value = datetime.strptime(
                    value,
                    "%Y-%m-%d"
                ).strftime("%d-%m-%Y")

            except ValueError:

                pass


        data[key] = value


    # ----------------------------------------------
    # Get Google Drive template ID
    # ----------------------------------------------

    file_id = request.form.get(
        "template_id"
    )

    if not file_id:

        return "Template ID missing.", 400


    try:

        # ------------------------------------------
        # Get template information
        # ------------------------------------------

        template_info = get_template(
            file_id
        )

        template_name = template_info["name"]

        extension = os.path.splitext(
            template_name
        )[1].lower()


        # ------------------------------------------
        # Create temporary template file
        # ------------------------------------------

        temp_template = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        )

        temp_template.close()

        template_path = temp_template.name


        # Download template from Google Drive
        download_template(
            file_id,
            template_path
        )


        # ------------------------------------------
        # Output filename
        # ------------------------------------------

        letter_no = data.get(
            "letter_no",
            "Report"
        )


        # Remove invalid filename characters
        invalid_chars = r'\/:*?"<>|'

        for ch in invalid_chars:

            letter_no = letter_no.replace(
                ch,
                "_"
            )


        output_file = (
            f"VLR_{letter_no}{extension}"
        )


        output_path = os.path.join(
            GENERATED_FOLDER,
            output_file
        )


        # ------------------------------------------
        # Generate report
        # ------------------------------------------

        generate_template(
            template_path,
            output_path,
            data
        )


        # ------------------------------------------
        # Success page
        # ------------------------------------------

        return render_template(
            "success.html",
            filename=output_file
        )


    except Exception as e:

        return f"""
        <h2>Report Generation Error</h2>
        <p>{str(e)}</p>
        """, 500


# --------------------------------------------------
# Download Report
# --------------------------------------------------

@app.route("/download/<filename>")
def download(filename):

    return send_from_directory(
        GENERATED_FOLDER,
        filename,
        as_attachment=True
    )


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )