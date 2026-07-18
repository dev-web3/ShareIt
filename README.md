# ShareIt - File Share App

A simple Flask-based local file sharing app for uploading, listing, downloading, and deleting ZIP files through a web page and API.

## Features

- Upload ZIP files from browser
- View all uploaded files
- Download files from the UI
- Delete files from the UI
- Keeps original filename
- If same filename exists, appends 5 random characters before extension
- Separate HTML, CSS, and JavaScript files
- Simple REST API endpoints

## Tech Stack

- Python 3
- Flask
- HTML
- CSS
- JavaScript

## Project Structure

```text
project/
├── app.py
├── requirements.txt
├── uploads/
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Setup

### 1. Clone or copy the project
Put all files in one folder.

### 2. Create a virtual environment

``` bash
uv sync -U
```

### 3. Run the App

```bash
uv run app.py
```

By default, the app runs on:

```bash
http://0.0.0.0:5000
```

Open in browser:

```bash
http://localhost:5000
```

## API Endpoints

### Home Page

```http
GET /
```

### Upload File

```http
POST /api/files/upload
```
Form-data:

 - file = ZIP file

### List Files

```http
GET /api/files/list
```

### Download File

```http
GET /api/files/<filename>
```

### Delete File

```http
DELETE /api/files/<filename>
```

## Usage

 - Open the web page in browser
 - Choose a ZIP file
 - Click Upload
 - View files in the list
 - Download or delete files as needed

## Notes

 - This app is intended for local network or personal machine usage
 - Uploaded files are saved inside the uploads/ folder
 - If a file with the same name already exists, a short random suffix is added

## Examples

### Upload with curl

```bash
curl -X POST http://127.0.0.1:5000/api/files/upload \\
  -F "file=@data.zip"
```

### List Files

```bash
curl http://127.0.0.1:5000/api/files/list
```

### Delete File

```bash
curl -X DELETE http://127.0.0.1:5000/api/files/example.zip
```

## Future Improvements
 - File size limit
 - Better security
 - Authentication
 - Folder upload support
 - Progress bar for uploads
 - Drag and drop upload
 - File metadata storage in database