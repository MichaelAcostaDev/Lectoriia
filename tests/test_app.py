import io
import os
import unittest
from unittest.mock import patch

from app import app


class FlaskRoutesTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_health_endpoint_reports_local_non_ai_analysis(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")
        self.assertEqual(response.get_json()["application"], "operational")
        self.assertEqual(
            response.get_json()["analysis"],
            {"mode": "local", "external_model": False},
        )

    def test_legacy_ai_health_endpoint_reports_local_engine_without_authentication(self):
        response = self.client.post("/api/health/ai")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["analysis"],
            {"mode": "local", "available": True, "external_model": False},
        )

    def test_analyze_endpoint_returns_local_results_without_credentials(self):
        response = self.client.post(
            "/api/analyze-text",
            json={"text": "La ciencia estudia la naturaleza y sus fenómenos."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["summary"]["source"], "local")
        self.assertEqual(response.get_json()["summary"]["model"], "Local")
        self.assertEqual(response.get_json()["classification"]["source"], "local")

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

    def test_adsense_defaults_to_configured_publisher_and_auto_ads(self):
        with patch.dict(os.environ, {}, clear=True):
            home = self.client.get("/")
            ads_txt = self.client.get("/ads.txt")

        self.assertIn(b'"publisherId": "ca-pub-9460130837910562"', home.data)
        self.assertIn(b'"autoAds": true', home.data)
        self.assertIn(
            b"google.com, pub-9460130837910562, DIRECT, f08c47fec0942fa0",
            ads_txt.data,
        )

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
