import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Lädt .env-Datei automatisch
load_dotenv()

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

def list_files(path='/'):
    try:
        response = requests.request(
            method='PROPFIND',
            url=f"{WEBDAV_URL}{path}",
            auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS),
            headers={"Depth": "1"},
        )
        if response.status_code == 207:
            return [
                line.split('<D:href>')[1].split('</D:href>')[0]
                for line in response.text.splitlines()
                if '<D:href>' in line and not line.endswith('/')
            ]
        else:
            return []
    except Exception as e:
        print(f"Fehler beim Listen: {e}")
        return []

def read_file(file_url):
    try:
        response = requests.get(file_url, auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASS))
        if response.status_code == 200:
            return response.text
        else:
            return ""
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        return ""

def search_files_for_keyword(path, keyword):
    files = list_files(path)
    matched = []
    for file_url in files:
        if file_url.endswith(".txt") or file_url.endswith(".md"):
            content = read_file(file_url)
            if keyword.lower() in content.lower():
                snippet_start = content.lower().find(keyword.lower())
                snippet = content[snippet_start:snippet_start+300]
                matched.append({
                    "file": file_url,
                    "match": snippet.strip()
                })
    return matched
