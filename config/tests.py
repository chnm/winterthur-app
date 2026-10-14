from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.http import HttpResponseNotFound
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import reverse
from whitenoise.middleware import WhiteNoiseMiddleware


class HealthCheckTests(SimpleTestCase):
    @patch("config.views.connection.ensure_connection")
    def test_health_check(self, ensure_connection):
        response = self.client.get(reverse("health"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "code": 200})

    @patch(
        "config.views.connection.ensure_connection",
        side_effect=Exception("connection refused"),
    )
    def test_health_check_reports_unreachable_database(self, ensure_connection):
        response = self.client.get(reverse("health"), secure=True)

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["status"], "error")


class ProductionStaticFilesTests(SimpleTestCase):
    def test_whitenoise_follows_security_middleware(self):
        security = "django.middleware.security.SecurityMiddleware"
        whitenoise = "whitenoise.middleware.WhiteNoiseMiddleware"

        self.assertEqual(
            settings.MIDDLEWARE[settings.MIDDLEWARE.index(security) + 1], whitenoise
        )

    def test_whitenoise_serves_collected_static_file(self):
        with TemporaryDirectory() as static_root:
            stylesheet = Path(static_root) / "css" / "test.css"
            stylesheet.parent.mkdir(parents=True)
            stylesheet.write_text("body { color: black; }", encoding="utf-8")

            with override_settings(DEBUG=False, STATIC_ROOT=static_root):
                middleware = WhiteNoiseMiddleware(
                    lambda request: HttpResponseNotFound()
                )
                response = middleware(RequestFactory().get("/static/css/test.css"))
                try:
                    content = b"".join(response.streaming_content)
                finally:
                    response.close()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, b"body { color: black; }")
