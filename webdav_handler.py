import requests
from requests.auth import HTTPBasicAuth
import os

# Hole Zugangsdaten aus Umgebungsvariablen (kannst du später in Render setzen)
WEBDAV_URL = os.getenv("WEBDAV_URL")
WEBDAV_USER = os.getenv("WEBDAV_USER")
WEBDAV_PASS = os.getenv("WEBDAV_PASS")

def upload_to_webdav(filename, content, path='/'):
    try:
        full_url = f"{WEBDAV_URL}{path}{filename}"
        response = requests.put(
            full_url,
            data=content.encode('utf-8'),
            auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS)
        )
        return response.status_code in [200, 201, 204]
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
