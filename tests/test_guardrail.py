"""Guardrail testleri."""
import pytest

from src.config import GuardrailConfig
from src.output.guardrail import OutputGuardrail


def test_guardrail_accepts_valid_json():
    raw = '''
    ```json
    {
        "summary": "Test özet",
        "events": [{"time": "00:05", "event": "x", "event_type": "fall", "confidence": 0.8}],
        "risk": "Yüksek",
        "actions": ["a1", "a2"],
        "reasoning": "r",
        "confidence": 0.8,
        "triggered_mock_tools": []
    }
    ```
    '''
    guardrail = OutputGuardrail(GuardrailConfig())
    result = guardrail.validate(raw, lambda t: raw, rag_risk_level="Yüksek")
    assert result["risk"] == "Yüksek"
    assert len(result["actions"]) == 2


def test_guardrail_retries_and_null_response():
    bad = "Bu geçerli bir JSON değil"
    guardrail = OutputGuardrail(GuardrailConfig(max_retries=2, temperatures=[0.1, 0.05]))
    result = guardrail.validate(bad, lambda t: bad, rag_risk_level="Düşük")
    assert result["summary"] == "Bilmiyorum"
