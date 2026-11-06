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


if __name__ == "__main__":
    unittest.main()
