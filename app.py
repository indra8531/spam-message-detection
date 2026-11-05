"""
SpamShield AI - Flask Application & REST API
Provides real-time spam detection, model evaluation inspection, history persistence,
and contact handling with CORS enabled.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analyzer import analyze
import db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
METRICS_PATH = os.path.join(BASE_DIR, "models", "model_metrics.json")

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# Initialize database
db.init_db()


@app.route("/")
def serve_index():
    """Serves the main application landing page."""
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    """Serves static files (CSS, JS, assets)."""
    return send_from_directory(STATIC_DIR, path)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health and operational status endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "SpamShield AI Detection Service",
        "version": "1.0.0",
        "model_loaded": True
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    """Main message detection endpoint."""
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "")

        if not message or not str(message).strip():
            return jsonify({
                "success": False,
                "error": "Message cannot be empty. Please enter or paste text to analyze."
            }), 400

        # Perform analysis
        result = analyze(message)

        if not result.get("success", False):
            return jsonify(result), 400

        # Save to database history
        record_id = db.save_detection(result, message)
        result["history_id"] = record_id

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An internal error occurred during analysis: {str(e)}"
        }), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    """Fetches previously analyzed messages."""
    try:
        limit = request.args.get("limit", default=50, type=int)
        history = db.get_history(limit=limit)
        return jsonify({
            "success": True,
            "history": history,
            "count": len(history)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/history/<int:item_id>", methods=["GET"])
def get_history_detail(item_id):
    """Fetches detailed information for a single detection record."""
    try:
        item = db.get_history_item(item_id)
        if not item:
            return jsonify({"success": False, "error": "Record not found"}), 404
        return jsonify({"success": True, "record": item}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/history/<int:item_id>", methods=["DELETE"])
def delete_history_item(item_id):
    """Deletes a specific history record."""
    try:
        success = db.delete_history_item(item_id)
        if not success:
            return jsonify({"success": False, "error": "Item not found"}), 404
        return jsonify({"success": True, "message": "Record deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/history", methods=["DELETE"])
def clear_history():
    """Clears all detection history records."""
    try:
        db.clear_all_history()
        return jsonify({"success": True, "message": "History cleared successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/model-info", methods=["GET"])
def get_model_info():
    """Returns machine learning model metrics, parameters, and top features."""
    try:
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                metrics = json.load(f)
            return jsonify({"success": True, "metrics": metrics}), 200
        else:
            return jsonify({
                "success": False,
                "error": "Model metrics file not found. Please train the model."
            }), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns detection counters and performance stats."""
    try:
        stats = db.get_stats()
        return jsonify({"success": True, "stats": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/contact", methods=["POST"])
def contact():
    """Handles contact feedback form submissions."""
    try:
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "Name, email, and message are required fields."
            }), 400

        cid = db.save_contact(name, email, subject or "General Inquiry", message)
        return jsonify({
            "success": True,
            "message": "Thank you for reaching out! Your message has been received.",
            "submission_id": cid
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("SpamShield AI Server running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
