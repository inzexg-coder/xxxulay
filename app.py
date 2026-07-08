import http.server
import socketserver
import webbrowser
import subprocess
import shutil
import threading
import os
import sys

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, fmt, *args):
        pass


def open_app_mode(url):
    browsers = [
        ("google-chrome-stable", ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("google-chrome",       ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("chromium-browser",    ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("chromium",            ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("brave-browser",       ["--app=" + url, "--window-size=420,620"]),
        ("brave",               ["--app=" + url, "--window-size=420,620"]),
        ("vivaldi",             ["--app=" + url, "--window-size=420,620"]),
        ("chrome",              ["--app=" + url, "--window-size=420,620", "--no-first-run"]),
        ("msedge",              ["--app=" + url, "--window-size=420,620"]),
        ("microsoft-edge",      ["--app=" + url, "--window-size=420,620"]),
        ("firefox",             ["--new-window", url]),
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

    if not open_app_mode(url):
        webbrowser.open(url)

    print("Press Ctrl+C to stop")

    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        httpd.shutdown()
        print("\nBye!")
