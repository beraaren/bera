"""Akıllı kare örnekleme: SSIM + Laplacian varyansı."""
from __future__ import annotations

from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray
from skimage.metrics import structural_similarity as ssim


class FrameSampler:
    """Videodan tekrarlı/bulanık kareleri atarak en bilgilendirici kareleri seçer."""

    def __init__(
        self,
        target_count: int = 8,
        use_smart_sampling: bool = True,
        ssim_threshold: float = 0.92,
        min_laplacian_variance: float = 80.0,
    ):
        self.target_count = target_count
        self.use_smart_sampling = use_smart_sampling
        self.ssim_threshold = ssim_threshold
        self.min_laplacian_variance = min_laplacian_variance

    def sample(self, frames: List[NDArray[np.uint8]], total_frames: int) -> Tuple[List[NDArray[np.uint8]], List[int]]:
        if not frames:
            return [], []

        # Tempsel olarak eşit aralıklı indeksler
        indices = np.linspace(0, total_frames - 1, self.target_count, dtype=int).tolist()

        # Videodan ilgili kareleri çıkar (en yakın decoded kare)
        sampled = []
        for idx in indices:
            idx = min(idx, len(frames) - 1)
            sampled.append(frames[idx])

        if not self.use_smart_sampling:
            return sampled, indices

        # Bulanık kareleri filtrele
        filtered = [(i, f) for i, f in zip(indices, sampled) if self._laplacian_variance(f) >= self.min_laplacian_variance]
        if not filtered:
            filtered = list(zip(indices, sampled))  # Hepsi bulanıksa tümünü al

        # Ardışık tekrarlı kareleri SSIM ile azalt
        final: List[Tuple[int, NDArray[np.uint8]]] = []
        for i, f in filtered:
            if not final:
                final.append((i, f))
                continue
            prev = final[-1][1]
            score = ssim(prev, f, channel_axis=2, data_range=255)
            if score < self.ssim_threshold:
                final.append((i, f))

        # Hâlâ hedef sayıya ulaşamazsak eksik kısımları doldur
        if len(final) < self.target_count and len(filtered) > len(final):
            used_indices = {x[0] for x in final}
            for i, f in filtered:
                if i not in used_indices:
                    final.append((i, f))
                if len(final) >= self.target_count:
                    break

        # Hâlâ eksikse tekrarlı da olsa doldur
        while len(final) < self.target_count and final:
            final.append(final[-1])

        final = final[: self.target_count]
        final_indices = [x[0] for x in final]
        final_frames = [x[1] for x in final]
        return final_frames, final_indices

    @staticmethod
    def _laplacian_variance(frame: NDArray[np.uint8]) -> float:
        import cv2
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return float(cv2.Laplacian(gray, cv2.CV_64F).var())
