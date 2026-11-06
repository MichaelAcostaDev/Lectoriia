import io
import os
import unittest
from unittest.mock import patch

from ai_utils import AIServiceError
from app import app


class FlaskRoutesTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_analyze_endpoint_reports_provider_configuration_errors(self):
        error = AIServiceError("AI token is missing.", "missing_token", 503)
        with patch("app.analyze_document", side_effect=error):
            response = self.client.post("/api/analyze-text", json={"text": "A document."})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()["code"], "missing_token")

    def test_analysis_rejects_non_string_document_text(self):
        response = self.client.post("/api/analyze-text", json={"text": 42})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["code"], "invalid_request")

    def test_invalid_json_body_returns_a_client_error(self):
        response = self.client.post("/api/analyze-text", data="not json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["code"], "invalid_request")

    def test_home_uses_accept_language_for_initial_document_language(self):
        response = self.client.get("/", headers={"Accept-Language": "es"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html lang="es">', response.data)

    def test_missing_publisher_id_does_not_create_ads_txt_in_production(self):
        with patch.dict(
            os.environ,
            {
                "VERCEL": "1",
                "ADSENSE_PUBLISHER_ID": "",
                "ADSENSE_SLOT_HERO": "",
                "ADSENSE_SLOT_MIDDLE": "",
                "ADSENSE_SLOT_SIDEBAR": "",
                "ADSENSE_SLOT_FOOTER": "",
            },
        ):
            response = self.client.get("/ads.txt")

        self.assertEqual(response.status_code, 404)

    def test_pdf_upload_rejects_empty_file_with_a_specific_error(self):
        response = self.client.post(
            "/api/upload-pdf",
            data={"file": (io.BytesIO(b""), "empty.pdf")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["code"], "empty_file")


if __name__ == "__main__":
    unittest.main()
