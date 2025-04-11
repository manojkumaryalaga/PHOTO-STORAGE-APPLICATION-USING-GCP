import os
from flask import Flask, request, render_template_string, Response
from google.cloud import storage
import google.generativeai as genai
from PIL import Image
import base64
import json
import io

# Initializing Flask app
app = Flask(__name__)

# Google Cloud setup
PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
# Initialize Google Cloud Storage client
storage_client = storage.Client(project=PROJECT_ID)

# Set Gemini API key here
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initializing the Gemini model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}

# Ensuring local files directory exists
os.makedirs('files', exist_ok=True)

# Function to check if the uploaded file is a valid image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to upload image to Google Cloud Storage
def upload_to_gcs(file):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)

# Function to generate description using Gemini AI
def generate_description(image):
    part = ["Give me a simple one line title and a one line of description for this Image", Image.open(image)]
    response = model.generate_content(part)
    print(response.text)
    l = response.text.split("\n")
    print(l, len(l))
    title, description = "", ""
    try:
        if len(l) == 3:
            title = l[0].split(":")[1]
            description = l[2].split(":")[1]
            print(title, description)
            upload_json(image, title, description)
        elif len(l) == 2:
            title = l[0].split(":")[1]
            description = l[1].split(":")[1]
            print(title, description)
            upload_json(image, title, description)
        elif len(l) == 4:
            title = l[2].split(":")[1]
            description = l[3].split(":")[1]
            print(title, description)
            upload_json(image, title, description)
        elif len(l) == 5:
            title = l[2].split(":")[1]
            description = l[4].split(":")[1]
            print(title, description)
            upload_json(image, title, description)
        elif len(l) == 6:
            title = l[2].split(":")[1]
            description = l[4].split(":")[1]
            print(title, description)
            upload_json(image, title, description)
        else:
            generate_description(image)
    except Exception as e:
        generate_description(image)
    print("-----")
    print(title, description)

def upload_json(image, title, description):
    dictionary = {"title": title, "description": description}
    json_object = json.dumps(dictionary, indent=4)

    with open(image.filename.rsplit(".", 1)[0] + ".json", "w") as outfile:
        outfile.write(json_object)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(image.filename.rsplit(".", 1)[0] + ".json")
    blob.upload_from_filename(image.filename.rsplit(".", 1)[0] + ".json")
    os.remove(image.filename.rsplit(".", 1)[0] + ".json")

# Function to save metadata JSON to Cloud Storage
def save_metadata(filename, metadata):
    json_filename = filename.rsplit(".", 1)[0] + ".json"
    json_blob = storage_client.bucket(BUCKET_NAME).blob(json_filename)
    json_blob.upload_from_string(json.dumps(metadata), content_type="application/json")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]

        # Upload image to Cloud Storage
        upload_to_gcs(file)

        # Generate title & description using Gemini AI
        generate_description(file)

    html = f"""
        <html>
        <body style='background-color: white; color: black;'>
            <h2>Upload an Image for Captioning</h2>
            <form method="post" enctype="multipart/form-data">
                <label for="file">Choose an image (JPEG/PNG):</label>
                <input type="file" name="file" accept="image/jpeg, image/png" required />
                <br />
                <button type="submit">Upload</button>
            </form>
            <br />
            <h3>Uploaded Images:</h3>
            <div style="color: white;">
    """

    l = fetchallfiles()
    for i in l:
        html += f" <a href='/files/{i}' style='color: white; text-decoration: underline;'>{i}</a><br>"

    html += """
        </div>
        </body>
        </html>
    """
    return html


@app.route("/files/<filename>")
def fetchfile(filename):
    file_name = filename
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename.rsplit(".", 1)[0] + ".json")
    file_content = None
    with blob.open("r") as obj:
        file_content = obj.read()
    file_content = json.loads(file_content)
    title = file_content["title"]
    description = file_content["description"]
    html = f"""
    <h1>{file_name} </h1>
    <img src='/images/{file_name}' width="25%">
    <p>title:{title}</p>
    <p>description:{description}</p>
    """
    return html

@app.route("/images/<imagename>")
def images(imagename):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(imagename)
    data = blob.download_as_bytes()
    return Response(io.BytesIO(data), mimetype="image/jpeg")

def fetchallfiles():
    l = list()
    images = storage_client.list_blobs(BUCKET_NAME)
    for i in images:
        if i.name.lower().endswith(".jpeg") or i.name.lower().endswith(".png") or i.name.lower().endswith(".jpg"):
            l.append(i.name)
    return l

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
