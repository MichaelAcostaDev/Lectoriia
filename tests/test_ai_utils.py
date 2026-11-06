import unittest
from unittest.mock import Mock, patch

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


class AIAnalysisTests(unittest.TestCase):
    def test_analysis_consolidates_all_pages_and_returns_thematic_labels(self):
        final_result = {
            "summary": "A document about learning and schools.",
            "keywords": ["learning", "schools"],
            "classification": [
                {"label": "Education", "score": 0.94},
                {"label": "neutral", "score": 0.6},
            ],
            "language": "en",
        }
        with (
            patch.object(
                ai_utils,
                "_map_chunks",
                side_effect=lambda chunks: [
                    {
                        "summary": f"Page {chunk['page_start']} summary.",
                        "keywords": ["learning" if chunk["page_start"] == 1 else "schools"],
                    }
                    for chunk in chunks
                ],
            ) as map_chunks,
            patch.object(ai_utils, "_reduce_summaries", return_value="Document summary."),
            patch.object(ai_utils, "_run_json", return_value=final_result),
        ):
            result = ai_utils.analyze_document("", pages=["First page", "Second page"])

        self.assertEqual(map_chunks.call_count, 1)
        self.assertEqual(result["summary"]["references"], [1, 2])
        self.assertEqual(result["summary"]["chunks_count"], 2)
        self.assertEqual(result["keywords"]["keywords"], ["learning", "schools"])
        self.assertEqual(result["classification"]["labels"], [{"label": "Education", "score": 0.94}])
        self.assertEqual(result["classification"]["source"], "huggingface")

    def test_follow_up_questions_use_real_chat_roles_and_valid_page_citations(self):
        messages_seen = []
        token_limits = []

        def fake_chat(messages, max_tokens=900):
            messages_seen.extend(messages)
            token_limits.append(max_tokens)
            return '{"answer":"The report describes a river study [p. 2].","references":[2,99]}'

        with patch.object(ai_utils, "_call_chat", side_effect=fake_chat):
            result = ai_utils.answer_question(
                "What does the report study?",
                "[Página 1] A history of music.\n[Página 2] The report studies a river.",
                history=[
                    {"role": "user", "content": "Summarize it."},
                    {"role": "assistant", "content": "It covers two topics."},
                ],
            )

        self.assertEqual([message["role"] for message in messages_seen], ["system", "user", "assistant", "user"])
        self.assertEqual(token_limits, [900])
        self.assertEqual(result["references"], [2])
        self.assertEqual(result["source"], "huggingface")

    def test_unavailable_token_does_not_produce_a_heuristic_answer(self):
        with patch.object(ai_utils, "HF_TOKEN", ""):
            with self.assertRaises(ai_utils.AIServiceError) as error:
                ai_utils._call_chat([{"role": "user", "content": "test"}])

        self.assertEqual(error.exception.code, "missing_token")
        self.assertEqual(error.exception.status_code, 503)

    def test_chat_request_uses_openai_compatible_roles_and_model(self):
        response = Mock()
        response.ok = True
        response.json.return_value = {"choices": [{"message": {"content": "Answer"}}]}
        messages = [
            {"role": "system", "content": "Rules"},
            {"role": "user", "content": "Question"},
        ]
        with (
            patch.object(ai_utils, "HF_TOKEN", "test-token"),
            patch.object(ai_utils.requests, "post", return_value=response) as post,
        ):
            content = ai_utils._call_chat(messages)

        self.assertEqual(content, "Answer")
        self.assertEqual(
            post.call_args.args[0],
            "https://router.huggingface.co/v1/chat/completions",
        )
        self.assertEqual(post.call_args.kwargs["json"]["messages"], messages)
        self.assertEqual(post.call_args.kwargs["json"]["model"], ai_utils.DEFAULT_CHAT_MODEL)

    def test_provider_rate_limit_has_a_retryable_error_code(self):
        response = Mock()
        response.ok = False
        response.status_code = 429
        response.json.return_value = {"error": "rate limit"}
        with (
            patch.object(ai_utils, "HF_TOKEN", "test-token"),
            patch.object(ai_utils.requests, "post", return_value=response),
        ):
            with self.assertRaises(ai_utils.AIServiceError) as error:
                ai_utils._call_chat([{"role": "user", "content": "test"}])

        self.assertEqual(error.exception.code, "provider_rate_limit")
        self.assertEqual(error.exception.status_code, 429)


if __name__ == "__main__":
    unittest.main()
