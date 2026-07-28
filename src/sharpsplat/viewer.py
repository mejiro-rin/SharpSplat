from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from urllib.parse import quote


class QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class ViewerServer:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self._server: ThreadingHTTPServer | None = None
        self.port: int | None = None

    def start(self, port: int) -> None:
        self.port = port
        handler = partial(QuietStaticHandler, directory=str(self.root_dir))
        self._server = ThreadingHTTPServer(("", port), handler)
        thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        thread.start()

    def viewer_url(self, ply_name: str) -> str:
        if self.port is None:
            raise RuntimeError("viewer server is not started")
        relative_file = quote(f"/outputs/{ply_name}.ply")
        return f"http://localhost:{self.port}/static/spark/viewer.html?file={relative_file}"
