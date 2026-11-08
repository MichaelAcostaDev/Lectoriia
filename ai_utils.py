import re
from collections import Counter
from typing import Any


MAX_DOCUMENT_CHARS = 500_000
MAX_DOCUMENT_CHUNKS = 512
CHUNK_SIZE = 6_000
CHUNK_OVERLAP = 500
MAX_RETRIEVED_CHUNKS = 4
MAX_RETRIEVED_CHARS = 14_000
LOCAL_ENGINE_NAME = "Local"

SPANISH_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "de", "del",
    "al", "por", "para", "con", "sin", "sobre", "entre", "como", "más", "muy", "pero",
    "porque", "cuando", "donde", "que", "qué", "quien", "quién", "sus", "este", "esta",
    "estos", "estas", "ese", "esa", "esos", "esas", "año", "años", "ser", "estar",
    "tener", "también", "hace", "hacer", "desde", "hasta", "todos", "todas", "menos",
    "a", "en", "se", "si", "no", "sí", "es", "son", "fue", "fueron", "ha", "han", "hay",
    "tras", "durante", "según", "mediante", "cada", "mismo", "misma", "después", "del",
    "lo", "le", "les", "me", "te", "mi", "tu", "su", "ya", "tambien", "esto", "esa",
    "será", "puede", "pueden", "dicho", "así", "asimismo", "cual", "cuales", "uno",
}
ENGLISH_STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "with", "without", "from", "into",
    "in", "on", "at", "of", "to", "is", "are", "was", "were", "be", "been",
    "being", "this", "that", "these", "those", "as", "by", "it", "its", "their",
    "they", "them", "he", "she", "we", "you", "our", "your", "us", "not", "but",
    "also", "more", "most", "very", "have", "has", "had", "can", "could", "should",
    "would", "will", "about", "after", "before", "during", "under", "over", "then",
    "there", "here", "through", "which", "what", "when", "where", "who", "why", "how",
    "were", "been", "being", "than", "their", "them", "these", "those", "each",
    "such", "many", "much", "some", "any", "all", "both", "into", "out", "up",
}
STOPWORDS = SPANISH_STOPWORDS | ENGLISH_STOPWORDS
WORD_PATTERN = re.compile(r"[a-záéíóúñü0-9]+", re.IGNORECASE)
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+|\n+")

TOPIC_TERMS = {
    "Technology": {
        "technology", "software", "computer", "digital", "internet", "data", "algorithm",
        "technology", "tecnología", "software", "computadora", "digital", "internet",
        "datos", "algoritmo", "informática", "programación", "inteligencia", "red",
    },
    "Science": {
        "science", "research", "experiment", "scientific", "species", "chemical",
        "ciencia", "investigación", "experimento", "científico", "especies", "química",
        "física", "biología", "estudio", "método",
    },
    "Education": {
        "education", "student", "school", "teacher", "learning", "university", "course",
        "educación", "estudiante", "escuela", "docente", "aprendizaje", "universidad",
        "curso", "enseñanza", "alumno", "profesor",
    },
    "Business": {
        "business", "company", "market", "customer", "sales", "industry", "revenue",
        "negocio", "empresa", "mercado", "cliente", "ventas", "industria", "ingresos",
        "comercio", "producto", "inversión",
    },
    "History": {
        "history", "historical", "century", "ancient", "war", "empire", "historical",
        "historia", "histórico", "siglo", "antiguo", "guerra", "imperio", "revolución",
        "civilización", "época",
    },
    "Health": {
        "health", "medical", "patient", "disease", "treatment", "hospital", "medicine",
        "salud", "médico", "paciente", "enfermedad", "tratamiento", "hospital",
        "medicina", "síntoma", "terapia", "clínica",
    },
    "Finance": {
        "finance", "financial", "bank", "money", "tax", "stock", "budget", "economic",
        "finanzas", "financiero", "banco", "dinero", "impuesto", "acciones", "presupuesto",
        "economía", "deuda", "capital",
    },
    "Politics": {
        "politics", "political", "government", "election", "president", "congress", "vote",
        "política", "político", "gobierno", "elección", "presidente", "congreso", "voto",
        "partido", "democracia", "estado",
    },
    "Law": {
        "law", "legal", "court", "judge", "rights", "contract", "lawyer", "justice",
        "ley", "legal", "tribunal", "juez", "derechos", "contrato", "abogado", "justicia",
        "jurídico", "legislación",
    },
    "Literature": {
        "literature", "novel", "poem", "poetry", "author", "character", "narrative", "book",
        "literatura", "novela", "poema", "poesía", "autor", "personaje", "narrativa", "libro",
        "cuento", "lector",
    },
}


class AIServiceError(RuntimeError):
    def __init__(self, message: str, code: str, status_code: int = 502):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _document_pages(text: str, pages: list[str] | None = None) -> list[dict[str, Any]]:
    if pages is not None:
        return [
            {"page": number, "text": normalize_text(page)}
            for number, page in enumerate(pages, start=1)
            if normalize_text(page)
        ]

    matches = list(re.finditer(r"\[P[aá]gina\s+(\d+)\]\s*", text, flags=re.IGNORECASE))
    if matches:
        result = []
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            page_text = normalize_text(text[match.end():end])
            if page_text:
                result.append({"page": int(match.group(1)), "text": page_text})
        return result
    return [{"page": None, "text": normalize_text(text)}]


def chunk_document(
    text: str,
    pages: list[str] | None = None,
    max_chars: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    document_pages = _document_pages(text, pages)
    if sum(len(page["text"]) for page in document_pages) > MAX_DOCUMENT_CHARS:
        raise AIServiceError(
            "This document exceeds the current analysis limit. Shorten it or split it into smaller documents.",
            "document_too_large",
            413,
        )

    chunks: list[dict[str, Any]] = []
    for page in document_pages:
        page_text = page["text"]
        start = 0
        while start < len(page_text):
            end = min(start + max_chars, len(page_text))
            if end < len(page_text):
                boundary = max(
                    page_text.rfind(". ", start + max_chars // 2, end),
                    page_text.rfind("? ", start + max_chars // 2, end),
                    page_text.rfind("! ", start + max_chars // 2, end),
                    page_text.rfind(" ", start + max_chars // 2, end),
                )
                if boundary > start:
                    end = boundary + 1
            piece = page_text[start:end].strip()
            if piece:
                chunks.append(
                    {
                        "text": piece,
                        "page_start": page["page"],
                        "page_end": page["page"],
                    }
                )
            if end >= len(page_text):
                break
            start = max(start + 1, end - overlap)

    if len(chunks) > MAX_DOCUMENT_CHUNKS:
        raise AIServiceError(
            "This document is too extensive for one analysis. Split it into smaller documents and try again.",
            "document_too_large",
            413,
        )
    return chunks


def _tokens(text: str) -> list[str]:
    return [word.lower() for word in WORD_PATTERN.findall(text)]


def _content_tokens(text: str) -> list[str]:
    return [token for token in _tokens(text) if len(token) > 2 and token not in STOPWORDS]


def _detect_language(text: str) -> str:
    tokens = _tokens(text)
    spanish = sum(token in SPANISH_STOPWORDS for token in tokens)
    english = sum(token in ENGLISH_STOPWORDS for token in tokens)
    if spanish == english:
        spanish += sum(character in "áéíóúñ¿¡" for character in text.lower())
    return "es" if spanish > english else "en"


def _sentence_records(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    seen = set()
    for chunk in chunks:
        for sentence in SENTENCE_PATTERN.split(chunk["text"]):
            sentence = sentence.strip()
            if not sentence:
                continue
            key = normalize_text(sentence).casefold()
            if key in seen:
                continue
            seen.add(key)
            records.append(
                {
                    "text": sentence,
                    "page": chunk.get("page_start"),
                    "index": len(records),
                }
            )
    return records


def _extractive_summary(chunks: list[dict[str, Any]], max_chars: int = 3_500) -> str:
    sentences = _sentence_records(chunks)
    if not sentences:
        return ""
    full_text = " ".join(sentence["text"] for sentence in sentences)
    if len(full_text) <= 900:
        return full_text

    frequencies = Counter(_content_tokens(full_text))
    ranked = []
    for sentence in sentences:
        terms = _content_tokens(sentence["text"])
        if not terms:
            continue
        score = sum(frequencies[term] for term in set(terms)) / (len(set(terms)) ** 0.5)
        ranked.append((score, -sentence["index"], sentence))

    selected = []
    used_chars = 0
    for _, _, sentence in sorted(ranked, reverse=True):
        extra = len(sentence["text"]) + (2 if selected else 0)
        if used_chars + extra > max_chars:
            continue
        selected.append(sentence)
        used_chars += extra
        if len(selected) >= 8:
            break
    if not selected:
        return full_text[:max_chars].rsplit(" ", 1)[0]
    return "\n\n".join(sentence["text"] for sentence in sorted(selected, key=lambda item: item["index"]))


def _extract_keywords(text: str, limit: int = 10) -> list[str]:
    token_positions = [
        (index, token)
        for index, token in enumerate(_tokens(text))
        if len(token) > 2 and token not in STOPWORDS and not token.isdigit()
    ]
    unigram_counts = Counter(token for _, token in token_positions)
    phrase_counts: Counter[str] = Counter()
    for (first_index, first), (second_index, second) in zip(token_positions, token_positions[1:]):
        if second_index - first_index <= 3 and first != second:
            phrase_counts[f"{first} {second}"] += 1

    ranked = [(float(count), word) for word, count in unigram_counts.items()]
    ranked.extend((count * 1.5, phrase) for phrase, count in phrase_counts.items() if count > 1)
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [term for _, term in ranked[:limit]]


def _classify(text: str) -> list[dict[str, Any]]:
    tokens = set(_tokens(text))
    counts = {
        label: sum(term in tokens for term in terms)
        for label, terms in TOPIC_TERMS.items()
    }
    matches = sorted(
        ((count, label) for label, count in counts.items() if count),
        key=lambda item: (-item[0], item[1]),
    )[:3]
    total = sum(count for count, _ in matches)
    if not total:
        return [{"label": "Other", "score": 1.0}]
    return [
        {"label": label, "score": round(count / total, 2)}
        for count, label in matches
    ]


def _unique_references(chunks: list[dict[str, Any]]) -> list[int]:
    return sorted(
        {
            int(chunk["page_start"])
            for chunk in chunks
            if chunk.get("page_start") is not None
        }
    )


def _analysis_payload(text: str, pages: list[str] | None) -> tuple[str, list[dict[str, Any]], str]:
    cleaned = normalize_text(text)
    if not cleaned and not pages:
        raise AIServiceError("Add document text before starting an analysis.", "empty_document", 400)
    chunks = chunk_document(cleaned, pages)
    if not chunks:
        raise AIServiceError("No readable text was found in the document.", "empty_document", 400)
    analysis_text = " ".join(
        page["text"] for page in _document_pages(cleaned, pages)
    )
    return analysis_text, chunks, analysis_text


def analyze_document(text: str, pages: list[str] | None = None) -> dict[str, Any]:
    analysis_text, chunks, _ = _analysis_payload(text, pages)
    return {
        "summary": {
            "summary": _extractive_summary(chunks),
            "model": LOCAL_ENGINE_NAME,
            "source": "local",
            "references": _unique_references(chunks),
            "chunks_count": len(chunks),
        },
        "keywords": {
            "keywords": _extract_keywords(analysis_text),
            "source": "local",
        },
        "classification": {
            "labels": _classify(analysis_text),
            "source": "local",
        },
        "text_length": len(analysis_text),
        "language": _detect_language(analysis_text),
    }


def summarize_text(text: str, pages: list[str] | None = None) -> dict[str, Any]:
    _, chunks, _ = _analysis_payload(text, pages)
    return {
        "summary": _extractive_summary(chunks),
        "model": LOCAL_ENGINE_NAME,
        "source": "local",
        "references": _unique_references(chunks),
        "chunks_count": len(chunks),
    }


def extract_keywords(
    text: str, limit: int = 10, pages: list[str] | None = None
) -> dict[str, Any]:
    _, _, analysis_text = _analysis_payload(text, pages)
    return {"keywords": _extract_keywords(analysis_text, limit), "source": "local"}


def classify_text(text: str, pages: list[str] | None = None) -> dict[str, Any]:
    _, _, analysis_text = _analysis_payload(text, pages)
    return {"labels": _classify(analysis_text), "source": "local"}


def _rank_chunks_for_question(
    chunks: list[dict[str, Any]], question: str
) -> list[dict[str, Any]]:
    question_tokens = set(_content_tokens(question))
    if not question_tokens:
        return chunks[:MAX_RETRIEVED_CHUNKS]
    scored = []
    for index, chunk in enumerate(chunks):
        chunk_tokens = set(_content_tokens(chunk["text"]))
        overlap = len(question_tokens & chunk_tokens)
        score = overlap / len(question_tokens)
        scored.append((score, -index, chunk))
    ranked = [chunk for _, _, chunk in sorted(scored, reverse=True)]
    selected = ranked[:MAX_RETRIEVED_CHUNKS]
    if not selected or all(
        not question_tokens.intersection(_content_tokens(chunk["text"]))
        for chunk in selected
    ):
        return chunks[:MAX_RETRIEVED_CHUNKS]
    return selected


def answer_question(
    question: str,
    context: str,
    history: list[dict[str, str]] | None = None,
    pages: list[str] | None = None,
) -> dict[str, Any]:
    question = (question or "").strip()
    cleaned = normalize_text(context or "")
    if not question:
        raise AIServiceError("Write a question before consulting the document.", "empty_question", 400)
    if not cleaned and not pages:
        raise AIServiceError("Add document text before asking a question.", "empty_document", 400)

    chunks = chunk_document(cleaned, pages)
    if not chunks:
        raise AIServiceError("No readable text was found in the document.", "empty_document", 400)
    selected = _rank_chunks_for_question(chunks, question)
    question_tokens = set(_content_tokens(question))
    sentence_matches = []
    for chunk_index, chunk in enumerate(selected):
        for sentence_index, sentence in enumerate(SENTENCE_PATTERN.split(chunk["text"])):
            sentence = sentence.strip()
            overlap = question_tokens.intersection(_content_tokens(sentence))
            if sentence and overlap:
                sentence_matches.append(
                    (
                        len(overlap) / max(1, len(question_tokens)),
                        -chunk_index,
                        -sentence_index,
                        sentence,
                        chunk.get("page_start"),
                    )
                )

    language = _detect_language(cleaned or " ".join(pages or []))
    if not sentence_matches:
        answer = (
            "No encuentro evidencia suficiente en el texto proporcionado para responder."
            if language == "es"
            else "I could not find enough evidence in the provided text to answer."
        )
        return {"answer": answer, "references": [], "source": "local", "model": LOCAL_ENGINE_NAME}

    best = sorted(sentence_matches, reverse=True)[:3]
    best.sort(key=lambda item: (item[1], item[2]))
    answer_parts = []
    references = set()
    for _, _, _, sentence, page in best:
        answer_parts.append(sentence)
        if page is not None:
            references.add(int(page))
    return {
        "answer": " ".join(answer_parts),
        "references": sorted(references),
        "source": "local",
        "model": LOCAL_ENGINE_NAME,
    }
