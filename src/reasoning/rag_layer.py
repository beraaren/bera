"""Çift indeksli RAG katmanı: risk pattern'leri + aksiyon kataloğu."""
from __future__ import annotations

from typing import Any, Dict, List

import yaml

from ..config import get_data_path


class RAGLayer:
    """Scene graph ve olay sinyallerine göre risk pattern'leri ve aksiyonları eşleştirir."""

    def __init__(
        self,
        patterns_path: str | None = None,
        actions_path: str | None = None,
    ):
        self.patterns: Dict[str, Any] = {}
        self.actions: Dict[str, Any] = {}

        ppath = patterns_path or get_data_path("risk_patterns.yaml")
        if ppath.exists():
            with open(ppath, "r", encoding="utf-8") as f:
                self.patterns = yaml.safe_load(f) or {}

        apath = actions_path or get_data_path("action_catalog.yaml")
        if apath.exists():
            with open(apath, "r", encoding="utf-8") as f:
                self.actions = yaml.safe_load(f) or {}

    def match_patterns(self, event_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Olay sinyallerini risk pattern deposuyla eşleştirir."""
        patterns = self.patterns.get("patterns", {})
        matches = []
        for sig in event_signals:
            event_type = sig.get("event_type", "")
            for name, pattern in patterns.items():
                if event_type == name or event_type in name or name in event_type:
                    matches.append({
                        "pattern": name,
                        "description": pattern.get("description", ""),
                        "risk_score": pattern.get("risk_score", 0),
                        "risk_level": pattern.get("risk_level", "Düşük"),
                        "matched_signal": sig,
                    })
        return matches

    def recommend_actions(self, risk_level: str, event_types: List[str]) -> List[str]:
        """Risk seviyesi ve olay tiplerine göre aksiyon önerir."""
        catalog = self.actions.get("actions", {})
        level_actions = catalog.get(risk_level, {})

        actions: List[str] = []
        # Olay tipine özel aksiyonlar
        for et in event_types:
            specific = level_actions.get(et)
            if isinstance(specific, list):
                actions.extend(specific)

        # Varsayılan aksiyonlar
        default = level_actions.get("default", [])
        if isinstance(default, list):
            actions.extend(default)

        # Tekrarları kaldır, sırayı koru
        seen = set()
        unique = []
        for a in actions:
            if a not in seen:
                seen.add(a)
                unique.append(a)
        return unique

    def build_context(self, event_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Karar ajanına verilecek RAG kontekstini oluşturur."""
        matches = self.match_patterns(event_signals)
        if not matches:
            return {"risk_level": "Düşük", "risk_score": 0, "actions": [], "matched_patterns": []}

        # En yüksek risk skorunu esas al
        top = max(matches, key=lambda x: x.get("risk_score", 0))
        risk_level = top.get("risk_level", "Düşük")
        event_types = [m["matched_signal"].get("event_type", "") for m in matches]
        actions = self.recommend_actions(risk_level, event_types)

        return {
            "risk_level": risk_level,
            "risk_score": top.get("risk_score", 0),
            "actions": actions,
            "matched_patterns": matches,
        }
