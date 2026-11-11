import sys
import os
from pathlib import Path

# Signal Vercel serverless environment
os.environ["VERCEL"] = "1"

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import app


class VercelPathMiddleware:
    """
    WSGI Middleware to fix URL routing on Vercel.
    When Vercel routes traffic through /api/index or /api/index.py,
    PATH_INFO can become '/api/index', causing Flask to return 404.
    This middleware restores the original requested path from Vercel headers.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path in ("/api/index", "/api/index.py", "/api"):
            real_path = (
                environ.get("HTTP_X_FORWARDED_URI")
                or environ.get("HTTP_X_MATCHED_PATH")
                or environ.get("HTTP_X_NOW_ROUTE_MATCHES")
                or "/"
            )
            # Remove query strings if present in the header
            if "?" in real_path:
                real_path = real_path.split("?", 1)[0]
            if real_path.startswith("/api/index") or not real_path:
                real_path = "/"
            environ["PATH_INFO"] = real_path
        return self.wsgi_app(environ, start_response)


# Wrap Flask with the Vercel routing middleware
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
