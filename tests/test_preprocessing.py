"""Ön işleme katmanı testleri."""
import numpy as np
import pytest

from src.preprocessing.enhancer import LowLightEnhancer
from src.preprocessing.frame_sampler import FrameSampler


def test_laplacian_filter_drops_blurry():
    sharp = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    blurry = np.full((100, 100, 3), 128, dtype=np.uint8)

    sampler = FrameSampler(min_laplacian_variance=50.0)
    sharp_var = sampler._laplacian_variance(sharp)
    blurry_var = sampler._laplacian_variance(blurry)

    assert sharp_var > blurry_var
    assert blurry_var < 10.0


def test_frame_sampler_returns_target_count():
    frames = [np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8) for _ in range(20)]
    sampler = FrameSampler(target_count=8, use_smart_sampling=False)
    selected, indices = sampler.sample(frames, total_frames=20)
    assert len(selected) == 8
    assert len(indices) == 8


def test_low_light_enhancer_preserves_shape():
    frame = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    enhancer = LowLightEnhancer(enabled=True)
    out = enhancer.enhance(frame)
    assert out.shape == frame.shape
    assert out.dtype == frame.dtype
