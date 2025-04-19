# BackBrain API (Vollständig & Automatisch)

Diese API durchsucht `.txt` und `.md` Dateien im Nextcloud-Ordner `benny_gpt`
nach Stichwörtern und liefert Treffer kontextbezogen zurück.

## Funktionsweise:
- Listet alle relevanten Dateien (WebDAV)
- Durchsucht Inhalt zeilenweise
- Gibt Fundstellen + Kontext aus

## Aufruf (nach Deployment bei Render.com):
GET /search-files?query=deinbegriff

## Setup-Hinweis:
- Nutze die `.env`-Datei für Zugangsdaten
- Startbefehl ist automatisiert über `start.sh`