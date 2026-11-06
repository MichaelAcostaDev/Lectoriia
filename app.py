import os

from flask import Flask, jsonify, render_template, request

from ai_utils import answer_question, classify_text, extract_keywords, summarize_text
from pdf_utils import extract_pdf_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "Debes seleccionar un archivo PDF."}), 400

    try:
        data = extract_pdf_text(file)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "No se pudo procesar el PDF."}), 400

    return jsonify(
        {
            "file_name": data["file_name"],
            "page_count": data["page_count"],
            "text": data["text"],
            "pages": data["pages"],
            "size_bytes": data["size_bytes"],
        }
    )


@app.route("/api/summary", methods=["POST"])
def summary_endpoint():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Es necesario proporcionar texto para resumir."}), 400
    return jsonify(summarize_text(text))


@app.route("/api/keywords", methods=["POST"])
def keywords_endpoint():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Es necesario proporcionar texto para extraer palabras clave."}), 400
    return jsonify(extract_keywords(text))


@app.route("/api/classify", methods=["POST"])
def classify_endpoint():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Es necesario proporcionar texto para clasificar."}), 400
    return jsonify(classify_text(text))


@app.route("/api/analyze-text", methods=["POST"])
def analyze_text():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Debes introducir texto para analizar."}), 400

    return jsonify(
        {
            "summary": summarize_text(text),
            "keywords": extract_keywords(text),
            "classification": classify_text(text),
            "text_length": len(text),
        }
    )


@app.route("/api/ask-question", methods=["POST"])
def ask_question_route():
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()
    context = (payload.get("context") or payload.get("text") or "").strip()
    if not question:
        return jsonify({"error": "Debes escribir una pregunta."}), 400
    if not context:
        return jsonify({"error": "No hay texto base para responder."}), 400

    return jsonify(answer_question(question, context))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
