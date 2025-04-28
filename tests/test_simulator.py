"""
Tests for the TanzoSimulator class.
"""

import json
import os
from pathlib import Path

import pytest
import yaml

from clients.python.tanzo_schema import TanzoProfile, TanzoSimulator


@pytest.fixture
def example_profile_path():
    """Return the path to an example profile."""
    return Path(__file__).parent.parent / "examples" / "Kai_profile.yaml"


@pytest.fixture
def digital_profile_path():
    """Return the path to the digital archetype example profile."""
    return Path(__file__).parent.parent / "examples" / "digital_archetype_only.yaml"


@pytest.fixture
def example_profile(example_profile_path):
    """Load and parse the example profile."""
    with open(example_profile_path, "r") as f:
        data = yaml.safe_load(f)
    return TanzoProfile(**data)


@pytest.fixture
def digital_profile(digital_profile_path):
    """Load and parse the digital archetype profile."""
    with open(digital_profile_path, "r") as f:
        data = yaml.safe_load(f)
    return TanzoProfile(**data)


@pytest.fixture
def example_simulator(example_profile):
    """Return a TanzoSimulator for the example profile."""
    return TanzoSimulator(example_profile)


@pytest.fixture
def digital_simulator(digital_profile):
    """Return a TanzoSimulator for the digital profile."""
    return TanzoSimulator(digital_profile)


def test_simulator_initialization(example_profile):
    """Test that the simulator initializes correctly."""
    simulator = TanzoSimulator(example_profile)
    assert simulator.profile == example_profile


def test_get_variance_factor(example_simulator):
    """Test that the variance factor is retrieved correctly."""
    # The example profile has a variance of 3, so it should be 0.3
    variance = example_simulator.get_variance_factor()
    assert isinstance(variance, float)
    assert 0 <= variance <= 1
    assert variance == 0.3  # 3/10


def test_simulate_attribute(example_simulator):
    """Test simulating an attribute with randomization."""
    # Test a regular attribute (1-10 range)
    value = example_simulator.simulate_attribute(5)
    assert isinstance(value, int)
    assert 1 <= value <= 10
    
    # Test with custom range
    value = example_simulator.simulate_attribute(0, -5, 5)
    assert isinstance(value, int)
    assert -5 <= value <= 5


def test_simulate_emotional_range(example_simulator):
    """Test simulating emotional ranges."""
    ranges = example_simulator.simulate_emotional_range()
    assert isinstance(ranges, dict)
    
    # Check that the example profile's emotional ranges are present
    assert "extrovert_introvert" in ranges
    assert "thinking_feeling" in ranges
    assert "practical_imaginative" in ranges
    
    # Check that values are within bounds (-10 to 10)
    for key, value in ranges.items():
        assert isinstance(value, int)
        assert -10 <= value <= 10


def test_simulate_stress_response(example_simulator):
    """Test simulating stress responses."""
    # Test with stress level below threshold
    response = example_simulator.simulate_stress_response(1)
    assert isinstance(response, dict)
    assert not response["triggered"]
    
    # Test with stress level at or above threshold
    response = example_simulator.simulate_stress_response(10)
    assert response["triggered"]
    assert response["response_type"] is not None
    assert isinstance(response["behaviors"], list)


def test_run_monte_carlo(example_simulator):
    """Test running a Monte Carlo simulation."""
    # Run with small number of iterations for testing
    results = example_simulator.run_monte_carlo(iterations=10)
    
    assert isinstance(results, dict)
    assert results["profile_name"] == "Kai Yamamoto"
    assert results["archetype"] == "Mentor"
    assert results["iterations"] == 10
    
    # Check that the emotional ranges have values
    assert len(results["emotional_ranges"]["extrovert_introvert"]) == 10
    
    # Check that the stress responses have been recorded
    assert len(results["stress_responses"]) == 10
    
    # Check that the summary section is present
    assert "summary" in results
    assert "emotional_ranges" in results["summary"]
    assert "communication" in results["summary"]
    assert "decision_making" in results["summary"]
    assert "stress_response_rate" in results["summary"]


def test_simulator_with_different_profiles(example_simulator, digital_simulator):
    """Test that the simulator works with different profile types."""
    # Run simulations on both profile types
    results1 = example_simulator.run_monte_carlo(iterations=5)
    results2 = digital_simulator.run_monte_carlo(iterations=5)
    
    # Check that the profiles are correctly identified
    assert results1["profile_name"] == "Kai Yamamoto"
    assert results2["profile_name"] == "NeoGuide"
    
    # Check that the archetypes are correctly used
    assert results1["archetype"] == "Mentor"
    assert results2["archetype"] == "Sage"


def test_simulator_determinism_with_seed():
    """Test that using the same seed produces deterministic results."""
    # Create a minimal profile with a fixed seed
    profile_data = {
        "identity": {"name": "Test"},
        "archetype": {"primary": "Sage"},
        "traits": {},
        "simulations": {
            "randomization": {
                "seed": 42,
                "variance": 5
            }
        }
    }
    profile = TanzoProfile(**profile_data)
    
    # Run two simulations with the same profile
    simulator1 = TanzoSimulator(profile)
    simulator2 = TanzoSimulator(profile)
    
    results1 = simulator1.run_monte_carlo(iterations=5)
    results2 = simulator2.run_monte_carlo(iterations=5)
    
    # With the same seed, the stress_responses should be identical
    assert results1["stress_responses"] == results2["stress_responses"]
