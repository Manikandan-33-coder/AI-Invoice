from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from extractor import extract_invoice_data

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf","png","jpg","jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process_invoice", methods=["POST"])
def process_invoice():
    if "file" not in request.files:
        return jsonify({"error":"No file uploaded"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error":"No file selected"})
    if not allowed_file(file.filename):
        return jsonify({"error":"Only PDF/PNG/JPG allowed"})
    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    data = extract_invoice_data(path)
    return jsonify(data)

@app.route("/save_invoice", methods=["POST"])
def save_invoice():
    data = request.json
    print("Invoice Saved:", data)
    return jsonify({"message":"Invoice saved successfully"})

if __name__ == "__main__":
    app.run(debug=True)