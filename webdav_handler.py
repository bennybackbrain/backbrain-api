import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
import os

WEBDAV_URL = os.getenv("WEBDAV_URL", "https://nx69869.your-storageshare.de/remote.php/dav/files/chatgpt_sync/benny_gpt/")
USERNAME = os.getenv("NEXTCLOUD_USERNAME")
PASSWORD = os.getenv("NEXTCLOUD_PASSWORD")

def list_files():
    headers = {"Depth": "1"}
    response = requests.request("PROPFIND", WEBDAV_URL, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    tree = ElementTree.fromstring(response.content)

    files = []
    for resp in tree.findall("{DAV:}response"):
        href = resp.find("{DAV:}href").text
        if href.endswith(".md") or href.endswith(".txt"):
            filename = href.split("/")[-1]
            if filename:
                files.append(filename)
    return files

def read_file(filename):
    url = WEBDAV_URL + filename
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.text
    return None