from __future__ import annotations

from pathlib import Path
import subprocess

from .repository import PredictionResult, ResultRepository


class SharpPredictor:
    def __init__(self, repository: ResultRepository, timeout_seconds: int, device: str) -> None:
        self.repository = repository
        self.timeout_seconds = timeout_seconds
        self.device = device

    def predict_many(self, image_paths, progress=None) -> list[PredictionResult]:
        results: list[PredictionResult] = []
        iterable = progress.tqdm(image_paths) if progress is not None else image_paths

        for source in iterable:
            source_path = Path(getattr(source, "name", source))
            copied_path = self.repository.store_upload(source_path)
            result_path = self.repository.result_path(source_path.stem)

            try:
                subprocess.run(
                    [
                        "sharp",
                        "predict",
                        "-i",
                        str(copied_path),
                        "-o",
                        str(self.repository.outputs_dir),
                        "--device",
                        self.device,
                        "--no-render",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                )
                status = "done" if result_path.exists() else "failed"
                ply_path = result_path if result_path.exists() else None
            except subprocess.TimeoutExpired:
                status = "timeout"
                ply_path = None
            except subprocess.CalledProcessError:
                status = "failed"
                ply_path = None
            except FileNotFoundError:
                raise FileNotFoundError("sharp not found") from None

            results.append(
                PredictionResult(
                    name=source_path.stem,
                    image_path=copied_path,
                    ply_path=ply_path,
                    status=status,
                )
            )

        return results
