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
        self.assertEqual(response.get_json()["status"], "ok")
        self.assertEqual(response.get_json()["application"], "operational")
        self.assertIn("credentials_configured", response.get_json()["ai"])
        self.assertEqual(response.get_json()["ai"]["provider_reachable"], "not_checked")

    def test_ai_health_requires_authorization(self):
        with (
            patch("app.get_hf_token", return_value="test-token"),
            patch("app._call_chat") as call_chat,
        ):
            response = self.client.post("/api/health/ai")

        self.assertEqual(response.status_code, 401)
        call_chat.assert_not_called()
        self.assertNotIn(b"test-token", response.data)

    def test_ai_health_runs_a_minimal_model_check_when_authorized(self):
        with (
            patch("app.get_hf_token", return_value="test-token"),
            patch("app._call_chat", return_value="OK") as call_chat,
        ):
            response = self.client.post(
                "/api/health/ai",
                headers={"Authorization": "Bearer test-token"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["ai"],
            {
                "credentials_configured": True,
                "provider_reachable": True,
                "model_operational": True,
            },
        )
        call_chat.assert_called_once()

    def test_ai_health_fails_explicitly_when_token_is_missing(self):
        with (
            patch("app.get_hf_token", return_value=""),
            patch("app._call_chat") as call_chat,
        ):
            response = self.client.post("/api/health/ai")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()["error_code"], "missing_token")
        self.assertEqual(response.get_json()["ai"]["provider_reachable"], "not_checked")
        call_chat.assert_not_called()

    def test_ai_health_does_not_claim_provider_is_unreachable_on_timeout(self):
        error = AIServiceError("Provider timeout.", "provider_timeout", 504)
        with (
            patch("app.get_hf_token", return_value="test-token"),
            patch("app._call_chat", side_effect=error),
        ):
            response = self.client.post(
                "/api/health/ai",
                headers={"Authorization": "Bearer test-token"},
            )

        self.assertEqual(response.status_code, 504)
        self.assertEqual(response.get_json()["ai"]["provider_reachable"], "unknown")
        self.assertNotIn(b"Provider timeout", response.data)

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

    def test_adsense_pub_id_is_normalized_for_ads_script_and_ads_txt(self):
        with patch.dict(
            os.environ,
            {
                "VERCEL": "1",
                "ADSENSE_PUBLISHER_ID": "pub-1234567890123456",
                "ADSENSE_SLOT_HERO": "1234567890",
                "ADSENSE_SLOT_MIDDLE": "",
                "ADSENSE_SLOT_SIDEBAR": "",
                "ADSENSE_SLOT_FOOTER": "",
            },
        ):
            home = self.client.get("/")
            ads_txt = self.client.get("/ads.txt")

        self.assertIn(b"ca-pub-1234567890123456", home.data)
        self.assertIn(
            b"google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0",
            ads_txt.data,
        )
        self.assertEqual(ads_txt.mimetype, "text/plain")
        self.assertEqual(ads_txt.headers["Cache-Control"], "no-store")

    def test_auto_ads_can_be_enabled_without_manual_slots(self):
        with patch.dict(
            os.environ,
            {
                "ADSENSE_PUBLISHER_ID": "pub-1234567890123456",
                "ADSENSE_AUTO_ADS": "true",
                "ADSENSE_SLOT_HERO": "",
                "ADSENSE_SLOT_MIDDLE": "",
                "ADSENSE_SLOT_SIDEBAR": "",
                "ADSENSE_SLOT_FOOTER": "",
            },
        ):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"autoAds": true', response.data)

    def test_privacy_page_is_bilingual_and_contact_is_optional(self):
        with patch.dict(os.environ, {"PRIVACY_CONTACT_EMAIL": ""}):
            spanish = self.client.get("/privacy", headers={"Accept-Language": "es"})
            english = self.client.get("/privacy", headers={"Accept-Language": "en"})

        self.assertIn("lang=\"es\"".encode(), spanish.data)
        self.assertIn("Privacidad".encode(), spanish.data)
        self.assertIn("lang=\"en\"".encode(), english.data)
        self.assertIn(b"PRIVACY_CONTACT_EMAIL", english.data)

    def test_ads_txt_without_publisher_is_not_cached(self):
        with patch.dict(os.environ, {"ADSENSE_PUBLISHER_ID": ""}):
            response = self.client.get("/ads.txt")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "text/plain")
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_pdf_upload_rejects_empty_file_with_a_specific_error(self):
        response = self.client.post(
            "/api/upload-pdf",
            data={"file": (io.BytesIO(b""), "empty.pdf")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["code"], "empty_file")

    def test_pdf_upload_rejects_files_over_configured_limit(self):
        with patch("pdf_utils.MAX_FILE_SIZE_BYTES", 1):
            response = self.client.post(
                "/api/upload-pdf",
                data={"file": (io.BytesIO(b"pdf"), "large.pdf")},
                content_type="multipart/form-data",
            )

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json()["code"], "file_too_large")


if __name__ == "__main__":
    unittest.main()
