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
# URL built after port detection


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, fmt, *args):
        pass


def open_app_mode(url):
    """Open URL without browser chrome (address bar, tabs)."""
    browsers = [
        ("google-chrome-stable", ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("google-chrome",       ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("chromium-browser",    ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("chromium",            ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("brave-browser",       ["--app=" + url, "--window-size=420,620"]),
        ("vivaldi",             ["--app=" + url, "--window-size=420,620"]),
        ("firefox",             ["--new-window", url]),
        ("microsoft-edge",      ["--app=" + url, "--window-size=420,620"]),
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
    # Find available port
    port = PORT
    while True:
        try:
            httpd = socketserver.TCPServer(("", port), QuietHandler)
            break
        except OSError:
            port += 1
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    url = f"http://localhost:{port}/index.html"
    print(f"  passgen — http://localhost:{port}")
    print()

    # Try app mode first
    if not open_app_mode(url):
        webbrowser.open(url)

    print("Press Ctrl+C to stop")

    try:
        signal.pause()
    except KeyboardInterrupt:
        httpd.shutdown()
        print("\nBye!")
