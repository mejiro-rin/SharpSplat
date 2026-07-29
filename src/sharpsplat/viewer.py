from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from urllib.parse import quote


class QuietStaticHandler(SimpleHTTPRequestHandler):
    """
    静态文件处理程序，继承自SimpleHTTPRequestHandler，用于提供静态文件服务。
    重写了log_message方法，以抑制日志输出。
    """
    def log_message(self, *args):
        pass


class ViewerServer:
    """
    3D查看器服务器类，用于启动和管理静态文件服务。
    """
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self._server: ThreadingHTTPServer | None = None
        self.port: int | None = None

    def start(self, port: int) -> None:
        """
        启动静态文件服务器，监听指定端口。
        """
        self.port = port
        handler = partial(QuietStaticHandler, directory=str(self.root_dir))
        self._server = ThreadingHTTPServer(("", port), handler)
        thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        thread.start()

    def viewer_url(self, ply_name: str) -> str:
        """
        返回3D查看器的URL，用于在UI中显示指定的PLY文件。
        """
        if self.port is None:
            raise RuntimeError("viewer server is not started")
        relative_file = quote(f"/outputs/{ply_name}.ply")
        return f"http://localhost:{self.port}/static/spark/viewer.html?file={relative_file}"
