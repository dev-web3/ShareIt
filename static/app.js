async function uploadFile() {
  const input = document.getElementById("fileInput");
  const file = input.files[0];
  const result = document.getElementById("result");

  if (!file) {
    result.textContent = "Choose a file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/files/upload", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  result.textContent = data.success
    ? `Uploaded successfully: ${data.saved_name}`
    : data.message || "Upload failed";

  if (data.success) {
    input.value = "";
  }

  loadFiles();
}

async function loadFiles() {
  const fileList = document.getElementById("fileList");
  fileList.innerHTML = "Loading...";

  const res = await fetch("/api/files/list");
  const data = await res.json();

  fileList.innerHTML = "";

  if (!data.files || data.files.length === 0) {
    fileList.innerHTML = "<p class='muted'>No files found.</p>";
    return;
  }

  data.files.forEach((f) => {
    const item = document.createElement("div");
    item.className = "file-item";
    item.innerHTML = `
      <span>${f.name}</span>
      <div class="actions">
        <a href="/api/files/${encodeURIComponent(f.name)}">Download</a>
        <button class="danger" onclick="deleteFile('${f.name}')">Delete</button>
      </div>
    `;
    fileList.appendChild(item);
  });
}

async function deleteFile(filename) {
  if (!confirm(`Delete ${filename}?`)) return;

  const res = await fetch(`/api/files/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });

  const data = await res.json();
  alert(data.message || "Done");
  loadFiles();
}

loadFiles();
