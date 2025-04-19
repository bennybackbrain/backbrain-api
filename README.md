# BackBrain API

Diese API verbindet deine Custom GPT mit deiner Nextcloud via WebDAV. Sie erlaubt:
- Auflisten von `.txt` und `.md` Dateien
- Durchsuchen dieser Dateien nach Stichwörtern
- Rückgabe der Treffer als Kontext für GPT-Antworten

## Endpunkt
GET /search-files?query=begriff

## .env-Variablen
- NEXTCLOUD_USERNAME
- NEXTCLOUD_PASSWORD
- WEBDAV_URL