from flask import Flask, request, render_template, send_file
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__)
CORS(app)  # Allow frontend requests

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded!", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected!", 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        processed_path = os.path.join(PROCESSED_FOLDER, "cleaned_" + file.filename)

        file.save(file_path)  # Save original file

        # Remove metadata using PIL
        try:
            image = Image.open(file_path)
            data = list(image.getdata())  # Get image pixels
            image_without_metadata = Image.new(image.mode, image.size)
            image_without_metadata.putdata(data)

            # Save cleaned image
            image_without_metadata.save(processed_path)
            return send_file(processed_path, as_attachment=True)

        except Exception as e:
            return f"Error processing the file: {e}", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
