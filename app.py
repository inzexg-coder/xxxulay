import webview
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import generate_password
from settings import load_services, save_services, load_settings, save_settings


class API:
    """Exposed to JavaScript via pywebview.api."""

    def __init__(self):
        self._services = load_services()

    def get_services(self):
        return json.dumps(self._services)

    def save_service(self, name):
        if name and name not in self._services:
            self._services.append(name)
            save_services(self._services)

    def get_settings(self):
        s = load_settings()
        return json.dumps(s)

    def save_settings(self, length, capitals, lower, digits, symbols):
        save_settings(length, capitals, lower, digits, symbols)

    def generate(self, seed, service, length, capitals, lower, digits, symbols):
        try:
            pwd = generate_password(
                master_seed=seed, service=service,
                length=length,
                use_capitals=capitals,
                use_lower=lower,
                use_digits=digits,
                use_symbols=symbols,
            )
            return json.dumps({"ok": True, "password": pwd})
        except ValueError as e:
            return json.dumps({"ok": False, "error": str(e)})


if __name__ == "__main__":
    api = API()
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

    window = webview.create_window(
        title="passgen",
        url=html_path,
        js_api=api,
        width=420,
        height=580,
        resizable=False,
    )
    webview.start()
