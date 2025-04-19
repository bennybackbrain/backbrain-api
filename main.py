from flask import Flask, request, jsonify
import requests
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# ENV-Variablen laden
load_dotenv()
WEBDAV_URL = os.getenv("WEBDAV_URL")
WEBDAV_USER = os.getenv("WEBDAV_USER")
WEBDAV_PASSWORD = os.getenv("WEBDAV_PASSWORD")

app = Flask(__name__)

# Datei-Upload (inkl. Ordner-Erstellung)
@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    filename = data.get("filename")
    content = data.get("content")
    path = data.get("path", "/")

    ensure_folder_exists(path)
    upload_url = f"{WEBDAV_URL.rstrip('/')}/{path.strip('/')}/{filename}"

    response = requests.put(
        upload_url,
        data=content.encode("utf-8"),
        auth=(WEBDAV_USER, WEBDAV_PASSWORD)
    )

    return jsonify({
        "status": "success" if response.status_code in [200, 201, 204] else "error",
        "code": response.status_code,
        "filename": filename,
        "url": upload_url
    })

# Ordner-Inhalt auflisten
@app.route("/list", methods=["GET"])
def list_files():
    path = request.args.get("path", "/")
    list_url = f"{WEBDAV_URL.rstrip('/')}/{path.strip('/')}"

    headers = {
        "Depth": "1",
        "Content-Type": "application/xml"
    }

    response = requests.request(
        "PROPFIND",
        list_url,
        headers=headers,
        auth=(WEBDAV_USER, WEBDAV_PASSWORD)
    )

    if not response.ok:
        return jsonify({"status": "error", "message": response.text}), response.status_code

    tree = ET.fromstring(response.text)
    items = []

    for resp in tree.findall("{DAV:}response"):
        href = resp.find("{DAV:}href").text
        name = href.strip("/").split("/")[-1]
        if name and name != path.strip("/"):
            items.append(name)

    return jsonify({"status": "success", "items": items})

# Datei-Inhalt lesen
@app.route("/read", methods=["GET"])
def read_file():
    path = request.args.get("path")
    if not path:
        return jsonify({"status": "error", "message": "Pfad fehlt"}), 400

    file_url = f"{WEBDAV_URL.rstrip('/')}/{path.strip('/')}"
    response = requests.get(file_url, auth=(WEBDAV_USER, WEBDAV_PASSWORD))

    if not response.ok:
        return jsonify({"status": "error", "message": response.text}), response.status_code

    return jsonify({
        "status": "success",
        "content": response.text
    })

# Ordner automatisch erstellen
def ensure_folder_exists(path):
    parts = path.strip("/").split("/")
    current_path = ""
    for part in parts:
        current_path += f"/{part}"
        folder_url = f"{WEBDAV_URL.rstrip('/')}/{current_path.strip('/')}/"
        response = requests.request(
            "MKCOL",
            folder_url,
            auth=(WEBDAV_USER, WEBDAV_PASSWORD)
        )
        # Fehler bei existierenden Ordnern (405) ignorieren

# Ping-Check
@app.route("/ping")
def ping():
    return "pong"

# Startpunkt
if __name__ == "__main__":
    app.run(debug=True)
