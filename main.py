from flask import Flask, request, jsonify
from webdav_handler import upload_to_webdav, create_folder, read_file, list_files

app = Flask(__name__)

@app.route('/')
def index():
    return "Backbrain API is running."

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "pong"})

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    filename = data.get('filename')
    content = data.get('content')
    path = data.get('path', '/')
    if not filename or not content:
        return jsonify({"error": "filename and content are required"}), 400
    success = upload_to_webdav(filename, content, path)
    if success:
        return jsonify({"status": "success", "filename": filename})
    else:
        return jsonify({"status": "failed"}), 500

@app.route('/create-folder', methods=['POST'])
def create_folder_route():
    data = request.json
    path = data.get('path')
    if not path:
        return jsonify({"error": "Pfadangabe fehlt"}), 400
    try:
        success = create_folder(path)
        if success:
            return jsonify({"status": "success", "path": path})
        else:
            return jsonify({"status": "failed"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/list-files', methods=['GET'])
def list_files_route():
    path = request.args.get('path', '/')
    try:
        result = list_files(path)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/read-file', methods=['GET'])
def read_file_route():
    path = request.args.get('path', '/')
    filename = request.args.get('filename')
    try:
        content = read_file(path, filename)
        return content, 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)