"""Exercise production configuration without connecting to a real database."""

import json
import os
from pathlib import Path
import subprocess
import sys

from django.test import SimpleTestCase


class DeploymentTests(SimpleTestCase):
    def run_python(self, code, **overrides):
        env = {
            key: value for key, value in os.environ.items()
            if not key.startswith(("DJANGO_", "VERCEL", "AWS_"))
            and key != "DATABASE_URL"
        }
        env.update({
            "PYTHON_DOTENV_DISABLED": "1",
            "DJANGO_SETTINGS_MODULE": "motionfolio.settings",
            "VERCEL": "1",
            "VERCEL_URL": "portfolio-preview.vercel.app",
            "DJANGO_SECRET_KEY": "test-only-" + "x" * 64,
            "DATABASE_URL": "postgresql://user:password@localhost/portfolio?sslmode=require&channel_binding=require",
            **overrides,
        })
        return subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parent.parent,
            env=env, capture_output=True, text=True, timeout=30,
        )

    def test_production_rejects_missing_secrets_debug_and_nonpersistent_database(self):
        cases = [
            ({"DJANGO_SECRET_KEY": ""}, "DJANGO_SECRET_KEY is required"),
            ({"DATABASE_URL": ""}, "persistent PostgreSQL"),
            ({"DATABASE_URL": "sqlite:///:memory:"}, "persistent PostgreSQL"),
            ({"DJANGO_DEBUG": "1"}, "Set DJANGO_DEBUG=0"),
        ]
        for overrides, message in cases:
            with self.subTest(overrides=overrides):
                result = self.run_python("import motionfolio.settings", **overrides)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)

    def test_vercel_domains_and_postgres_options(self):
        result = self.run_python(
            "import json; from motionfolio import settings as s; "
            "print(json.dumps([s.DEBUG, s.ALLOWED_HOSTS, s.CSRF_TRUSTED_ORIGINS, s.DATABASES['default']]))",
            DJANGO_ALLOWED_HOSTS="portfolio.example.com",
            DJANGO_CSRF_TRUSTED_ORIGINS="https://portfolio.example.com",
            VERCEL_PROJECT_PRODUCTION_URL="portfolio.vercel.app",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        debug, hosts, origins, database = json.loads(result.stdout)
        self.assertFalse(debug)
        self.assertIn("portfolio-preview.vercel.app", hosts)
        self.assertIn("portfolio.example.com", hosts)
        self.assertIn("https://portfolio.vercel.app", origins)
        self.assertIn("https://portfolio.example.com", origins)
        self.assertEqual(database["OPTIONS"]["channel_binding"], "require")
        self.assertEqual(database["OPTIONS"]["sslmode"], "require")
        self.assertEqual(database["CONN_MAX_AGE"], 0)
        self.assertTrue(database["DISABLE_SERVER_SIDE_CURSORS"])

    def test_local_mode_works_without_database_or_secret(self):
        result = self.run_python(
            "from motionfolio import settings as s; "
            "assert s.DEBUG; assert s.DATABASES['default']['ENGINE'].endswith('sqlite3')",
            VERCEL="", DATABASE_URL="", DJANGO_SECRET_KEY="",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_https_proxy_does_not_create_a_redirect_loop(self):
        result = self.run_python("""
import django
django.setup()
from django.http import HttpResponse
from django.middleware.security import SecurityMiddleware
from django.test import RequestFactory
middleware = SecurityMiddleware(lambda request: HttpResponse('OK'))
factory = RequestFactory()
request = factory.get('/', HTTP_HOST='portfolio-preview.vercel.app', HTTP_X_FORWARDED_PROTO='https')
assert request.is_secure()
assert middleware(request).status_code == 200
request = factory.get('/', HTTP_HOST='portfolio-preview.vercel.app')
assert middleware(request).status_code == 301
""")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cloud_media_generates_signed_urls_without_local_disk(self):
        result = self.run_python("""
import django
django.setup()
from django.core.files.storage import default_storage
url = default_storage.url('projects/cover.png')
assert url.startswith('https://')
assert '/media/projects/cover.png' in url
assert 'X-Amz-Signature=' in url
""",
            AWS_STORAGE_BUCKET_NAME="portfolio-test",
            AWS_ACCESS_KEY_ID="test-access-key",
            AWS_SECRET_ACCESS_KEY="test-secret-key",
            AWS_S3_REGION_NAME="auto",
            AWS_S3_ENDPOINT_URL="https://storage.example.com",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
