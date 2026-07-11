from flask import Flask, render_template, request, send_from_directory
import os

from modules.placeholder_reader import get_placeholders
from modules.word_generator import generate_word

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated_reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload")
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_template():

    file = request.files["template"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    placeholders = get_placeholders(filepath)

    app.config["CURRENT_TEMPLATE"] = filepath

    return render_template(
        "generate.html",
        placeholders=placeholders
    )


@app.route("/generate", methods=["POST"])
def generate():

    data = {}

    for key in request.form:
        data[key] = request.form[key]

    template = app.config["CURRENT_TEMPLATE"]

    letter_no = data.get("letter_no", "Report")

    output_file = f"VLR {letter_no}.docx"

    output_path = os.path.join(
        app.config["GENERATED_FOLDER"],
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


@app.route("/download/<filename>")
def download(filename):

    return send_from_directory(
        app.config["GENERATED_FOLDER"],
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)