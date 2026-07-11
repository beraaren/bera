"""Olay tespit motoru testleri."""
from src.config import EventsConfig
from src.events.event_engine import EventEngine
from src.perception.detector import Detection
from src.perception.tracker import TrackedObject


def make_track(class_name: str, x1: float, y1: float, x2: float, y2: float, tid: int = 1) -> TrackedObject:
    det = Detection(class_name=class_name, confidence=0.8, bbox=(x1, y1, x2, y2))
    return TrackedObject(track_id=tid, class_name=class_name, initial_detection=det)


def test_gathering_detection():
    cfg = EventsConfig(enabled_rules=["gathering"], thresholds={"gathering": {"min_persons": 3, "max_inter_center_distance": 120}})
    engine = EventEngine(cfg, fps=25.0)

    obs = {
        "frame_idx": 10,
        "timestamp": 0.4,
        "detections": [],
        "tracks": [
            {"track_id": 1, "class": "insan", "history_length": 1, "last_center": [50, 50], "speed": [0, 0]},
            {"track_id": 2, "class": "insan", "history_length": 1, "last_center": [55, 55], "speed": [0, 0]},
            {"track_id": 3, "class": "insan", "history_length": 1, "last_center": [60, 60], "speed": [0, 0]},
        ],
        "scene_graph": {
            "frame_idx": 10,
            "timestamp": 0.4,
            "nodes": [
                {"id": "insan_0", "class": "insan", "track_id": 1, "center": [50, 50], "confidence": 0.8},
                {"id": "insan_1", "class": "insan", "track_id": 2, "center": [55, 55], "confidence": 0.8},
                {"id": "insan_2", "class": "insan", "track_id": 3, "center": [60, 60], "confidence": 0.8},
            ],
            "edges": [],
        },
    }

    signals = engine.process_observation(obs)
    assert len(signals) >= 1
    assert signals[0].event_type == "gathering"


def test_proximity_detection():
    cfg = EventsConfig(enabled_rules=["proximity"], thresholds={"proximity": {"dangerous_pairs": [["forklift", "insan"]], "distance_threshold_pixels": 100}})
    engine = EventEngine(cfg, fps=25.0)

    obs = {
        "frame_idx": 5,
        "timestamp": 0.2,
        "detections": [],
        "tracks": [
            {"track_id": 1, "class": "forklift", "history_length": 1, "last_center": [100, 100], "speed": [0, 0]},
            {"track_id": 2, "class": "insan", "history_length": 1, "last_center": [110, 110], "speed": [0, 0]},
        ],
        "scene_graph": {
            "frame_idx": 5,
            "timestamp": 0.2,
            "nodes": [
                {"id": "forklift_0", "class": "forklift", "track_id": 1, "center": [100, 100], "confidence": 0.9},
                {"id": "insan_0", "class": "insan", "track_id": 2, "center": [110, 110], "confidence": 0.85},
            ],
            "edges": [
                {"source": "forklift_0", "target": "insan_0", "relation": "near", "weight": 0.9}
            ],
        },
    }

    signals = engine.process_observation(obs)
    assert any(s.event_type == "dangerous_proximity" for s in signals)
