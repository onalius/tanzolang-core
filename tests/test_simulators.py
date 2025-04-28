"""
Tests for the simulation functionality.
"""

import pytest
import numpy as np
from pathlib import Path

from clients.python.tanzo_schema import (
    TanzoProfile, Archetype, Behavior, simulate_profile,
    load_profile_from_yaml
)
from clients.python.tanzo_schema.simulators import (
    _sample_behavior_activation, _simulate_iteration
)


def test_sample_behavior_activation():
    """Test sampling behavior activation."""
    behavior = Behavior(
        name="Test Behavior",
        description="A test behavior",
        strength=0.7
    )
    
    # Test with default params
    activation = _sample_behavior_activation(behavior, {})
    assert 0.0 <= activation <= 1.0
    
    # Test with high randomness
    activations = [_sample_behavior_activation(behavior, {"randomness": 0.8}) for _ in range(100)]
    assert all(0.0 <= a <= 1.0 for a in activations)
    
    # Test with no randomness
    activation = _sample_behavior_activation(behavior, {"randomness": 0.0})
    assert activation == 0.7


def test_simulate_iteration():
    """Test simulating a single iteration."""
    minimal_profile = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            }
        }
    )
    
    # Minimal profile should return empty metrics
    metrics = _simulate_iteration(minimal_profile)
    assert metrics == {}
    
    # Create a more complete profile
    complex_profile = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Complex Profile",
            "archetype": {
                "primary": "advisor"
            },
            "behaviors": [
                {
                    "name": "Behavior 1",
                    "description": "First behavior",
                    "strength": 0.8
                },
                {
                    "name": "Behavior 2",
                    "description": "Second behavior",
                    "strength": 0.5
                }
            ],
            "personality": {
                "traits": {
                    "openness": 0.7,
                    "conscientiousness": 0.6,
                    "extraversion": 0.5,
                    "agreeableness": 0.8,
                    "neuroticism": 0.3
                }
            },
            "communication": {
                "complexity": 0.7,
                "verbosity": 0.6
            }
        }
    )
    
    # Complex profile should return various metrics
    metrics = _simulate_iteration(complex_profile)
    assert "mean_behavior_activation" in metrics
    assert any("expression" in k for k in metrics.keys())
    assert "expressed_complexity" in metrics
    assert "expressed_verbosity" in metrics


def test_simulate_profile():
    """Test the full profile simulation."""
    examples_dir = Path(__file__).parent.parent / "examples"
    kai_path = examples_dir / "Kai_profile.yaml"
    profile = load_profile_from_yaml(kai_path)
    
    # Run simulation with 50 iterations
    result = simulate_profile(profile, iterations=50)
    
    assert result.profile_name == "Kai - Technical Advisor"
    assert result.iterations == 50
    assert len(result.metrics) > 0
    assert len(result.summary) > 0
    
    # Check that all metric values are within 0-1 range
    assert all(0.0 <= m.value <= 1.0 for m in result.metrics)


def test_simulation_reproducibility():
    """Test that simulations are reproducible with fixed random seed."""
    np.random.seed(42)
    
    minimal_profile = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            },
            "behaviors": [
                {
                    "name": "Behavior",
                    "description": "Test behavior",
                    "strength": 0.7
                }
            ],
            "simulation": {
                "parameters": {
                    "randomness": 0.2
                }
            }
        }
    )
    
    # Run two identical simulations
    result1 = simulate_profile(minimal_profile, iterations=10)
    
    np.random.seed(42)
    result2 = simulate_profile(minimal_profile, iterations=10)
    
    # Results should be identical when seed is the same
    for i, metric in enumerate(result1.metrics):
        assert metric.value == result2.metrics[i].value
