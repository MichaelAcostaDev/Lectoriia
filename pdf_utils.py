import os
import re
import tempfile
import logging
from typing import Dict, List

from pypdf import PdfReader

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024
logger = logging.getLogger(__name__)


class PDFProcessingError(ValueError):
    def __init__(self, message: str, code: str, status_code: int = 400):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def validate_pdf(file_obj, file_name: str) -> None:
    if not file_name.lower().endswith(".pdf"):
        raise PDFProcessingError("The selected file must be a PDF.", "invalid_file_type")

    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    file_obj.seek(0)
    if file_size <= 0:
        raise PDFProcessingError("The PDF file is empty.", "empty_file")
    if file_size > MAX_FILE_SIZE_BYTES:
        raise PDFProcessingError("The PDF exceeds the 15 MB file size limit.", "file_too_large", 413)


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
            raise PDFProcessingError("The PDF does not contain any valid pages.", "invalid_pdf")

        page_texts: List[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            cleaned = re.sub(r"\s+", " ", text).strip()
            page_texts.append(cleaned)

        full_text = "\n\n".join(f"[Página {idx}] {text}" for idx, text in enumerate(page_texts, start=1))
        if not full_text.strip():
            raise PDFProcessingError(
                "No readable text could be extracted. The PDF may be scanned, protected, or empty.",
                "no_extractable_text",
            )

        return {
            "file_name": file_name,
            "page_count": len(page_texts),
            "pages": page_texts,
            "text": full_text,
            "size_bytes": os.path.getsize(temp_path),
        }
    except Exception as exc:
        if isinstance(exc, PDFProcessingError):
            raise
        logger.exception("Could not read uploaded PDF")
        raise PDFProcessingError(
            "The PDF could not be read. Check that the file is valid and not protected.",
            "invalid_pdf",
        ) from exc
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
