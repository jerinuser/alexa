from flask import Flask, request, render_template, send_file
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# Ensure upload and result directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def create_sketch(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted = 255 - gray_image

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(inverted, (15, 15), 0)

    # Invert the blurred image
    invertedblur = 255 - blur

    # Create a sketch by dividing the grayscale image by the inverted blurred image
    sketch = cv2.divide(gray_image, invertedblur, scale=220.0)

    # Apply adaptive thresholding for enhanced sketch effect
    adaptive_sketch = cv2.adaptiveThreshold(
        sketch, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
    )

    # Save the sketch image
    cv2.imwrite(output_path, adaptive_sketch)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            # Save the uploaded file
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(input_path)

            # Generate sketch
            output_path = os.path.join(app.config["RESULT_FOLDER"], "sketch_image.png")
            create_sketch(input_path, output_path)

            return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
