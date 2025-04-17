import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/upload', methods = ["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename == "":
            return "No file selected"
        else:
            filename =secure_filename(uploaded_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(file_path)
            return f"File uploaded successfully: {filename}"

    return render_template("upload.html")

@app.route('/')
def hello():
    return "Link Vault Home Page"


if __name__ == '__main__':
    app.run(debug = True)