from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(slots=True)
class PredictionResult:
    """
    表示单个预测结果的类，包含结果的名称、图像路径、PLY文件路径和状态。
    """
    name: str
    image_path: Path
    ply_path: Path | None
    status: str

    @property
    def has_ply(self) -> bool:
        """
        检查预测结果是否包含有效的PLY文件。
        """
        return self.ply_path is not None and self.ply_path.exists()

    def to_dict(self) -> dict[str, str | None]:
        """
        将预测结果转换为字典格式，便于在UI中使用。
        """
        return {
            "name": self.name,
            "image": str(self.image_path),
            "ply": str(self.ply_path) if self.ply_path is not None else None,
            "status": self.status,
        }


class ResultRepository:
    """
    结果存储库类，负责管理上传的图像和预测结果的存储。
    """
    def __init__(self, uploads_dir: Path, outputs_dir: Path) -> None:
        self.uploads_dir = uploads_dir
        self.outputs_dir = outputs_dir

    def store_upload(self, source_path: Path) -> Path:
        """
        将上传的图像文件存储到指定的上传目录中，并返回存储后的路径。
        """
        destination = self.uploads_dir / source_path.name
        shutil.copy2(source_path, destination)
        return destination

    def result_path(self, stem: str) -> Path:
        """
        根据结果的名称生成对应的PLY文件路径。
        """
        return self.outputs_dir / f"{stem}.ply"

    def existing_result_names(self) -> list[str]:
        """
        扫描输出目录中的现有PLY文件，并返回一个包含结果名称的列表。
        """
        return sorted(path.stem for path in self.outputs_dir.glob("*.ply"))
