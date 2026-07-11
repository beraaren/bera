"""Inference ve genel performans ölçümleme."""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import psutil


class MetricsCollector:
    def __init__(self, output_path: str | Path = "outputs/metrics.json"):
        self.output_path = Path(output_path)
        self.records: dict[str, Any] = {}
        self._start_mem = 0.0

    @contextmanager
    def measure(self, name: str):
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024 ** 2)
        start = time.perf_counter()
        try:
            yield self
        finally:
            elapsed = time.perf_counter() - start
            mem_after = process.memory_info().rss / (1024 ** 2)
            self.records[name] = {
                "elapsed_seconds": round(elapsed, 3),
                "memory_mb_before": round(mem_before, 1),
                "memory_mb_after": round(mem_after, 1),
                "memory_delta_mb": round(mem_after - mem_before, 1),
            }

    def add(self, name: str, value: Any) -> None:
        self.records[name] = value

    def save(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
