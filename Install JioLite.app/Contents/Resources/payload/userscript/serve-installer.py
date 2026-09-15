#!/usr/bin/env python3
"""Serve JioLite.user.js briefly and open its Violentmonkey install page."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import threading
from urllib.parse import urlsplit


USERSCRIPT_PATH = Path(__file__).with_name("JioLite.user.js")
MAXIMUM_LIFETIME_SECONDS = 300
POST_REQUEST_LIFETIME_SECONDS = 90


class UserscriptHandler(BaseHTTPRequestHandler):
    shutdown_scheduled = False

    def do_GET(self):
        if urlsplit(self.path).path not in {"/", "/JioLite.user.js"}:
            self.send_error(404)
            return

        script = USERSCRIPT_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Content-Length", str(len(script)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(script)

        if not type(self).shutdown_scheduled:
            type(self).shutdown_scheduled = True
            timer = threading.Timer(POST_REQUEST_LIFETIME_SECONDS, self.server.shutdown)
            timer.daemon = True
            timer.start()

    def log_message(self, format_string, *args):
        print(f"{self.client_address[0]} - {format_string % args}", flush=True)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), UserscriptHandler)
    maximum_lifetime = threading.Timer(MAXIMUM_LIFETIME_SECONDS, server.shutdown)
    maximum_lifetime.daemon = True
    maximum_lifetime.start()

    port = server.server_address[1]
    install_url = f"http://127.0.0.1:{port}/JioLite.user.js"
    subprocess.run(["/usr/bin/open", install_url], check=True)
    server.serve_forever()
    server.server_close()


if __name__ == "__main__":
    main()
