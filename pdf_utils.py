import os
import re
import tempfile
from typing import Dict, List, Tuple

from pypdf import PdfReader

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024


def validate_pdf(file_obj, file_name: str) -> None:
    if not file_name.lower().endswith(".pdf"):
        raise ValueError("El archivo debe tener extensión .pdf.")

    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    file_obj.seek(0)
    if file_size <= 0:
        raise ValueError("El archivo PDF está vacío.")
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError("El archivo supera el tamaño máximo permitido (15 MB).")


def extract_pdf_text(file_obj) -> Dict[str, object]:
    file_name = getattr(file_obj, "filename", "document.pdf")
    validate_pdf(file_obj, file_name)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        file_obj.seek(0)
        temp_file.write(file_obj.read())
        temp_path = temp_file.name

    try:
        reader = PdfReader(temp_path)
        if len(reader.pages) == 0:
            raise ValueError("El PDF no contiene páginas válidas.")

        page_texts: List[str] = []
        for idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            cleaned = re.sub(r"\s+", " ", text).strip()
            page_texts.append(cleaned)

        full_text = "\n\n".join(f"[Página {idx}] {text}" for idx, text in enumerate(page_texts, start=1))
        if not full_text.strip():
            raise ValueError("No se pudo extraer texto del PDF. El documento puede estar protegido o vacío.")

        return {
            "file_name": file_name,
            "page_count": len(page_texts),
            "pages": page_texts,
            "text": full_text,
            "size_bytes": os.path.getsize(temp_path),
        }
    except Exception as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError("No se pudo leer el PDF. Verifica que el archivo no esté dañado o protegido.") from exc
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
