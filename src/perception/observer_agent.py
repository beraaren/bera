"""Gözlemci Ajan: videoyu izler, tespit/takip/scene graph üretir."""
from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from numpy.typing import NDArray

from ..config import PerceptionConfig
from ..utils.logger import get_logger
from .detector import Detection, ObjectDetector
from .scene_graph import SceneGraph
from .tracker import ObjectTracker, TrackedObject


class ObserverAgent:
    """Objektif algı katmanı; sadece gözlemlenen nesneleri ve ilişkileri raporlar."""

    def __init__(self, config: PerceptionConfig):
        self.config = config
        self.logger = get_logger("ObserverAgent")
        self.detector = ObjectDetector(
            model_path=config.yolo_model,
            confidence=config.confidence_threshold,
            custom_classes=config.custom_classes,
        )
        self.tracker = ObjectTracker(tracker_name=config.tracker, persist=config.tracker_persist)
        self.tracks: Dict[int, TrackedObject] = {}

    def observe_frame(self, frame: NDArray[np.uint8], frame_idx: int, timestamp: float) -> Dict[str, Any]:
        """Tek kare için tespit, takip ve scene graph üretir."""
        # Tespit (ve takip)
        tracked = self.tracker.track(frame, self.detector, frame_idx=frame_idx)

        # Track state güncelle
        for t in tracked:
            existing = self.tracks.get(t.track_id)
            if existing:
                existing.update(t.last_detection)
            else:
                self.tracks[t.track_id] = t

        # Kaybolan track'leri işaretle
        active_ids = {t.track_id for t in tracked}
        for tid, t in self.tracks.items():
            if tid not in active_ids:
                t.disappeared += 1

        # Scene graph
        detections: List[Detection] = [t.last_detection for t in self.tracks.values() if t.disappeared < 5]
        graph = SceneGraph.from_detections(frame_idx, timestamp, detections)

        return {
            "frame_idx": frame_idx,
            "timestamp": round(timestamp, 2),
            "detections": [d.to_dict() for d in detections],
            "tracks": [t.to_dict() for t in self.tracks.values() if t.disappeared < 5],
            "scene_graph": graph.to_dict(),
        }

    def observe_video(self, frames: List[NDArray[np.uint8]], fps: float) -> List[Dict[str, Any]]:
        observations = []
        for idx, frame in enumerate(frames):
            timestamp = idx / fps if fps else 0.0
            obs = self.observe_frame(frame, idx, timestamp)
            observations.append(obs)
        return observations
