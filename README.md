# Backbrain API (Flask-Version)

Eine einfache API zum Speichern und Durchsuchen von Dateien in Nextcloud (WebDAV).

## Endpunkte

- `POST /upload`: Datei mit Inhalt an WebDAV senden
- `GET /search?keyword=...`: Alle Dateien nach Begriff durchsuchen
- `GET /ping`: Verbindungstest

## .env-Konfiguration

Erstelle eine `.env`-Datei mit folgendem Inhalt:

WEBDAV_URL=https://nx69869.your-storageshare.de/remote.php/dav/files/chatgpt_sync/
WEBDAV_USER=chatgpt_sync
WEBDAV_PASS=HIER_DEIN_PASSWORT
