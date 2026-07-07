import http.server
import socketserver
import webbrowser
import threading
import os

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(DIR, "index.html")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def log_message(self, fmt, *args):
        pass  # quiet


if __name__ == "__main__":
    print("Opening passgen in your browser...")
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
