"""PyAV tabanlı güvenli video okuyucu."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

import av
import numpy as np
from numpy.typing import NDArray


class VideoReader:
    """Videoyu açar, kare sayısını güvenli şekilde tahmin eder ve kareleri iterler."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Video bulunamadı: {self.path}")

        self.container = av.open(str(self.path))
        self.stream = self.container.streams.video[0]
        self._total_frames = self._estimate_total_frames()
        self._fps = float(self.stream.average_rate) if self.stream.average_rate else 25.0

    def _estimate_total_frames(self) -> int:
        total = self.stream.frames
        if total and total > 0:
            return total

        duration = self.stream.duration
        time_base = self.stream.time_base
        avg_rate = self.stream.average_rate
        if duration and time_base and avg_rate:
            return int(float(duration * time_base) * float(avg_rate))

        # Son çare: kareleri say
        total = sum(1 for _ in self.container.decode(video=0))
        self.container.seek(0)
        return total or 1

    @property
    def total_frames(self) -> int:
        return self._total_frames

    @property
    def fps(self) -> float:
        return self._fps

    def duration_seconds(self) -> float:
        return self._total_frames / self._fps if self._fps else 0.0

    def iter_frames(self, max_frames: int | None = None) -> Iterator[NDArray[np.uint8]]:
        """RGB24 numpy dizisi olarak kareleri döner."""
        self.container.seek(0)
        count = 0
        for frame in self.container.decode(video=0):
            yield frame.to_ndarray(format="rgb24")
            count += 1
            if max_frames is not None and count >= max_frames:
                break

    def close(self) -> None:
        self.container.close()

    def __enter__(self) -> VideoReader:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
