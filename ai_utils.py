import os
import re
from collections import Counter

import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
DEFAULT_SUMMARY_MODEL = os.getenv("HF_SUMMARY_MODEL", "facebook/bart-large-cnn")
DEFAULT_QA_MODEL = os.getenv("HF_QA_MODEL", "deepset/roberta-base-squad2")
DEFAULT_KEYWORDS_MODEL = os.getenv("HF_KEYWORDS_MODEL", "ml6team/keyphrase-extraction-kbir-inspec")
DEFAULT_CLASSIFICATION_MODEL = os.getenv(
    "HF_CLASSIFICATION_MODEL",
    "cardiffnlp/twitter-xlm-roberta-base-sentiment"
)

SPANISH_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "de", "del",
    "al", "por", "para", "con", "sin", "sobre", "entre", "como", "más", "muy", "pero",
    "porque", "cuando", "donde", "que", "qué", "quien", "quién", "sus", "este", "esta",
    "estos", "estas", "ese", "esa", "esos", "esas", "año", "años", "ser", "estar",
    "tener", "también", "hace", "hacer", "desde", "hasta", "todos", "todas", "menos",
    "a", "en", "se", "si", "no", "sí", "es", "son", "fue", "fueron", "ha", "han", "hay",
    "tras", "durante", "según", "mediante", "cada", "mismo", "misma", "después"
}

ENGLISH_STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "with", "without", "from", "into",
    "in", "on", "at", "of", "to", "is", "are", "was", "were", "be", "been",
    "being", "this", "that", "these", "those", "as", "by", "it", "its", "their",
    "they", "them", "he", "she", "we", "you", "our", "your", "us", "not", "but",
    "also", "more", "most", "very", "have", "has", "had", "can", "could", "should",
    "would", "will", "about", "after", "before", "during", "under", "over", "then",
    "there", "here", "through", "which", "what", "when", "where", "who", "why", "how"
}
STOPWORDS = SPANISH_STOPWORDS | ENGLISH_STOPWORDS

POSITIVE_WORDS = {
    "excelente", "positiva", "positivo", "bueno", "mejor", "eficaz", "claridad", "feliz",
    "satisfactorio", "apoyo", "beneficio", "ganancia", "mejora", "solución", "estable",
    "success", "good", "great", "positive", "effective", "clear", "benefit", "improvement"
}
NEGATIVE_WORDS = {
    "malo", "negativo", "problema", "peligro", "error", "defecto", "fallo", "riesgo",
    "limitado", "frustrante", "inconveniente", "dificultad", "pérdida", "costoso", "bad",
    "negative", "problem", "risk", "issue", "fail", "broken", "limited", "frustrating"
}


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    return text


def split_text_chunks(text: str, max_chars: int = 1800) -> list[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []
    if len(cleaned) <= max_chars:
        return [cleaned]

    chunks = []
    current = []
    current_len = 0
    for sentence in re.split(r"(?<=[.!?])\s+", cleaned):
        sentence = sentence.strip()
        if not sentence:
            continue
        if current_len + len(sentence) + 1 <= max_chars:
            current.append(sentence)
            current_len += len(sentence) + 1
        else:
            if current:
                chunks.append(" ".join(current))
            current = [sentence]
            current_len = len(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks if chunks else [cleaned]


def _has_hf_token() -> bool:
    return bool(HF_TOKEN)


def _call_hf(model_name: str, payload: dict, timeout: int = 60):
    if not _has_hf_token():
        raise RuntimeError("Missing HUGGINGFACE_API_TOKEN environment variable.")

    url = f"https://api-inference.huggingface.co/models/{model_name}"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return response.text

    try:
        error_data = response.json()
    except ValueError:
        error_data = {"error": response.text}

    raise RuntimeError(error_data.get("error") or error_data.get("message") or f"HF request failed with status {response.status_code}.")


def summarize_text(text: str) -> dict:
    cleaned = normalize_text(text)
    if not cleaned:
        return {"summary": "No hay contenido para resumir.", "model": DEFAULT_SUMMARY_MODEL, "source": "fallback"}

    if not _has_hf_token():
        return {
            "summary": heuristic_summary(cleaned),
            "model": DEFAULT_SUMMARY_MODEL,
            "source": "fallback"
        }

    try:
        chunks = split_text_chunks(cleaned)
        summaries = []
        for chunk in chunks[:4]:
            result = _call_hf(DEFAULT_SUMMARY_MODEL, {"inputs": chunk})
            summaries.append(_extract_summary_text(result))
        combined = " ".join(s for s in summaries if s)
        if not combined:
            raise RuntimeError("No summary text produced.")
        return {"summary": combined, "model": DEFAULT_SUMMARY_MODEL, "source": "huggingface"}
    except Exception:
        return {
            "summary": heuristic_summary(cleaned),
            "model": DEFAULT_SUMMARY_MODEL,
            "source": "fallback"
        }


def answer_question(question: str, context: str) -> dict:
    question = (question or "").strip()
    context = normalize_text(context or "")
    if not question:
        return {"answer": "Necesitas formular una pregunta antes de consultar el documento.", "source": "fallback"}
    if not context:
        return {"answer": "No hay contenido disponible para responder. Sube un PDF o pega un texto.", "source": "fallback"}

    if not _has_hf_token():
        return {"answer": fallback_answer(question, context), "source": "fallback"}

    try:
        chunks = split_text_chunks(context, max_chars=2200)
        ranked = rank_chunks_for_question(chunks, question)
        context_text = "\n\n".join(ranked[:3])
        response = _call_hf(DEFAULT_QA_MODEL, {"inputs": {"question": question, "context": context_text}})
        answer = response.get("answer") if isinstance(response, dict) else None
        if answer:
            return {"answer": answer.strip(), "source": "huggingface"}
        raise RuntimeError("Empty answer from model.")
    except Exception:
        return {"answer": fallback_answer(question, context), "source": "fallback"}


def extract_keywords(text: str, limit: int = 10) -> dict:
    cleaned = normalize_text(text)
    if not cleaned:
        return {"keywords": [], "source": "fallback"}

    if not _has_hf_token():
        keywords = heuristic_keywords(cleaned, limit)
        return {"keywords": keywords, "source": "fallback"}

    try:
        payload = {"inputs": cleaned}
        result = _call_hf(DEFAULT_KEYWORDS_MODEL, payload)
        keywords = parse_keyword_output(result, limit)
        if keywords:
            return {"keywords": keywords, "source": "huggingface"}
    except Exception:
        pass

    return {"keywords": heuristic_keywords(cleaned, limit), "source": "fallback"}


def classify_text(text: str) -> dict:
    cleaned = normalize_text(text)
    if not cleaned:
        return {"labels": [], "source": "fallback"}

    if not _has_hf_token():
        return {"labels": heuristic_classification(cleaned), "source": "fallback"}

    try:
        result = _call_hf(DEFAULT_CLASSIFICATION_MODEL, {"inputs": cleaned})
        labels = parse_classification_output(result)
        if labels:
            return {"labels": labels, "source": "huggingface"}
    except Exception:
        pass

    return {"labels": heuristic_classification(cleaned), "source": "fallback"}


def _extract_summary_text(result):
    if isinstance(result, list) and result and isinstance(result[0], dict):
        text = result[0].get("summary_text") or result[0].get("generated_text")
        if text:
            return str(text)
    if isinstance(result, dict):
        if "summary_text" in result:
            return str(result["summary_text"])
        if "generated_text" in result:
            return str(result["generated_text"])
        if "output_text" in result:
            return str(result["output_text"])
    if isinstance(result, str):
        return result
    return ""


def parse_keyword_output(result, limit: int = 10):
    if isinstance(result, list):
        values = []
        for item in result[:limit]:
            if isinstance(item, dict):
                values.append(item.get("keyword") or item.get("word") or item.get("text") or "")
            elif isinstance(item, str):
                values.append(item)
        return [value.strip() for value in values if value and value.strip()][:limit]

    if isinstance(result, dict):
        key = result.get("keywords") or result.get("predictions") or result.get("result")
        if isinstance(key, list):
            values = []
            for item in key[:limit]:
                if isinstance(item, dict):
                    values.append(item.get("keyword") or item.get("word") or item.get("text") or "")
                elif isinstance(item, str):
                    values.append(item)
            return [value.strip() for value in values if value and value.strip()][:limit]
    return []


def parse_classification_output(result):
    if isinstance(result, list):
        if result and isinstance(result[0], dict):
            return [{"label": item.get("label"), "score": float(item.get("score", 0.0))} for item in result[:5]]
        if result and isinstance(result[0], list):
            flat = []
            for item in result[0][:5]:
                if isinstance(item, dict):
                    flat.append({"label": item.get("label"), "score": float(item.get("score", 0.0))})
            return flat
    if isinstance(result, dict):
        if "label" in result and "score" in result:
            return [{"label": result.get("label"), "score": float(result.get("score", 0.0))}]
        if "labels" in result and "scores" in result:
            return [{"label": label, "score": float(score)} for label, score in zip(result["labels"], result["scores"])][:5]
    return []


def heuristic_summary(text: str) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return "No hay información suficiente para generar un resumen claro."
    if len(sentences) <= 3:
        return " ".join(sentences)
    selected = sentences[:3]
    return " ".join(selected)


def rank_chunks_for_question(chunks: list[str], question: str) -> list[str]:
    tokens = set(re.findall(r"[\wáéíóúñü]+", question.lower()))
    scored = []
    for chunk in chunks:
        chunk_text = re.findall(r"[\wáéíóúñü]+", chunk.lower())
        score = sum(1 for token in tokens if token in chunk_text)
        scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    best = [chunk for _, chunk in scored if chunk]
    return best or chunks


def fallback_answer(question: str, context: str) -> str:
    tokens = set(re.findall(r"[\wáéíóúñü]+", question.lower()))
    candidate_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", context) if s.strip()]
    if not candidate_sentences:
        return "No hay información suficiente para responder con precisión."
    scored = []
    for sentence in candidate_sentences:
        sentence_tokens = set(re.findall(r"[\wáéíóúñü]+", sentence.lower()))
        overlap = sum(1 for token in tokens if token in sentence_tokens)
        scored.append((overlap, sentence))
    scored.sort(key=lambda item: item[0], reverse=True)
    for _, sentence in scored:
        if sentence:
            return sentence
    return "No se encontró suficiente información para responder con precisión."


def heuristic_keywords(text: str, limit: int = 10) -> list[str]:
    text = re.sub(r"[^\w\sáéíóúñüÁÉÍÓÚÑÜ]+", " ", text.lower())
    tokens = [token for token in text.split() if token and len(token) > 3 and token not in STOPWORDS]
    counts = Counter(tokens)
    ranked = [term for term, _ in counts.most_common(limit * 2)]
    phrases = []
    for term in ranked:
        if term not in phrases:
            phrases.append(term)
        if len(phrases) >= limit:
            break
    return phrases


def heuristic_classification(text: str) -> list[dict]:
    norm = normalize_text(text).lower()
    positive_hits = sum(1 for word in POSITIVE_WORDS if word in norm)
    negative_hits = sum(1 for word in NEGATIVE_WORDS if word in norm)

    if positive_hits == 0 and negative_hits == 0:
        scores = {"neutral": 0.7, "positive": 0.15, "negative": 0.15}
    else:
        total = max(1, positive_hits + negative_hits)
        positive_score = positive_hits / total
        negative_score = negative_hits / total
        neutral_score = 1.0 - max(positive_score, negative_score)
        scores = {"neutral": round(neutral_score, 3), "positive": round(positive_score, 3), "negative": round(negative_score, 3)}

    return [
        {"label": "positive", "score": scores.get("positive", 0.0)},
        {"label": "neutral", "score": scores.get("neutral", 0.0)},
        {"label": "negative", "score": scores.get("negative", 0.0)},
    ]
