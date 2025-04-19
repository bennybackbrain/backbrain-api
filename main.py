from flask import Flask, request, jsonify
from webdav_handler import upload_to_webdav, search_files_for_keyword

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

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    path = request.args.get('path', '/benny_gpt/')

    if not keyword:
        return jsonify({"error": "keyword is required"}), 400

    results = search_files_for_keyword(path, keyword)
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
