"""
Zarai Saathi — Flask/OpenCV backend.
Local demo backend for agricultural advisory and crop-image screening.
Image color analysis is heuristic only and must not be treated as a confirmed diagnosis.
"""
import os
import uuid
from pathlib import Path
from backend import app

# Vercel serverless WSGI handler entrypoint
def handler(environ, start_response):
    return app(environ, start_response)

import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB upload limit
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

def analyze_leaf_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "Invalid or unreadable image. Please upload a JPG, PNG, WEBP, or BMP file."}
        img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green, upper_green = np.array([35, 40, 40]), np.array([85, 255, 255])
        lower_yellow, upper_yellow = np.array([10, 40, 40]), np.array([34, 255, 255])
        green = cv2.countNonZero(cv2.inRange(hsv, lower_green, upper_green))
        yellow = cv2.countNonZero(cv2.inRange(hsv, lower_yellow, upper_yellow))
        total = img.shape[0] * img.shape[1]
        green_ratio, infection_ratio = green / total * 100, yellow / total * 100

        if green_ratio > 55 and infection_ratio < 5:
            severity = "Healthy-looking"
            diagnosis = "The image is predominantly green with limited yellow pixels."
            treatment = "Continue routine scouting and follow local crop-management guidance."
        elif infection_ratio > 15:
            severity = "High visual symptom signal"
            diagnosis = "A high proportion of yellow pixels was detected; this can reflect disease, nutrient stress, aging, or lighting."
            treatment = "Inspect several plants and consult an agriculture extension officer before choosing a treatment."
        elif infection_ratio > 6:
            severity = "Moderate visual symptom signal"
            diagnosis = "Some yellow pixels were detected; causes may include nutrient or water stress, disease, or lighting."
            treatment = "Check leaf undersides, soil moisture, and nearby plants; seek local expert confirmation."
        else:
            severity = "Low visual symptom signal"
            diagnosis = "The color heuristic found limited yellow pixels; this does not rule out disease."
            treatment = "Continue monitoring and compare with a clear close-up photo and local expert guidance."

        return {
            "status": "success",
            "green_percentage": round(green_ratio, 2),
            "infection_percentage": round(infection_ratio, 2),
            "severity": severity,
            "diagnosis": diagnosis,
            "recommended_treatment": treatment,
            "region": "Sindh Agro-Zone",
            "disclaimer": "Color-based screening only; not a validated disease classifier or confirmed diagnosis."
        }
    except Exception:
        app.logger.exception("Image analysis failed")
        return {"error": "Image analysis failed. Please try another image."}

@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Image is too large. Maximum upload size is 8 MB."}), 413

@app.get("/api/health")
def health_check():
    return jsonify({
        "status": "online",
        "service": "Zarai Saathi CV & agricultural advisory backend",
        "modes_supported": ["OpenCV color heuristic", "rule-based agricultural advisory"]
    })

@app.post("/api/diagnose")
def diagnose_crop():
    if "file" not in request.files:
        return jsonify({"error": "No image file was provided (expected field name: file)."}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Please choose an image first."}), 400
    ext = Path(secure_filename(file.filename)).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file type. Use JPG, JPEG, PNG, WEBP, or BMP."}), 415
    filepath = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}{ext}")
    try:
        file.save(filepath)
        result = analyze_leaf_image(filepath)
        return jsonify(result), (400 if result.get("error") else 200)
    finally:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except OSError:
            app.logger.warning("Could not remove temporary upload")

@app.post("/api/chat")
def chat_ai_json():
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", "")).strip().lower()
    if not query:
        return jsonify({"status": "error", "message": "Please enter a question."}), 400

    if any(term in query for term in ("locust", "تڈی", "pest", "whitefly", "کیڑا", "insect")):
        payload = {
            "status": "success", "topic": "Pest scouting and control",
            "recommendation": "Identify the pest and assess how much of the field is affected before selecting a control. Use only a locally registered product according to its label; avoid spraying in wind and protect pollinators. Contact your District Agriculture Extension Officer for a field-specific recommendation.",
            "action_items": ["Inspect both sides of leaves and check several plants", "Record the affected area and crop stage", "Confirm product choice, dose, and pre-harvest interval with local extension staff"]
        }
    elif any(term in query for term in ("wheat", "گندم", "fertilizer", "urea", "dap")):
        payload = {
            "status": "success", "topic": "Wheat fertilizer and irrigation",
            "recommendation": "Fertilizer needs vary with soil test, variety, sowing date, and previous crop. Use soil-test recommendations and local Agriculture Extension guidance; avoid applying fertilizer immediately before heavy runoff or over-irrigation.",
            "action_items": ["Check crop stage and soil moisture", "Use a soil test where available", "Confirm rates for your district with an extension officer"]
        }
    elif any(term in query for term in ("water", "irrigation", "پانی", "tube well", "canal")):
        payload = {
            "status": "success", "topic": "Water and irrigation planning",
            "recommendation": "Irrigation timing depends on crop stage, soil texture, recent weather, and canal availability. Check root-zone moisture and avoid waterlogging; coordinate with the local Warabandi schedule.",
            "action_items": ["Inspect soil moisture at root depth", "Check field drainage and canal schedule", "Reassess after rainfall or extreme heat"]
        }
    elif any(term in query for term in ("price", "rate", "mandi", "market", "بھاؤ")):
        payload = {
            "status": "success", "topic": "Mandi price comparison",
            "recommendation": "Compare at least three current buyer offers and verify grade, moisture, weighing method, transport cost, payment timing, and any commission. The prices shown in this demo dashboard are illustrative and should not be treated as official live rates.",
            "action_items": ["Ask buyers for a written price and grade", "Compare net proceeds after transport and fees", "Keep a receipt and payment record"]
        }
    else:
        payload = {
            "status": "success", "topic": "General Sindh agricultural advisory",
            "recommendation": "For a more useful recommendation, include your district, crop, crop stage, visible symptoms, irrigation source, and recent treatment. Confirm high-impact decisions with a local Agriculture Extension Officer.",
            "action_items": ["Monitor the field regularly", "Keep dated crop-health notes", "Use locally verified weather and market information"]
        }
    payload["disclaimer"] = "This demo provides general information, not official government advice. Verify local recommendations before acting."
    return jsonify(payload)

if __name__ == "__main__":
    print(f"Zarai Saathi backend starting from {BASE_DIR}")
    print("Health check: http://127.0.0.1:5000/api/health")
    app.run(host="127.0.0.1", port=5000, debug=False)
