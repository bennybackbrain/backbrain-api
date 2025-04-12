import requests
from requests.auth import HTTPBasicAuth
import os
import xml.etree.ElementTree as ET

WEBDAV_URL = os.getenv("WEBDAV_URL")
WEBDAV_USER = os.getenv("WEBDAV_USER")
WEBDAV_PASS = os.getenv("WEBDAV_PASS")

def upload_to_webdav(filename, content, path='/'):
    try:
        full_url = f"{WEBDAV_URL}{path.strip('/')}/{filename}"
        response = requests.put(
            full_url,
            data=content.encode('utf-8'),
            auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS)
        )
        return response.status_code in [200, 201, 204]
    except Exception as e:
        print(f"Upload failed: {e}")
        return False

def create_folder(path='/'):
    try:
        full_url = f"{WEBDAV_URL}{path.strip('/')}/"
        response = requests.request(
            method="MKCOL",
            url=full_url,
            auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS)
        )
        return response.status_code in [200, 201, 204]
    except Exception as e:
        print(f"Ordnererstellung fehlgeschlagen: {e}")
        return False

def list_files(path='/'):
    url = f"{WEBDAV_URL}{path.strip('/')}/"
    headers = {"Depth": "1"}
    response = requests.request("PROPFIND", url, headers=headers, auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS))
    if response.status_code != 207:
        raise Exception(f"Fehler beim Abrufen der Dateiliste: {response.status_code}")
    return response.text

def read_file(path, filename):
    full_path = f"{WEBDAV_URL}{path.strip('/')}/{filename}"
    response = requests.get(full_path, auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS))
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Fehler beim Lesen der Datei: {response.status_code}")