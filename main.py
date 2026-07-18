from flask import Flask, request, jsonify, send_file, render_template_string
import os
import uuid

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

HTML_PAGE = """
<!doctype html>
<html>
<head>
  <title>Share Files</title>
</head>
<body>
  <h2>Upload ZIP File</h2>
  <input type="file" id="fileInput" accept=".zip" />
  <button onclick="uploadFile()">Upload</button>
  <p id="result"></p>

  <h2>Files in Server</h2>
  <button onclick="loadFiles()">Refresh List</button>
  <ul id="fileList"></ul>

  <script>
    async function uploadFile() {
      const file = document.getElementById("fileInput").files[0];
      if (!file) {
        document.getElementById("result").innerText = "Choose a file first.";
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/api/files/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      document.getElementById("result").innerText =
        data.success ? "Uploaded. Saved as: " + data.saved_name : data.message;

      loadFiles();
    }

    async function loadFiles() {
      const res = await fetch("/api/files/list");
      const data = await res.json();

      const ul = document.getElementById("fileList");
      ul.innerHTML = "";

      data.files.forEach(f => {
        const li = document.createElement("li");
        li.innerHTML = `<a href="/api/files/${encodeURIComponent(f.name)}" target="_blank">${f.name}</a>`;
        ul.appendChild(li);
      });
    }

    loadFiles();
  </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


def unique_filename(original_name) -> str:
    base, ext = os.path.splitext(original_name)
    path = os.path.join(UPLOAD_DIR, original_name)

    if not os.path.exists(path):
        return original_name

    rand_id = uuid.uuid4().hex[:5]
    return f"{base}_{rand_id}{ext}"


@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file"}), 400

    f = request.files["file"]
    original_name = f.filename
    saved_name = unique_filename(original_name)
    path = os.path.join(UPLOAD_DIR, saved_name)
    f.save(path)

    return jsonify({"success": True, "saved_name": saved_name, "message": "uploaded"})


@app.route("/api/files/list", methods=["GET"])
def list_files():
    files = []
    for name in os.listdir(UPLOAD_DIR):
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
