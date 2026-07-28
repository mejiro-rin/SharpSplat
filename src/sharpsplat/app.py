from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from sharpsplat.config import AppSettings, discover_paths
    from sharpsplat.predictor import SharpPredictor
    from sharpsplat.repository import ResultRepository
    from sharpsplat.ui import SharpSplatUI
    from sharpsplat.viewer import ViewerServer
else:
    from .config import AppSettings, discover_paths
    from .predictor import SharpPredictor
    from .repository import ResultRepository
    from .ui import SharpSplatUI
    from .viewer import ViewerServer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SharpSplatApp:
    """主应用程序类，封装了所有组件的初始化和启动逻辑。"""
    def __init__(self, settings: AppSettings | None = None) -> None:
        self.settings = settings or AppSettings()
        self.paths = discover_paths()
        self.repository = ResultRepository(self.paths.uploads_dir, self.paths.outputs_dir)
        self.predictor = SharpPredictor(
            repository=self.repository,
            timeout_seconds=self.settings.sharp_timeout_seconds,
            device=self.settings.sharp_device,
        )
        self.viewer = ViewerServer(self.paths.base_dir)
        self.ui = SharpSplatUI(self.predictor, self.repository, self.viewer)

    def launch(self, ui_port: int, share: bool = False) -> None:
        # use a far offset so Gradio's auto-increment never collides
        viewer_port = self.settings.viewer_port or (ui_port + 100)
        self.viewer.start(viewer_port)
        ui = self.ui.build()
        ui.queue()
        logger.info("viewer on port %d", viewer_port)
        ui.launch(server_port=ui_port, share=share)


def main() -> None:
    """应用程序的入口点，解析命令行参数并启动应用程序。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=AppSettings().ui_port)
    parser.add_argument("--share", action="store_true")
    arguments = parser.parse_args()

    app = SharpSplatApp()
    app.launch(arguments.port, arguments.share)


if __name__ == "__main__":
    main()
