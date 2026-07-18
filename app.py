from flask import Flask, request, jsonify, send_file, render_template
import os
import uuid

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def unique_filename(original_name):
    base, ext = os.path.splitext(original_name)
    path = os.path.join(UPLOAD_DIR, original_name)

    if not os.path.exists(path):
        return original_name

    rand_id = uuid.uuid4().hex[:5]
    return f"{base}_{rand_id}{ext}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file"}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"success": False, "message": "Empty filename"}), 400

    saved_name = unique_filename(f.filename)
    path = os.path.join(UPLOAD_DIR, saved_name)
    f.save(path)

    return jsonify({"success": True, "saved_name": saved_name})


@app.route("/api/files/list", methods=["GET"])
def list_files():
    files = []
    for name in sorted(os.listdir(UPLOAD_DIR)):
        path = os.path.join(UPLOAD_DIR, name)
        if os.path.isfile(path):
            files.append({"name": name})
    return jsonify({"success": True, "files": files})


@app.route("/api/files/<path:filename>", methods=["GET"])
def download_file(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"success": False, "message": "Not found"}), 404

    return send_file(path, as_attachment=True, download_name=filename)


@app.route("/api/files/<path:filename>", methods=["DELETE"])
def delete_file(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"success": False, "message": "Not found"}), 404

    os.remove(path)
    return jsonify({"success": True, "message": "Deleted", "filename": filename})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
