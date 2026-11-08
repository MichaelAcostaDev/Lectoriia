import unittest
from unittest.mock import patch

import ai_utils


class DocumentChunkingTests(unittest.TestCase):
    def test_chunks_preserve_pdf_page_references(self):
        chunks = ai_utils.chunk_document(
            "",
            pages=["A " * 800, "B " * 650],
            max_chars=500,
            overlap=50,
        )

        self.assertGreater(len(chunks), 2)
        self.assertEqual({chunk["page_start"] for chunk in chunks}, {1, 2})
        self.assertTrue(all(chunk["page_start"] == chunk["page_end"] for chunk in chunks))
        page_one_text = " ".join(chunk["text"] for chunk in chunks if chunk["page_start"] == 1)
        page_two_text = " ".join(chunk["text"] for chunk in chunks if chunk["page_start"] == 2)
        self.assertGreaterEqual(page_one_text.count("A"), 800)
        self.assertGreaterEqual(page_two_text.count("B"), 650)

    def test_oversized_document_returns_explicit_error(self):
        with patch.object(ai_utils, "MAX_DOCUMENT_CHARS", 5):
            with self.assertRaises(ai_utils.AIServiceError) as error:
                ai_utils.chunk_document("123456")

        self.assertEqual(error.exception.code, "document_too_large")
        self.assertEqual(error.exception.status_code, 413)

    def test_extracts_page_markers_from_legacy_document_text(self):
        chunks = ai_utils.chunk_document("[Página 2] Second page.\n[Página 3] Third page.")

        self.assertEqual([chunk["page_start"] for chunk in chunks], [2, 3])


class LocalAnalysisTests(unittest.TestCase):
    def test_analysis_is_local_and_returns_summary_keywords_and_topics(self):
        text = (
            "La educación ayuda a los estudiantes. "
            "Los estudiantes aprenden en la escuela y la universidad."
        )

        result = ai_utils.analyze_document(text)

        self.assertEqual(result["summary"]["summary"], text)
        self.assertIn("estudiantes", result["keywords"]["keywords"])
        self.assertEqual(result["classification"]["labels"][0]["label"], "Education")
        self.assertEqual(result["summary"]["source"], "local")
        self.assertEqual(result["keywords"]["source"], "local")
        self.assertEqual(result["classification"]["source"], "local")
        self.assertEqual(result["summary"]["model"], "Local")
        self.assertEqual(result["language"], "es")

    def test_pdf_references_are_preserved_for_analysis(self):
        result = ai_utils.analyze_document(
            "",
            pages=[
                "La historia describe una antigua ciudad.",
                "La educación se impartía en la escuela.",
            ],
        )

        self.assertEqual(result["summary"]["references"], [1, 2])
        self.assertEqual(result["summary"]["chunks_count"], 2)

    def test_summary_selects_relevant_sentences_for_long_documents(self):
        text = (
            "Los volcanes expulsan lava durante las erupciones. "
            "La lava puede alcanzar temperaturas muy altas y transformar el terreno. "
            "Los volcanes se forman por el movimiento de placas tectónicas. "
        ) * 12

        result = ai_utils.summarize_text(text)

        self.assertLess(len(result["summary"]), len(text))
        self.assertIn("volcanes", result["summary"])
        self.assertEqual(result["source"], "local")

    def test_question_answers_with_matching_extracts_and_page_reference(self):
        result = ai_utils.answer_question(
            "¿Qué estudian los investigadores?",
            "",
            pages=[
                "La investigación analiza el clima y la temperatura.",
                "Los investigadores estudian cómo cambia el clima en verano.",
            ],
        )

        self.assertIn("investigadores estudian", result["answer"])
        self.assertEqual(result["references"], [2])
        self.assertEqual(result["source"], "local")

    def test_question_reports_insufficient_evidence_without_inventing_answer(self):
        result = ai_utils.answer_question(
            "¿Quién ganó el torneo?",
            "El documento describe el clima y las estaciones del año.",
        )

        self.assertIn("No encuentro evidencia suficiente", result["answer"])
        self.assertEqual(result["references"], [])

    def test_analysis_has_no_external_http_client_dependency(self):
        result = ai_utils.analyze_document(
            "La ciencia estudia la naturaleza y sus fenómenos."
        )
        self.assertEqual(result["summary"]["source"], "local")
        self.assertFalse(hasattr(ai_utils, "requests"))

    def test_empty_document_is_rejected(self):
        with self.assertRaises(ai_utils.AIServiceError) as error:
            ai_utils.analyze_document("")

        self.assertEqual(error.exception.code, "empty_document")
        self.assertEqual(error.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
