"""Geometrik olay tespit kuralları."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..perception.scene_graph import SceneEdge, SceneGraph, SceneNode
from ..perception.tracker import TrackedObject
from .state_machine import TrackStateMachine


@dataclass
class EventSignal:
    event_type: str
    timestamp: float
    description: str
    confidence: float
    involved_track_ids: List[int]
    metadata: Dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self._format_time(self.timestamp),
            "description": self.description,
            "confidence": round(self.confidence, 3),
            "involved_track_ids": self.involved_track_ids,
            "metadata": self.metadata,
        }

    @staticmethod
    def _format_time(seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


class RuleSet:
    """Yapılandırılabilir geometrik kurallar kümesi."""

    def __init__(self, thresholds: Dict[str, Any], fps: float = 25.0):
        self.thresholds = thresholds
        self.fps = fps

    def evaluate(
        self,
        tracks: List[TrackedObject],
        states: TrackStateMachine,
        graph: SceneGraph,
    ) -> List[EventSignal]:
        signals: List[EventSignal] = []

        enabled = self.thresholds.get("enabled_rules", [])

        if "tip_over" in enabled:
            signals.extend(self._rule_tip_over(tracks, states))
        if "fall" in enabled:
            signals.extend(self._rule_fall(tracks, states))
        if "gathering" in enabled:
            signals.extend(self._rule_gathering(tracks))
        if "immobility" in enabled:
            signals.extend(self._rule_immobility(tracks, states))
        if "ppe_missing" in enabled:
            signals.extend(self._rule_ppe_missing(graph))
        if "proximity" in enabled:
            signals.extend(self._rule_proximity(graph))

        return signals

    def _rule_tip_over(self, tracks: List[TrackedObject], states: TrackStateMachine) -> List[EventSignal]:
        signals = []
        cfg = self.thresholds.get("tip_over", {})
        min_frames = cfg.get("min_duration_frames", 3)
        ar_min = cfg.get("aspect_ratio_min", 1.45)

        for t in tracks:
            if t.class_name != "forklift":
                continue
            state = states.get(t.track_id)
            if state and state.tip_over_frames >= min_frames:
                det = t.last_detection
                if det.aspect_ratio >= ar_min:
                    signals.append(
                        EventSignal(
                            event_type="forklift_tip_over",
                            timestamp=t.last_detection.frame_idx / self.fps,
                            description=f"Forklift (track {t.track_id}) devrilme pozisyonunda; en/boy oranı {det.aspect_ratio:.2f}",
                            confidence=min(1.0, det.aspect_ratio / 3.0),
                            involved_track_ids=[t.track_id],
                            metadata={"aspect_ratio": det.aspect_ratio},
                        )
                    )
        return signals

    def _rule_fall(self, tracks: List[TrackedObject], states: TrackStateMachine) -> List[EventSignal]:
        signals = []
        cfg = self.thresholds.get("fall", {})
        speed_drop_ratio = cfg.get("speed_drop_ratio", 0.5)

        for t in tracks:
            if t.class_name != "insan":
                continue
            state = states.get(t.track_id)
            speed_y = t.speed[1]
            if state and state.fall_frames >= 2 and speed_y > 30:
                signals.append(
                    EventSignal(
                        event_type="person_fall",
                        timestamp=t.last_detection.frame_idx / self.fps,
                        description=f"Personel (track {t.track_id}) düşme hareketi gösteriyor.",
                        confidence=min(1.0, abs(speed_y) / 100.0),
                        involved_track_ids=[t.track_id],
                        metadata={"vertical_speed": speed_y},
                    )
                )
        return signals

    def _rule_gathering(self, tracks: List[TrackedObject]) -> List[EventSignal]:
        signals = []
        cfg = self.thresholds.get("gathering", {})
        min_persons = cfg.get("min_persons", 3)
        max_dist = cfg.get("max_inter_center_distance", 120)

        persons = [t for t in tracks if t.class_name == "insan"]
        if len(persons) < min_persons:
            return signals

        # Basit kümeleme: birbirine yakın kişileri bul
        clusters = []
        visited = set()
        for p in persons:
            if id(p) in visited:
                continue
            cluster = [p]
            visited.add(id(p))
            for q in persons:
                if id(q) in visited:
                    continue
                if math.hypot(p.last_detection.center[0] - q.last_detection.center[0],
                             p.last_detection.center[1] - q.last_detection.center[1]) <= max_dist:
                    cluster.append(q)
                    visited.add(id(q))
            if len(cluster) >= min_persons:
                clusters.append(cluster)

        for cluster in clusters:
            signals.append(
                EventSignal(
                    event_type="gathering",
                    timestamp=cluster[0].last_detection.frame_idx / self.fps,
                    description=f"{len(cluster)} personel tehlikeli bölgede toplanmış.",
                    confidence=min(1.0, len(cluster) / 5.0),
                    involved_track_ids=[t.track_id for t in cluster],
                    metadata={"person_count": len(cluster)},
                )
            )
        return signals

    def _rule_immobility(self, tracks: List[TrackedObject], states: TrackStateMachine) -> List[EventSignal]:
        signals = []
        cfg = self.thresholds.get("immobility", {})
        min_seconds = cfg.get("min_duration_seconds", 2.5)

        for t in tracks:
            if t.class_name != "insan":
                continue
            state = states.get(t.track_id)
            if state and state.seconds_stationary(self.fps) >= min_seconds:
                signals.append(
                    EventSignal(
                        event_type="immobile_person",
                        timestamp=t.last_detection.frame_idx / self.fps,
                        description=f"Personel (track {t.track_id}) {state.seconds_stationary(self.fps):.1f} saniyedir hareketsiz.",
                        confidence=min(1.0, state.seconds_stationary(self.fps) / 10.0),
                        involved_track_ids=[t.track_id],
                        metadata={"stationary_seconds": state.seconds_stationary(self.fps)},
                    )
                )
        return signals

    def _rule_ppe_missing(self, graph: SceneGraph) -> List[EventSignal]:
        signals = []
        cfg = self.thresholds.get("ppe_missing", {})
        proximity = cfg.get("proximity_threshold_pixels", 80)
        ppe_classes = cfg.get("classes", ["baret", "yelek"])

        persons = graph.find_nodes("insan")
        for person in persons:
            has_ppe = {ppe: False for ppe in ppe_classes}
            for edge in graph.edges:
                if edge.relation != "wearing":
                    continue
                other_id = edge.source if edge.target == person.node_id else edge.target
                other = graph.nodes.get(other_id)
                if other and other.class_name in ppe_classes:
                    has_ppe[other.class_name] = True

            missing = [p for p, v in has_ppe.items() if not v]
            if missing:
                signals.append(
                    EventSignal(
                        event_type="ppe_missing",
                        timestamp=graph.timestamp,
                        description=f"Personel {person.node_id} eksik KKD: {', '.join(missing)}.",
                        confidence=0.7,
                        involved_track_ids=[person.track_id] if person.track_id is not None else [],
                        metadata={"missing_ppe": missing},
                    )
                )
        return signals

    def _rule_proximity(self, graph: SceneGraph) -> List[EventSignal]:
        signals = []
        cfg = self.thresholds.get("proximity", {})
        dangerous_pairs = [set(p) for p in cfg.get("dangerous_pairs", [["forklift", "insan"]])]
        threshold = cfg.get("distance_threshold_pixels", 100)

        for edge in graph.edges:
            if edge.relation != "near":
                continue
            a = graph.nodes.get(edge.source)
            b = graph.nodes.get(edge.target)
            if not a or not b:
                continue
            if {a.class_name, b.class_name} in dangerous_pairs:
                # Mesafe tahmini: weight 1 - dist/threshold
                estimated_dist = (1 - edge.weight) * threshold
                if estimated_dist <= threshold:
                    signals.append(
                        EventSignal(
                            event_type="dangerous_proximity",
                            timestamp=graph.timestamp,
                            description=f"{a.class_name} ve {b.class_name} arasında tehlikeli yakınlık (~{estimated_dist:.0f} piksel).",
                            confidence=edge.weight,
                            involved_track_ids=[tid for tid in (a.track_id, b.track_id) if tid is not None],
                            metadata={"estimated_distance_pixels": estimated_dist},
                        )
                    )
        return signals
