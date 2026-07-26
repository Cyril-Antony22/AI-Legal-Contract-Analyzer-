"""
PROJECT 1 - AI Legal Contract Analyzer (Part 1 - Flask Application)

This is the main application file. It wires together:
  Module 1 - Contract Upload
  Module 2 - OCR Processing        (modules/ocr_processor.py)
  Module 3 - AI Contract Analysis  (modules/ai_analyzer.py)
  Module 4 - Clause Identification (modules/ai_analyzer.py)
  Module 5 - Risk Analysis         (modules/ai_analyzer.py)
  Module 6 - AI Summary            (modules/ai_analyzer.py)
  Module 7 - AI Legal Chat         (modules/ai_analyzer.py)
  Module 8 - Export Report         (modules/report_generator.py)
  + a "Share Report" button that posts to Make.com (Part 2)
"""

import os
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, send_from_directory, jsonify, session
)
from config import Config
from modules.file_handler import allowed_file, save_upload
from modules.ocr_processor import extract_text_from_file
from modules.ai_analyzer import (
    generate_summary, extract_clauses, analyze_risks,
    extract_dates_and_parties, chat_about_contract
)
from modules.report_generator import generate_report
from modules.webhook_sender import send_report_to_make

app = Flask(__name__)
app.config.from_object(Config)

# ---------------------------------------------------------------------------
# In-memory "database" of analyzed contracts, keyed by contract_id.
# For a beginner project this is fine. For production, swap this for a
# real database (SQLite/Postgres) so data survives a server restart.
# ---------------------------------------------------------------------------
CONTRACTS = {}


@app.route("/")
def index():
    """Module 1 - Contract Upload page."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Handles the uploaded file end-to-end:
    save it -> OCR it -> run all AI analysis modules -> store results.
    """
    if "contract_file" not in request.files:
        flash("No file selected.")
        return redirect(url_for("index"))

    file = request.files["contract_file"]
    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Unsupported file type. Please upload a PDF, PNG, or JPG.")
        return redirect(url_for("index"))

    # Module 1 - save the upload
    contract_id, saved_path = save_upload(file)

    # Module 2 - OCR
    extracted_text = extract_text_from_file(saved_path)

    # Modules 3/4/5/6 - AI analysis (each call hits the OpenRouter API once)
    summary = generate_summary(extracted_text)
    clauses = extract_clauses(extracted_text)
    risks = analyze_risks(extracted_text)
    dates_parties = extract_dates_and_parties(extracted_text)

    CONTRACTS[contract_id] = {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "summary": summary,
        "clauses": clauses,
        "risks": risks,
        "dates_parties": dates_parties,
        "chat_history": [],
    }

    return redirect(url_for("results", contract_id=contract_id))


@app.route("/results/<contract_id>")
def results(contract_id):
    """Shows the summary, clauses, risks, and dates for one contract."""
    analysis = CONTRACTS.get(contract_id)
    if not analysis:
        flash("Contract not found. Please upload again.")
        return redirect(url_for("index"))
    return render_template("results.html", contract_id=contract_id, analysis=analysis)


@app.route("/chat/<contract_id>")
def chat_page(contract_id):
    """Module 7 - AI Legal Chat page."""
    analysis = CONTRACTS.get(contract_id)
    if not analysis:
        flash("Contract not found. Please upload again.")
        return redirect(url_for("index"))
    return render_template("chat.html", contract_id=contract_id, analysis=analysis)


@app.route("/chat/<contract_id>/ask", methods=["POST"])
def chat_ask(contract_id):
    """AJAX endpoint the chat page calls for every question the user asks."""
    analysis = CONTRACTS.get(contract_id)
    if not analysis:
        return jsonify({"error": "Contract not found"}), 404

    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "Empty question"}), 400

    answer = chat_about_contract(
        analysis["extracted_text"], analysis["chat_history"], question
    )

    analysis["chat_history"].append({"role": "user", "content": question})
    analysis["chat_history"].append({"role": "assistant", "content": answer})

    return jsonify({"answer": answer})


@app.route("/export/<contract_id>/<file_format>")
def export(contract_id, file_format):
    """Module 8 - Export Report as pdf / csv / json / txt."""
    analysis = CONTRACTS.get(contract_id)
    if not analysis:
        flash("Contract not found. Please upload again.")
        return redirect(url_for("index"))

    path = generate_report(
        analysis, Config.REPORT_FOLDER, contract_id, file_format
    )
    directory, name = os.path.split(path)
    return send_from_directory(directory, name, as_attachment=True)


@app.route("/share/<contract_id>", methods=["POST"])
def share(contract_id):
    """
    PART 2 bridge - the 'Share Contract Report' button.
    Sends the analysis to the Make.com webhook (see modules/webhook_sender.py).
    """
    analysis = CONTRACTS.get(contract_id)
    if not analysis:
        return jsonify({"ok": False, "error": "Contract not found"}), 404

    recipient_email = request.json.get("recipient_email", "")
    result = send_report_to_make(analysis, recipient_email, analysis["filename"])
    return jsonify(result)


if __name__ == "__main__":
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.REPORT_FOLDER, exist_ok=True)
    app.run(debug=True)
