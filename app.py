import hmac
import logging
import os
import re
from typing import Any

from flask import Flask, jsonify, make_response, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from ai_utils import (
    AIServiceError,
    answer_question,
    analyze_document,
    classify_text,
    extract_keywords,
    get_hf_token,
    has_hf_token,
    summarize_text,
    _call_chat,
)
from pdf_utils import PDFProcessingError, extract_pdf_text

logger = logging.getLogger(__name__)
app = Flask(__name__)
REQUEST_LIMIT_BYTES = 4_500_000 if os.getenv("VERCEL") else 15 * 1024 * 1024
app.config["MAX_CONTENT_LENGTH"] = REQUEST_LIMIT_BYTES


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


def _adsense_client_id() -> str:
    publisher_id = os.getenv("ADSENSE_PUBLISHER_ID", "").strip()
    match = re.fullmatch(r"(?:ca-)?pub-(\d+)", publisher_id)
    return f"ca-pub-{match.group(1)}" if match else ""


def _adsense_slot_config() -> dict[str, str]:
    return {
        key: value
        for key, value in {
            "hero": os.getenv("ADSENSE_SLOT_HERO", "").strip(),
            "middle": os.getenv("ADSENSE_SLOT_MIDDLE", "").strip(),
            "sidebar": os.getenv("ADSENSE_SLOT_SIDEBAR", "").strip(),
            "footer": os.getenv("ADSENSE_SLOT_FOOTER", "").strip(),
        }.items()
        if re.fullmatch(r"\d{1,30}", value)
    }


def _privacy_contact_email() -> str:
    email = os.getenv("PRIVACY_CONTACT_EMAIL", "").strip()
    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return email
    return ""


@app.route("/")
def index():
    locale = request.accept_languages.best_match(["es", "en"], default="en")
    publisher_id = _adsense_client_id()
    ad_slots = _adsense_slot_config()
    auto_ads = os.getenv("ADSENSE_AUTO_ADS", "").strip().lower() in {"1", "true", "yes"}
    return render_template(
        "index.html",
        initial_locale=locale,
        adsense_config={
            "publisherId": publisher_id,
            "slots": ad_slots,
            "autoAds": auto_ads,
        },
        show_development_ads=not bool(os.getenv("VERCEL")),
    )


@app.route("/privacy")
def privacy():
    locale = request.accept_languages.best_match(["es", "en"], default="en")
    return render_template(
        "privacy.html",
        locale=locale,
        contact_email=_privacy_contact_email(),
    )


@app.route("/ads.txt")
def ads_txt():
    publisher_id = _adsense_client_id()
    if not publisher_id:
        logger.warning("ads.txt requested without a valid AdSense publisher ID")
        response = make_response("AdSense publisher ID is not configured.\n", 404)
        response.mimetype = "text/plain"
        response.headers["Cache-Control"] = "no-store"
        return response
    response = make_response(
        f"google.com, {publisher_id.removeprefix('ca-')}, DIRECT, f08c47fec0942fa0\n"
    )
    response.mimetype = "text/plain"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "application": "operational",
            "ai": {
                "credentials_configured": has_hf_token(),
                "provider_reachable": "not_checked",
                "model_operational": "not_checked",
            },
        }
    )


@app.route("/api/health/ai", methods=["POST"])
def ai_health():
    token = get_hf_token()
    if not token:
        return jsonify(
            {
                "application": "operational",
                "ai": {
                    "credentials_configured": False,
                    "provider_reachable": "not_checked",
                    "model_operational": "not_checked",
                },
                "error_code": "missing_token",
            }
        ), 503
    authorization = request.headers.get("Authorization", "").encode("utf-8")
    expected_authorization = f"Bearer {token}".encode("utf-8")
    if not hmac.compare_digest(authorization, expected_authorization):
        return jsonify({"error": "Valid health-check authorization is required."}), 401

    try:
        answer = _call_chat(
            [
                {
                    "role": "system",
                    "content": "Reply with exactly the word OK and nothing else.",
                },
                {"role": "user", "content": "Connection health check."},
            ],
            max_tokens=8,
        )
    except AIServiceError as error:
        logger.warning("AI health check failed (code=%s)", error.code)
        provider_reachable = (
            "unknown"
            if error.code in {"provider_timeout", "provider_unavailable"}
            else True
        )
        model_operational = (
            "unknown"
            if provider_reachable == "unknown"
            else False
        )
        return jsonify(
            {
                "application": "operational",
                "ai": {
                    "credentials_configured": True,
                    "provider_reachable": provider_reachable,
                    "model_operational": model_operational,
                },
                "error_code": error.code,
            }
        ), error.status_code

    model_operational = answer.strip().casefold() == "ok"
    return jsonify(
        {
            "application": "operational",
            "ai": {
                "credentials_configured": True,
                "provider_reachable": True,
                "model_operational": model_operational,
            },
        }
    ), 200 if model_operational else 502


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
                "error": "The request exceeds the configured upload limit.",
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
