from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(slots=True)
class PredictionResult:
    name: str
    image_path: Path
    ply_path: Path | None
    status: str

    @property
    def has_ply(self) -> bool:
        return self.ply_path is not None and self.ply_path.exists()

    def to_dict(self) -> dict[str, str | None]:
        return {
            "name": self.name,
            "image": str(self.image_path),
            "ply": str(self.ply_path) if self.ply_path is not None else None,
            "status": self.status,
        }


class ResultRepository:
    def __init__(self, uploads_dir: Path, outputs_dir: Path) -> None:
        self.uploads_dir = uploads_dir
        self.outputs_dir = outputs_dir

    def store_upload(self, source_path: Path) -> Path:
        destination = self.uploads_dir / source_path.name
        shutil.copy2(source_path, destination)
        return destination

    def result_path(self, stem: str) -> Path:
        return self.outputs_dir / f"{stem}.ply"

    def existing_result_names(self) -> list[str]:
        return sorted(path.stem for path in self.outputs_dir.glob("*.ply"))
