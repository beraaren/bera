"""Olay tespit motoru: gözlemleri geometrik kurallarla işler."""
from __future__ import annotations

from typing import Any, Dict, List

from ..config import EventsConfig
from ..perception.scene_graph import SceneGraph
from ..perception.tracker import TrackedObject
from ..utils.logger import get_logger
from .rules import EventSignal, RuleSet
from .state_machine import TrackStateMachine


class EventEngine:
    """Track state machine + kural seti ile sürekli olay sinyalleri üretir."""

    def __init__(self, config: EventsConfig, fps: float = 25.0):
        self.config = config
        self.fps = fps
        self.rules = RuleSet({
            "enabled_rules": config.enabled_rules,
            **config.thresholds.model_dump(),
        }, fps=fps)
        self.states = TrackStateMachine(fps=fps)
        self.signals: List[EventSignal] = []
        self.logger = get_logger("EventEngine")

    def process_observation(self, observation: Dict[str, Any]) -> List[EventSignal]:
        """Bir kare gözlemini işleyip yeni sinyaller döner."""
        tracks = self._observation_to_tracks(observation)
        self.states.update(tracks)

        graph_data = observation.get("scene_graph", {})
        graph = SceneGraph(
            frame_idx=graph_data.get("frame_idx", 0),
            timestamp=graph_data.get("timestamp", 0.0),
        )
        for n in graph_data.get("nodes", []):
            from ..perception.scene_graph import SceneNode
            graph.add_node(
                SceneNode(
                    node_id=n["id"],
                    class_name=n["class"],
                    track_id=n.get("track_id"),
                    bbox=tuple(n.get("bbox", [0, 0, 0, 0])),
                    confidence=n.get("confidence", 0.0),
                    frame_idx=n.get("frame_idx", 0),
                )
            )
        graph.build_relations()

        new_signals = self.rules.evaluate(tracks, self.states, graph)
        # Yinelenen sinyalleri önle (aynı track + event_type son 10 saniye içinde varsa atla)
        filtered = []
        for sig in new_signals:
            if not self._is_recent(sig):
                filtered.append(sig)
                self.signals.append(sig)
        return filtered

    def _observation_to_tracks(self, observation: Dict[str, Any]) -> List[TrackedObject]:
        from ..perception.detector import Detection
        tracks: List[TrackedObject] = []
        for t in observation.get("tracks", []):
            det = Detection(
                class_name=t["class"],
                confidence=1.0,
                bbox=(0.0, 0.0, 0.0, 0.0),
            )
            # Daha zengin bilgi varsa kullan
            det_data = next(
                (d for d in observation.get("detections", []) if d.get("class") == t["class"]),
                None,
            )
            if det_data:
                det = Detection(
                    class_name=det_data["class"],
                    confidence=det_data.get("confidence", 1.0),
                    bbox=tuple(det_data.get("bbox", [0, 0, 0, 0])),
                    frame_idx=det_data.get("frame_idx", 0),
                )
            to = TrackedObject(track_id=t["track_id"], class_name=t["class"], initial_detection=det)
            to.history = [det]
            tracks.append(to)
        return tracks

    def _is_recent(self, sig: EventSignal, window_seconds: float = 10.0) -> bool:
        for prev in reversed(self.signals):
            if prev.event_type == sig.event_type and set(prev.involved_track_ids) == set(sig.involved_track_ids):
                if abs(prev.timestamp - sig.timestamp) <= window_seconds:
                    return True
        return False

    def get_signals(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.signals]
