import logging
import os
import re
from typing import Any

from flask import Flask, abort, jsonify, make_response, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from ai_utils import (
    AIServiceError,
    answer_question,
    analyze_document,
    classify_text,
    extract_keywords,
    summarize_text,
)
from pdf_utils import PDFProcessingError, extract_pdf_text

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024


def _json_payload() -> dict[str, Any]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise AIServiceError("A JSON request body is required.", "invalid_request", 400)
    return payload


def _document_arguments(payload: dict[str, Any]) -> tuple[str, list[str] | None]:
    text = payload.get("text", "")
    pages = payload.get("pages")
    if not isinstance(text, str):
        raise AIServiceError("Document text must be a string.", "invalid_request", 400)
    if pages is not None and (
        not isinstance(pages, list) or any(not isinstance(page, str) for page in pages)
    ):
        raise AIServiceError("Document pages must be a list of text.", "invalid_request", 400)
    return text.strip(), pages


@app.route("/")
def index():
    locale = request.accept_languages.best_match(["es", "en"], default="en")
    publisher_id = os.getenv("ADSENSE_PUBLISHER_ID", "").strip()
    if not re.fullmatch(r"ca-pub-\d+", publisher_id):
        publisher_id = ""
    ad_slots = {
        key: value
        for key, value in {
            "hero": os.getenv("ADSENSE_SLOT_HERO", ""),
            "middle": os.getenv("ADSENSE_SLOT_MIDDLE", ""),
            "sidebar": os.getenv("ADSENSE_SLOT_SIDEBAR", ""),
            "footer": os.getenv("ADSENSE_SLOT_FOOTER", ""),
        }.items()
        if value.isdigit()
    }
    return render_template(
        "index.html",
        initial_locale=locale,
        adsense_config={"publisherId": publisher_id, "slots": ad_slots},
        show_development_ads=not bool(os.getenv("VERCEL")),
    )


@app.route("/ads.txt")
def ads_txt():
    publisher_id = os.getenv("ADSENSE_PUBLISHER_ID", "").strip()
    if not re.fullmatch(r"ca-pub-\d+", publisher_id):
        abort(404)
    response = make_response(
        f"google.com, {publisher_id.removeprefix('ca-')}, DIRECT, f08c47fec0942fa0\n"
    )
    response.mimetype = "text/plain"
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    file = request.files.get("file")
    if not file or file.filename == "":
        raise PDFProcessingError("Select a PDF file first.", "missing_file", 400)
    data = extract_pdf_text(file)
    return jsonify(data)


@app.route("/api/summary", methods=["POST"])
def summary_endpoint():
    payload = _json_payload()
    text, pages = _document_arguments(payload)
    return jsonify(summarize_text(text, pages))


@app.route("/api/keywords", methods=["POST"])
def keywords_endpoint():
    payload = _json_payload()
    text, pages = _document_arguments(payload)
    return jsonify(extract_keywords(text, pages=pages))


@app.route("/api/classify", methods=["POST"])
def classify_endpoint():
    payload = _json_payload()
    text, pages = _document_arguments(payload)
    return jsonify(classify_text(text, pages))


@app.route("/api/analyze-text", methods=["POST"])
def analyze_text():
    payload = _json_payload()
    text, pages = _document_arguments(payload)
    return jsonify(analyze_document(text, pages))


@app.route("/api/ask-question", methods=["POST"])
def ask_question_route():
    payload = _json_payload()
    question = payload.get("question", "")
    context = payload.get("context", payload.get("text", ""))
    history = payload.get("history", [])
    pages = payload.get("pages")
    if not isinstance(question, str) or not isinstance(context, str):
        raise AIServiceError("Question and document text must be strings.", "invalid_request", 400)
    if not isinstance(history, list):
        raise AIServiceError("Conversation history must be a list.", "invalid_request", 400)
    if pages is not None and (
        not isinstance(pages, list) or any(not isinstance(page, str) for page in pages)
    ):
        raise AIServiceError("Document pages must be a list of text.", "invalid_request", 400)
    return jsonify(answer_question(question, context, history, pages))


@app.errorhandler(AIServiceError)
def handle_ai_error(error: AIServiceError):
    if error.status_code >= 500:
        logger.warning("AI request failed (code=%s)", error.code)
    return jsonify({"error": str(error), "code": error.code}), error.status_code


@app.errorhandler(PDFProcessingError)
def handle_pdf_error(error: PDFProcessingError):
    return jsonify({"error": str(error), "code": error.code}), error.status_code


@app.errorhandler(RequestEntityTooLarge)
def handle_request_too_large(error: RequestEntityTooLarge):
    logger.info("Rejected request over upload limit (status=%s)", error.code)
    return (
        jsonify(
            {
                "error": "The request exceeds the 15 MB upload limit.",
                "code": "request_too_large",
            }
        ),
        413,
    )


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "").lower() == "true",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
    )
