from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppPaths:
    base_dir: Path
    outputs_dir: Path
    uploads_dir: Path
    static_dir: Path
    spark_dir: Path


@dataclass(frozen=True, slots=True)
class AppSettings:
    ui_port: int = 7860
    viewer_port: int | None = None
    sharp_timeout_seconds: int = 600
    sharp_device: str = "default"


def discover_paths() -> AppPaths:
    base_dir = Path(__file__).resolve().parent.parent.parent
    outputs_dir = base_dir / "outputs"
    uploads_dir = base_dir / "uploads"
    static_dir = base_dir / "static"
    spark_dir = static_dir / "spark"

    outputs_dir.mkdir(exist_ok=True)
    uploads_dir.mkdir(exist_ok=True)

    return AppPaths(
        base_dir=base_dir,
        outputs_dir=outputs_dir,
        uploads_dir=uploads_dir,
        static_dir=static_dir,
        spark_dir=spark_dir,
    )
