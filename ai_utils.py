import math
import re
import unicodedata
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
    "utiliza", "utilizan", "permite", "permiten", "tiene", "tienen", "realiza", "realizan",
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
    "use", "uses", "used", "using", "provide", "provides", "provided", "include", "includes",
    "including", "help", "helps", "make", "makes", "made", "store", "stores", "storing",
}
STOPWORDS = SPANISH_STOPWORDS | ENGLISH_STOPWORDS
WORD_PATTERN = re.compile(r"[a-záéíóúñü0-9]+", re.IGNORECASE)
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+|\n+")


def _canonical_token(token: str) -> str:
    decomposed = unicodedata.normalize("NFD", token.casefold())
    return "".join(character for character in decomposed if unicodedata.category(character) != "Mn")


def _stem_token(token: str) -> str:
    word = _canonical_token(token)
    if len(word) <= 4 or not word.isalpha():
        return word
    if word.endswith("ies") and len(word) > 5:
        return word[:-3] + "y"
    if word.endswith("ing") and len(word) > 6:
        stem = word[:-3]
        if len(stem) > 3 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem + "e" if stem.endswith(("at", "iz")) else stem
    if word.endswith("ed") and len(word) > 5:
        stem = word[:-2]
        if len(stem) > 3 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem + "e" if stem.endswith(("at", "iv")) else stem
    if word.endswith("es") and len(word) > 5:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 5:
        return word[:-1]
    if word.endswith("e") and len(word) > 6:
        return word[:-1]
    return word


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
    "Environment": {
        "environment", "climate", "ecosystem", "pollution", "conservation", "wildlife",
        "wetland", "wetlands", "habitat", "ecology", "ecological", "renewable energy",
        "solar energy", "energy", "battery", "bird", "birds", "medio ambiente", "clima",
        "ecosistema", "contaminación", "conservación", "biodiversidad", "humedal", "hábitat",
        "ecología", "energía renovable", "energía", "ave", "aves",
    },
    "Psychology": {
        "psychology", "behavior", "cognition", "emotion", "mental", "therapy",
        "psicología", "conducta", "cognición", "emoción", "mental", "terapia",
    },
    "Geography": {
        "geography", "geographic", "region", "population", "territory",
        "geografía", "geográfico", "región", "población", "territorio", "paisaje",
    },
    "Arts": {
        "art", "artist", "painting", "music", "design", "museum",
        "arte", "artista", "pintura", "música", "diseño", "museo",
    },
    "Sports": {
        "sport", "team", "player", "game", "competition", "athlete",
        "deporte", "equipo", "jugador", "partido", "competición", "atleta",
    },
}
SYNONYM_GROUPS = (
    {"cause", "causes", "caused", "reason", "because", "resulted", "causa", "motivo", "razón", "provocó"},
    {"effect", "impact", "consequence", "result", "efecto", "impacto", "consecuencia", "resultado"},
    {"decline", "decrease", "decreased", "fall", "fell", "drop", "reduction", "declining", "disminución", "disminuyó"},
    {"develop", "developed", "created", "create", "invented", "invent", "formulated", "proposed", "desarrolló", "desarrollo", "creó", "inventó"},
    {"explain", "describe", "detail", "explanation", "explicar", "describir", "explicación"},
    {"compare", "difference", "contrast", "comparison", "comparar", "diferencia", "contrastar", "comparación"},
    {"date", "year", "when", "fecha", "año", "cuándo"},
    {"person", "who", "author", "researcher", "persona", "quién", "autor", "investigador"},
    {"place", "where", "location", "lugar", "dónde", "ubicación"},
    {"definition", "define", "meaning", "definición", "significa", "significado"},
)
SYNONYM_LOOKUP = {_stem_token(term): group for group in SYNONYM_GROUPS for term in group}
KEYWORD_NON_CONCEPTS = {
    "now", "led", "fell", "reduced", "reduce", "supports", "support", "protect", "protects",
    "protected", "power", "powered", "impulsa", "impulsan", "pueden", "puede",
}
KEYPHRASE_ADJECTIVE_ENDINGS = (
    "able", "ible", "al", "ive", "ous", "ary", "ory", "ful", "less",
    "ical", "ico", "ica", "ivo", "iva",
)
KEYPHRASE_NOUN_TERMS = {
    _stem_token(token)
    for terms in TOPIC_TERMS.values()
    for term in terms
    for token in WORD_PATTERN.findall(term)
}
FOLLOW_UP_REFERENCES = re.compile(
    r"\b(that|those|it|they|them|both|previous|above|this|these|"
    r"eso|esa|ese|esto|esta|este|ambos|ambas|anterior|anteriores|lo\s+anterior)\b",
    re.IGNORECASE,
)


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
    if max_chars < 1 or overlap < 0 or overlap >= max_chars:
        raise AIServiceError(
            "Chunk size must be positive and overlap must be smaller than the chunk size.",
            "invalid_request",
            400,
        )
    return _chunk_pages(document_pages, max_chars, overlap)


def _chunk_pages(
    document_pages: list[dict[str, Any]],
    max_chars: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
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
                if len(chunks) > MAX_DOCUMENT_CHUNKS:
                    raise AIServiceError(
                        "This document is too extensive for one analysis. Split it into smaller documents and try again.",
                        "document_too_large",
                        413,
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
    return [
        _stem_token(token)
        for token in _tokens(text)
        if len(token) > 2 and token not in STOPWORDS
    ]


def _detect_language(text: str) -> str:
    tokens = _tokens(text)
    spanish = sum(token in SPANISH_STOPWORDS for token in tokens)
    english = sum(token in ENGLISH_STOPWORDS for token in tokens)
    if spanish == english:
        spanish += sum(character in "áéíóúñ¿¡" for character in text.lower())
    return "es" if spanish > english else "en"


def _sentence_records(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    seen: dict[str, dict[str, Any]] = {}
    for chunk_index, chunk in enumerate(chunks):
        for sentence in SENTENCE_PATTERN.split(chunk["text"]):
            sentence = sentence.strip()
            if not sentence:
                continue
            key = normalize_text(sentence).casefold()
            if key in seen:
                record = seen[key]
                record["occurrences"] += 1
                if chunk.get("page_start") is not None:
                    record["pages"].add(chunk["page_start"])
                continue
            record = {
                "text": sentence,
                "page": chunk.get("page_start"),
                "pages": {chunk["page_start"]} if chunk.get("page_start") is not None else set(),
                "occurrences": 1,
                "index": len(records),
                "chunk_index": chunk_index,
            }
            seen[key] = record
            records.append(record)
    return records


def _extractive_summary(chunks: list[dict[str, Any]], max_chars: int = 3_500) -> str:
    sentences = _sentence_records(chunks)
    if not sentences:
        return ""
    full_text = " ".join(sentence["text"] for sentence in sentences)
    if len(sentences) == 1:
        return _truncate_text(full_text, max_chars)

    document_frequency: Counter[str] = Counter()
    sentence_terms: list[set[str]] = []
    for sentence in sentences:
        terms = set(_content_tokens(sentence["text"]))
        sentence_terms.append(terms)
        document_frequency.update(terms)

    sentence_count = len(sentences)
    ranked: list[tuple[float, dict[str, Any]]] = []
    relevance_by_index: dict[int, float] = {}
    for sentence, terms in zip(sentences, sentence_terms):
        if not terms:
            continue
        # Smoothed TF-IDF favors distinctive terms while damping long sentences.
        score = sum(
            (1 + math.log1p(sum(term in item for item in sentence_terms)))
            * (math.log((sentence_count + 1) / (document_frequency[term] + 1)) + 1)
            for term in terms
        ) / math.sqrt(len(terms))
        position = sentence["index"] / max(1, sentence_count - 1)
        score *= 1 + 0.12 * (1 - position)
        score *= 1 + 0.12 * math.log1p(sentence["occurrences"] - 1)
        ranked.append((score, sentence))
        relevance_by_index[sentence["index"]] = score

    # Keep a broad shortlist, then use maximal marginal relevance to avoid repetition.
    ranked.sort(key=lambda item: (-item[0], item[1]["index"]))
    shortlist = [sentence for _, sentence in ranked[: min(80, len(ranked))]]
    target_chars = min(max_chars, max(180, int(len(full_text) * 0.30)))
    target_count = min(
        8,
        1 if sentence_count <= 2 else max(2, round(sentence_count * 0.30)),
    )
    selected: list[dict[str, Any]] = []
    used_chars = 0
    section_count = min(4, max(1, len(chunks)))
    section_selections = Counter()
    while shortlist and len(selected) < target_count:
        best_index = -1
        best_score = float("-inf")
        for index, sentence in enumerate(shortlist):
            extra = len(sentence["text"]) + (2 if selected else 0)
            if used_chars + extra > target_chars:
                continue
            terms = sentence_terms[sentence["index"]]
            redundancy = max(
                (
                    len(terms & sentence_terms[item["index"]])
                    / max(1, len(terms | sentence_terms[item["index"]]))
                    for item in selected
                ),
                default=0.0,
            )
            section = min(
                section_count - 1,
                sentence["chunk_index"] * section_count // max(1, len(chunks)),
            )
            coverage_bonus = 0.24 if section_selections[section] == 0 else 0
            relevance = relevance_by_index[sentence["index"]]
            adjusted = relevance * (1 - 0.68 * redundancy) + coverage_bonus
            if adjusted > best_score:
                best_index, best_score = index, adjusted
        if best_index < 0:
            break
        sentence = shortlist.pop(best_index)
        selected.append(sentence)
        used_chars += len(sentence["text"]) + (2 if len(selected) > 1 else 0)
        section = min(
            section_count - 1,
            sentence["chunk_index"] * section_count // max(1, len(chunks)),
        )
        section_selections[section] += 1
    if not selected:
        return _truncate_text(full_text, max_chars)
    return "\n\n".join(sentence["text"] for sentence in sorted(selected, key=lambda item: item["index"]))


def _truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max(0, max_chars - 1)].rsplit(" ", 1)[0].rstrip() + "…"


def _keyword_candidates(text: str) -> list[tuple[float, str]]:
    sentences = [sentence for sentence in SENTENCE_PATTERN.split(normalize_text(text)) if sentence]
    content_by_sentence = []
    term_documents: Counter[str] = Counter()
    for sentence in sentences:
        sentence_tokens = []
        for index, token in enumerate(_tokens(sentence)):
            if (
                len(token) > 2
                and token not in STOPWORDS
                and _canonical_token(token) not in KEYWORD_NON_CONCEPTS
                and not token.isdigit()
            ):
                sentence_tokens.append((index, token.casefold(), _stem_token(token)))
        content_by_sentence.append(sentence_tokens)
        sentence_terms = {normalized for _, _, normalized in sentence_tokens}
        term_documents.update(sentence_terms)
    counts: Counter[str] = Counter()
    display_terms: dict[str, str] = {}
    total_terms = 0
    for sentence_tokens in content_by_sentence:
        for _, display, normalized in sentence_tokens:
            counts[normalized] += 1
            display_terms.setdefault(normalized, display)
            total_terms += 1
    candidates: dict[str, float] = {}
    total_terms = max(1, total_terms)
    for term, count in counts.items():
        idf = math.log((len(sentences) + 1) / (term_documents[term] + 1)) + 1
        coverage = term_documents[term] / max(1, len(sentences))
        candidates[term] = (
            (1 + math.log(count))
            * (0.75 + 2 * coverage)
            * (0.8 + 0.2 * idf)
            * (1 + count / total_terms)
        )

    phrase_counts: Counter[str] = Counter()
    phrase_displays: dict[str, str] = {}
    for sentence_tokens in content_by_sentence:
        for left in range(len(sentence_tokens)):
            first_index, first_display, first = sentence_tokens[left]
            for second_index, second_display, second in sentence_tokens[left + 1:left + 4]:
                if second_index - first_index > 1:
                    break
                if first == second:
                    continue
                phrase = f"{first} {second}"
                phrase_counts[phrase] += 1
                phrase_displays.setdefault(phrase, f"{first_display} {second_display}")
    for phrase, count in phrase_counts.items():
        first_display, second_display = phrase_displays[phrase].split(" ", 1)
        adjective_phrase = (
            first_display.endswith(KEYPHRASE_ADJECTIVE_ENDINGS)
            or (
                _stem_token(first_display) in KEYPHRASE_NOUN_TERMS
                and second_display.endswith(KEYPHRASE_ADJECTIVE_ENDINGS)
            )
        )
        if count < 2 and not adjective_phrase:
            continue
        first, second = phrase.split()
        score = (1 + math.log(count)) * 1.8 + 0.35 * (counts[first] + counts[second])
        if adjective_phrase and count == 1:
            score += 1.2
        candidates[phrase] = score

    ranked = sorted(candidates.items(), key=lambda item: (-item[1], item[0]))
    selected: list[tuple[float, str]] = []
    selected_terms: set[str] = set()
    for term, score in ranked:
        component_terms = set(term.split())
        if component_terms and component_terms <= selected_terms:
            continue
        display_term = phrase_displays.get(term, term) if " " in term else display_terms.get(term, term)
        selected.append((score, display_term))
        selected_terms.update(component_terms)
    return selected


def _extract_keywords(text: str, limit: int = 10) -> list[str]:
    return [term for _, term in _keyword_candidates(text)[:limit]]


def _classify(text: str) -> list[dict[str, Any]]:
    tokens = Counter(_content_tokens(text))
    normalized_text = f" {_canonical_token(text)} "
    evidence: dict[str, tuple[float, list[str]]] = {}
    for label, terms in TOPIC_TERMS.items():
        score = 0.0
        matched: list[str] = []
        for term in terms:
            normalized_term = " ".join(_canonical_token(token) for token in _tokens(term))
            if " " in normalized_term and f" {normalized_term} " in normalized_text:
                score += 1.6
                matched.append(term)
            else:
                for token in _content_tokens(term):
                    count = tokens[token]
                    if count:
                        score += (1 + math.log1p(count)) / max(1, len(_content_tokens(term)))
                        matched.append(term)
        if score:
            evidence[label] = (score, matched[:5])
    matches = sorted(evidence.items(), key=lambda item: (-item[1][0], item[0]))[:3]
    total = sum(score for _, (score, _) in matches)
    if total < 0.35:
        return [{"label": "Other", "score": 0.0, "evidence": []}]
    return [
        {
            "label": label,
            "score": round(score / total, 2),
            "evidence": list(dict.fromkeys(matched)),
        }
        for label, (score, matched) in matches
    ]


def _unique_references(chunks: list[dict[str, Any]]) -> list[int]:
    return sorted(
        {
            int(chunk["page_start"])
            for chunk in chunks
            if chunk.get("page_start") is not None
        }
    )


def _summary_references(chunks: list[dict[str, Any]], summary: str) -> list[int]:
    selected = {
        normalize_text(sentence).casefold()
        for sentence in summary.split("\n\n")
        if sentence.strip()
    }
    return sorted(
        {
            int(page)
            for record in _sentence_records(chunks)
            if normalize_text(record["text"]).casefold() in selected
            for page in record["pages"]
        }
    )


def _analysis_payload(text: str, pages: list[str] | None) -> tuple[str, list[dict[str, Any]], str]:
    cleaned = normalize_text(text)
    if not cleaned and not pages:
        raise AIServiceError("Add document text before starting an analysis.", "empty_document", 400)
    document_pages = _document_pages(cleaned, pages)
    chunks = _chunk_pages(document_pages)
    if not chunks:
        raise AIServiceError("No readable text was found in the document.", "empty_document", 400)
    analysis_text = " ".join(page["text"] for page in document_pages)
    return analysis_text, chunks, analysis_text


def analyze_document(text: str, pages: list[str] | None = None) -> dict[str, Any]:
    analysis_text, chunks, _ = _analysis_payload(text, pages)
    summary = _extractive_summary(chunks)
    return {
        "summary": {
            "summary": summary,
            "model": LOCAL_ENGINE_NAME,
            "source": "local",
            "references": _summary_references(chunks, summary),
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
    summary = _extractive_summary(chunks)
    return {
        "summary": summary,
        "model": LOCAL_ENGINE_NAME,
        "source": "local",
        "references": _summary_references(chunks, summary),
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
    chunks: list[dict[str, Any]],
    question: str,
    document_index: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    index = document_index or _build_document_index(chunks)
    query_tokens = _query_tokens(question)
    if not query_tokens:
        query_tokens = []
    expanded_query = Counter(query_tokens)
    expanded_query.update(
        {
            _stem_token(term): 0.6
            for term in _intent_terms(_question_intent(question))
        }
    )
    for token in set(query_tokens):
        group = SYNONYM_LOOKUP.get(token)
        if group:
            for synonym in group:
                expanded_query.setdefault(_stem_token(synonym), 0.45)

    intent = _question_intent(question)
    scored: list[tuple[float, int, dict[str, Any]]] = []
    for item in index["chunks"]:
        frequency = item["frequencies"]
        length = len(item["tokens"])
        score = 0.0
        for token, query_weight in expanded_query.items():
            term_frequency = frequency[token]
            if not term_frequency:
                continue
            doc_frequency = index["document_frequency"][token]
            inverse_frequency = math.log(
                1 + (len(chunks) - doc_frequency + 0.5) / (doc_frequency + 0.5)
            )
            denominator = term_frequency + 1.2 * (
                1 - 0.75 + 0.75 * length / max(1, index["average_length"])
            )
            score += query_weight * inverse_frequency * (term_frequency * 2.2 / denominator)
        if intent == "date" and re.search(
            r"\b(?:1[5-9]\d{2}|20\d{2}|21\d{2})\b", item["chunk"]["text"]
        ):
            score += 0.5
        if intent == "cause" and re.search(
            r"\b(cause[sd]?|led to|leads to|because|due to|resulted in|debido a|porque|ya que)\b",
            _canonical_token(item["chunk"]["text"]),
        ):
            score += 0.4
        if intent == "person" and re.search(
            r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b", item["chunk"]["text"]
        ):
            score += 0.4
        if score:
            scored.append((score, item["position"], item["chunk"]))
    scored.sort(key=lambda item: (-item[0], item[1]))
    selected: list[dict[str, Any]] = []
    selected_chars = 0
    for _, _, chunk in scored:
        if len(selected) >= MAX_RETRIEVED_CHUNKS:
            break
        if selected_chars + len(chunk["text"]) > MAX_RETRIEVED_CHARS and selected:
            continue
        selected.append(chunk)
        selected_chars += len(chunk["text"])
    return selected


def _query_tokens(question: str) -> list[str]:
    tokens = _content_tokens(question)
    return tokens


def _build_document_index(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    indexed_chunks = []
    document_frequency: Counter[str] = Counter()
    total_length = 0
    for position, chunk in enumerate(chunks):
        tokens = _content_tokens(chunk["text"])
        frequencies = Counter(tokens)
        document_frequency.update(frequencies.keys())
        total_length += len(tokens)
        indexed_chunks.append(
            {
                "position": position,
                "chunk": chunk,
                "tokens": tokens,
                "frequencies": frequencies,
            }
        )
    return {
        "chunks": indexed_chunks,
        "document_frequency": document_frequency,
        "average_length": total_length / max(1, len(indexed_chunks)),
    }


def _valid_history(history: list[dict[str, str]] | None) -> list[dict[str, str]]:
    if not isinstance(history, list):
        return []
    valid = []
    for message in history[-8:]:
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        content = message.get("content")
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            valid.append({"role": role, "content": normalize_text(content)[:800]})
    return valid


def _follow_up_context(question: str, history: list[dict[str, str]]) -> str:
    if not FOLLOW_UP_REFERENCES.search(question):
        return ""
    previous = [
        message["content"]
        for message in history[-4:]
        if message["role"] in {"user", "assistant"}
    ]
    return " ".join(previous[-3:])


def _question_intent(question: str) -> str:
    normalized = _canonical_token(question)
    if re.search(r"\b(when|date|year|cuando|fecha|ano)\b", normalized):
        return "date"
    if re.search(r"\b(who|person|quien|persona)\b", normalized):
        return "person"
    if re.search(r"\b(where|place|donde|lugar)\b", normalized):
        return "place"
    if re.search(
        r"\b(why|cause|reason|por que|causa|motivo|razon|led to|leads to)\b",
        normalized,
    ):
        return "cause"
    if re.search(r"\b(compare|difference|contrast|comparar|diferencia|contrastar)\b", normalized):
        return "comparison"
    if re.search(r"\b(define|definition|meaning|definicion|significa)\b", normalized):
        return "definition"
    if re.search(r"\b(list|name|enumerate|lista|nombra|enumera)\b", normalized):
        return "list"
    return "explanation"


def _intent_terms(intent: str) -> tuple[str, ...]:
    return {
        "date": ("date", "year", "fecha", "año"),
        "person": ("person", "author", "researcher", "persona", "autor"),
        "place": ("place", "location", "region", "lugar", "ubicación"),
        "cause": ("cause", "reason", "because", "causa", "motivo"),
        "comparison": ("compare", "difference", "contrast", "comparar", "diferencia"),
        "definition": ("definition", "meaning", "definition", "definición", "significado"),
        "list": ("list", "items", "lista", "elementos"),
    }.get(intent, ())


def _sentence_relevance(
    sentence: str,
    query: Counter[str],
    document_index: dict[str, Any],
    intent: str,
) -> float:
    tokens = _content_tokens(sentence)
    frequencies = Counter(tokens)
    score = 0.0
    for token, query_weight in query.items():
        term_frequency = frequencies[token]
        if not term_frequency:
            continue
        doc_frequency = document_index["document_frequency"][token]
        inverse_frequency = math.log(
            1 + (len(document_index["chunks"]) - doc_frequency + 0.5) / (doc_frequency + 0.5)
        )
        score += query_weight * inverse_frequency * term_frequency / (term_frequency + 1.2)
    lowered = _canonical_token(sentence)
    if intent == "date" and re.search(r"\b(?:1[5-9]\d{2}|20\d{2}|21\d{2})\b", sentence):
        score += 0.8
    if intent == "cause" and re.search(
        r"\b(because|because of|due to|caused by|since|led to|leads to|porque|debido|a causa de|ya que)\b",
        lowered,
    ):
        score += 0.4
    if intent == "definition" and re.search(
        r"\b(is|are|means|refers to|es|son|significa|se define)\b", lowered
    ):
        score += 0.2
    return score


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
    conversation = _valid_history(history)
    follow_up_context = _follow_up_context(question, conversation)
    query_text = f"{question} {follow_up_context}".strip()
    question_tokens = _query_tokens(query_text)
    if not question_tokens and follow_up_context:
        question_tokens = _query_tokens(follow_up_context)
    if (
        FOLLOW_UP_REFERENCES.search(question)
        and not follow_up_context
        and len(question_tokens) <= 2
    ):
        clarification = (
            "¿A qué parte de la conversación anterior te refieres?"
            if _detect_language(cleaned or " ".join(pages or [])) == "es"
            else "Which part of the previous conversation are you referring to?"
        )
        return {
            "answer": clarification,
            "references": [],
            "source": "local",
            "model": LOCAL_ENGINE_NAME,
            "answer_type": "clarification",
        }
    document_index = _build_document_index(chunks)
    selected = _rank_chunks_for_question(chunks, query_text, document_index)
    expanded_query = Counter(question_tokens)
    intent = _question_intent(question)
    expanded_query.update(
        {
            _stem_token(term): 0.6
            for term in _intent_terms(intent)
        }
    )
    for token in set(question_tokens):
        group = SYNONYM_LOOKUP.get(token)
        if group:
            for synonym in group:
                expanded_query.setdefault(_stem_token(synonym), 0.45)
    selected_ids = {id(chunk) for chunk in selected}
    sentence_matches: list[dict[str, Any]] = []
    seen_sentences: set[str] = set()
    for chunk in chunks:
        if id(chunk) not in selected_ids:
            continue
        for sentence in SENTENCE_PATTERN.split(chunk["text"]):
            sentence = sentence.strip()
            normalized_sentence = normalize_text(sentence).casefold()
            if not sentence or normalized_sentence in seen_sentences:
                continue
            seen_sentences.add(normalized_sentence)
            score = _sentence_relevance(
                sentence,
                expanded_query,
                document_index,
                intent,
            )
            if score > 0:
                sentence_matches.append(
                    {
                        "score": score,
                        "text": sentence,
                        "page": chunk.get("page_start"),
                        "terms": set(_content_tokens(sentence)),
                        "position": len(sentence_matches),
                    }
                )
    language = _detect_language(cleaned or " ".join(pages or []))
    if not sentence_matches:
        answer = (
            "No encuentro evidencia suficiente en el texto proporcionado para responder."
            if language == "es"
            else "I could not find enough evidence in the provided text to answer."
        )
        return {
            "answer": answer,
            "references": [],
            "source": "local",
            "model": LOCAL_ENGINE_NAME,
            "answer_type": "not_found",
        }

    selected_sentences: list[dict[str, Any]] = []
    remaining = sorted(sentence_matches, key=lambda item: (-item["score"], item["position"]))
    target_count = 2 if intent == "comparison" else 3
    while remaining and len(selected_sentences) < target_count:
        best_index = max(
            range(len(remaining)),
            key=lambda index: remaining[index]["score"] * (
                1 - 0.72 * max(
                    (
                        len(remaining[index]["terms"] & item["terms"])
                        / max(1, len(remaining[index]["terms"] | item["terms"]))
                        for item in selected_sentences
                    ),
                    default=0.0,
                )
            ),
        )
        selected_sentences.append(remaining.pop(best_index))
    selected_sentences.sort(key=lambda item: item["position"])
    answer_parts = [item["text"] for item in selected_sentences]
    references = set()
    for item in selected_sentences:
        if item["page"] is not None:
            references.add(int(item["page"]))
    return {
        "answer": " ".join(answer_parts),
        "references": sorted(references),
        "source": "local",
        "model": LOCAL_ENGINE_NAME,
        "answer_type": "extractive",
    }
