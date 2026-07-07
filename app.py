#!/usr/bin/env python3
"""passgen — desktop app (no browser chrome)"""

import http.server
import socketserver
import webbrowser
import subprocess
import shutil
import threading
import os
import sys
import signal

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))
URL = f"http://localhost:{PORT}/index.html"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, fmt, *args):
        pass


def open_app_mode(url):
    """Open URL without browser chrome (address bar, tabs)."""
    browsers = [
        ("google-chrome-stable", ["--app=" + url, "--window-size=420,580", "--no-first-run"]),
        ("google-chrome",       ["--app=" + url, "--window-size=420,580", "--no-first-run"]),
        ("chromium-browser",    ["--app=" + url, "--window-size=420,580", "--no-first-run"]),
        ("chromium",            ["--app=" + url, "--window-size=420,580", "--no-first-run"]),
        ("brave-browser",       ["--app=" + url, "--window-size=420,580"]),
        ("vivaldi",             ["--app=" + url, "--window-size=420,580"]),
        ("firefox",             ["--new-window", url]),
        ("microsoft-edge",      ["--app=" + url, "--window-size=420,580"]),
    ]
    for name, args in browsers:
        path = shutil.which(name)
        if path:
            subprocess.Popen([path] + args,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            return True
    return False


if __name__ == "__main__":
    # Start HTTP server
    httpd = socketserver.TCPServer(("", PORT), QuietHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    print(f"  passgen — http://localhost:{PORT}")
    print()

    # Try app mode first
    if not open_app_mode(URL):
        webbrowser.open(URL)

    print("Press Ctrl+C to stop")

    try:
        signal.pause()
    except KeyboardInterrupt:
        httpd.shutdown()
        print("\nBye!")
