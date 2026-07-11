"""Karar Ajanı: algı + RAG + VLM ile nihai kararı üretir."""
from __future__ import annotations

import base64
import io
import json
from typing import Any, Dict, List

import numpy as np
from numpy.typing import NDArray
from PIL import Image

from ..config import DecisionAgentConfig, VLMConfig
from ..models.vlm_backend import VLMBackend, create_backend
from ..utils.logger import get_logger
from .memory import ShortTermMemory
from .mock_tools import MockToolRegistry
from .rag_layer import RAGLayer


class DecisionAgent:
    """VLM odaklı karar ajanı; RAG ve geometrik sinyalleri birleştirir."""

    def __init__(
        self,
        config: DecisionAgentConfig,
        vlm_config: VLMConfig,
        rag: RAGLayer,
        memory: ShortTermMemory,
        tools: MockToolRegistry,
        backend: VLMBackend | None = None,
    ):
        self.config = config
        self.vlm_config = vlm_config
        self.rag = rag
        self.memory = memory
        self.tools = tools
        self.backend = backend or create_backend(vlm_config)
        self.logger = get_logger("DecisionAgent")

    def decide(
        self,
        images: List[NDArray[np.uint8]],
        event_signals: List[Dict[str, Any]],
        scene_graphs: List[Dict[str, Any]],
        fps: float,
    ) -> Dict[str, Any]:
        """VLM çağrısı yapar; RAG ve hafızayı prompta dahil eder."""
        rag_context = self.rag.build_context(event_signals)
        memory_context = self.memory.to_prompt_context()

        prompt = self._build_prompt(event_signals, scene_graphs, rag_context, memory_context)
        self.logger.debug(f"VLM prompt uzunluğu: {len(prompt)} karakter")

        temperature = self.vlm_config.vllm.temperature
        max_tokens = self.vlm_config.vllm.max_new_tokens
        if self.backend.name() == "llama_cpp":
            temperature = self.vlm_config.llama_cpp.temperature
            max_tokens = self.vlm_config.llama_cpp.max_tokens
        elif self.backend.name() == "transformers":
            max_tokens = self.vlm_config.transformers.max_new_tokens

        raw = self.backend.generate(images, prompt, temperature=temperature, max_tokens=max_tokens)
        self.logger.debug(f"VLM çıktısı:\n{raw}")

        # Çıktıyı parse etmeyi guardrail'e bırak; burada hafif temizlik
        return {"raw": raw, "rag_context": rag_context}

    def _build_prompt(
        self,
        event_signals: List[Dict[str, Any]],
        scene_graphs: List[Dict[str, Any]],
        rag_context: Dict[str, Any],
        memory_context: str,
    ) -> str:
        system = self.config.system_prompt

        parts = [system]

        if self.config.include_event_signals:
            parts.append("\n--- ALGI KATMANI SİNYALLERİ ---")
            if event_signals:
                parts.append(json.dumps(event_signals, ensure_ascii=False, indent=2))
            else:
                parts.append("Geometrik olay sinyali tespit edilmedi.")

        if self.config.include_rag_context:
            parts.append("\n--- RAG KONTEXTİ ---")
            parts.append(json.dumps(rag_context, ensure_ascii=False, indent=2))

        if self.config.include_scene_graph:
            parts.append("\n--- SAHNE GRAFİ (SON KARE) ---")
            if scene_graphs:
                parts.append(json.dumps(scene_graphs[-1], ensure_ascii=False, indent=2))

        parts.append("\n--- KISA SÜRELİ HAFIZA ---")
        parts.append(memory_context)

        parts.append(
            "\nYukarıdaki bilgilere dayanarak videoyu analiz et ve SADECE aşağıdaki JSON "
            "şemasına uygun Türkçe yanıt ver. Açıklama ekleme:\n"
            '{\n'
            '  "summary": "Videonun genel özeti",\n'
            '  "events": [\n'
            '    {"time": "MM:SS", "event": "olay açıklaması", "event_type": "tip_over|fall|gathering|...", "confidence": 0.0-1.0}\n'
            '  ],\n'
            '  "risk": "Düşük|Orta|Yüksek",\n'
            '  "actions": ["aksiyon 1", "aksiyon 2"],\n'
            '  "reasoning": "Kararın gerekçesi",\n'
            '  "confidence": 0.0-1.0,\n'
            '  "triggered_mock_tools": [\n'
            '    {"tool_name": "call_health_team", "params": {"location": "...", "urgency": "Yüksek"}}\n'
            '  ]\n'
            '}'
        )
        return "\n".join(parts)

    @staticmethod
    def frames_to_grid(frames: List[NDArray[np.uint8]], cols: int = 4) -> NDArray[np.uint8]:
        """Kareleri tek grid görüntüsüne birleştirir."""
        rows = (len(frames) + cols - 1) // cols
        h, w = frames[0].shape[:2]
        grid = np.zeros((h * rows, w * cols, 3), dtype=np.uint8)
        for idx, f in enumerate(frames):
            r, c = divmod(idx, cols)
            grid[r * h:(r + 1) * h, c * w:(c + 1) * w] = f
        return grid
