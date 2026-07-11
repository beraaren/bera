"""Düşük ışık / CCTV görüntü iyileştirme."""
from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray


class LowLightEnhancer:
    """CLAHE ve gamma düzeltme ile görüntü kontrastını iyileştirir.

    Zero-DCE gibi derin öğrenme tabanlı yöntemler için ``enhance_zero_dce``
    placeholder metodu bırakılmıştır; ONNX ağırlığı verildiğinde aktif hale
    getirilebilir.
    """

    def __init__(
        self,
        enabled: bool = True,
        clip_limit: float = 2.0,
        grid_size: tuple[int, int] = (8, 8),
        gamma: float = 1.0,
    ):
        self.enabled = enabled
        self.clip_limit = clip_limit
        self.grid_size = grid_size
        self.gamma = gamma
        self._clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)

    def enhance(self, frame: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if not self.enabled:
            return frame

        lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        l = self._clahe.apply(l)
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

        if self.gamma != 1.0:
            inv_gamma = 1.0 / self.gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
            enhanced = cv2.LUT(enhanced, table)

        return enhanced

    def enhance_zero_dce(self, frame: NDArray[np.uint8], onnx_path: str | None = None) -> NDArray[np.uint8]:
        """Placeholder: ONNX Zero-DCE modeli yüklendiğinde entegre edilir."""
        if onnx_path is None:
            return self.enhance(frame)
        # TODO: cv2.dnn.readNetFromONNX ile Zero-DCE çalıştır.
        return self.enhance(frame)
