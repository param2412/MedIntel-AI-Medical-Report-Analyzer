"""MedIntel AI Flask Backend - PDF Upload, Extraction, and Analysis."""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from modules.utils.helper import setup_environment
from modules.ocr.pdf_extractor import extract_text_from_pdf, get_pdf_metadata
from modules.parser.medical_parser import parse_medical_report
# from modules.parser.medical_parser import parse_medical_report
from modules.rag.chatbot import answer_question_from_metrics
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "data/uploaded_reports"
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    """Check if file is an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "MedIntel AI Backend"
    }), 200


@app.route('/upload', methods=['POST'])
def upload_pdf():
    """
    Upload and process a medical PDF report.
    
    Expected: multipart/form-data with 'file' parameter
    Returns: JSON with raw text and parsed medical metrics
    """
    try:
        # Validate file presence
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided. Please upload a PDF file."
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "error": "No file selected."
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Invalid file type. Only PDF files are allowed."
            }), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(filepath)
        
        # Parse medical report
        parsed_report = parse_medical_report(extracted_text)
        
        # Get PDF metadata
        metadata = get_pdf_metadata(filepath)
        
        # Prepare response
        response = {
            "status": "success",
            "filename": filename,
            "filepath": filepath,
            "metadata": metadata,
            "raw_text": extracted_text[:500],  # First 500 chars preview
            "raw_text_length": len(extracted_text),
            "parsed_metrics": parsed_report.get("metrics", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except FileNotFoundError as e:
        return jsonify({
            "error": f"File processing error: {str(e)}"
        }), 400
    
    except Exception as e:
        return jsonify({
            "error": f"Upload failed: {str(e)}"
        }), 500


@app.route('/extract', methods=['POST'])
def extract_from_file():
    """
    Extract and parse text from an already uploaded PDF.
    
    Expected JSON: {"filepath": "path/to/file.pdf"}
    Returns: JSON with raw text and parsed metrics
    """
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        
        if not filepath:
            return jsonify({"error": "filepath parameter required"}), 400
        
        if not os.path.exists(filepath):
            return jsonify({"error": f"File not found: {filepath}"}), 404
        
        # Extract text
        extracted_text = extract_text_from_pdf(filepath)
        
        # Parse report
        parsed_report = parse_medical_report(extracted_text)
        
        response = {
            "status": "success",
            "filepath": filepath,
            "raw_text": extracted_text[:500],
            "raw_text_length": len(extracted_text),
            "parsed_metrics": parsed_report.get("metrics", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "error": f"Extraction failed: {str(e)}"
        }), 500


@app.route('/metrics', methods=['POST'])
def get_metrics():
    """
    Parse and extract medical metrics from uploaded PDF.
    
    Expected JSON: {"filepath": "path/to/file.pdf"}
    Returns: JSON with parsed medical metrics only
    """
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({"error": "Valid filepath required"}), 400
        
        # Extract and parse
        text = extract_text_from_pdf(filepath)
        parsed = parse_medical_report(text)
        
        return jsonify({
            "status": "success",
            "filepath": filepath,
            "metrics": parsed.get("metrics", {}),
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    """Entry point for the MedIntel AI backend."""
    setup_environment()
    print("✓ MedIntel AI backend initialized")
    print("Starting Flask server on http://localhost:5000")
    # When running under Streamlit the Flask reloader uses signals which
    # raise "signal only works in main thread". Disable debug and the
    # reloader to avoid signal calls when Streamlit executes this file.
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
