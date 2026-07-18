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
  <title>Share ZIP</title>
</head>
<body>
  <h2>Upload ZIP File</h2>
  <input type="file" id="fileInput" accept=".zip" />
  <button onclick="uploadFile()">Upload</button>
  <p id="result"></p>

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
        data.success ? "Uploaded. File ID: " + data.file_id : data.message;
    }
  </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file"}), 400

    f = request.files["file"]
    file_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{file_id}.zip")
    f.save(path)

    return jsonify({"success": True, "file_id": file_id, "message": "uploaded"})


@app.route("/api/files/<file_id>", methods=["GET"])
def download_file(file_id):
    path = os.path.join(UPLOAD_DIR, f"{file_id}.zip")
    if not os.path.exists(path):
        return jsonify({"success": False, "message": "Not found"}), 404

    return send_file(path, as_attachment=True, download_name=f"{file_id}.zip")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
