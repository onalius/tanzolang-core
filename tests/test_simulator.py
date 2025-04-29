"""
Tests for the TanzoLang simulator.
"""

import os
from pathlib import Path

import numpy as np
import pytest

from tanzo_schema.simulator import (
    _simulate_value,
    _simulate_trait,
    _simulate_attribute,
    simulate_single_profile,
    simulate_profile,
    summarize_simulations,
)
from tanzo_schema.validator import load_profile


# Find the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"


def test_simulate_value():
    """Test the _simulate_value function."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Test with a specific variance
    value = _simulate_value(50, 10)
    assert 0 <= value <= 100, "Simulated value should be within bounds"
    
    # Test with global variance factor
    value = _simulate_value(50, None, 0.2)
    assert 0 <= value <= 100, "Simulated value should be within bounds"
    
    # Test with different bounds
    value = _simulate_value(5, 1, 0.1, 1, 10)
    assert 1 <= value <= 10, "Simulated value should be within custom bounds"


def test_simulate_trait():
    """Test the _simulate_trait function."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    trait_data = {
        "value": 75,
        "variance": 10,
        "description": "Test trait"
    }
    
    simulated = _simulate_trait(trait_data, 0.2)
    
    # Check that all original fields are preserved
    assert "value" in simulated
    assert "variance" in simulated
    assert "description" in simulated
    assert simulated["description"] == "Test trait"
    
    # Check that value is simulated
    assert simulated["value"] != 75, "Value should be different after simulation"
    assert 0 <= simulated["value"] <= 100, "Simulated value should be within bounds"
    
    # Check that a simulated flag is added
    assert "simulated" in simulated
    assert simulated["simulated"] is True


def test_simulate_attribute():
    """Test the _simulate_attribute function."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    attr_data = {
        "value": 60,
        "variance": 15,
        "notes": "Test attribute"
    }
    
    simulated = _simulate_attribute(attr_data, 0.2)
    
    # Check that all original fields are preserved
    assert "value" in simulated
    assert "variance" in simulated
    assert "notes" in simulated
    assert simulated["notes"] == "Test attribute"
    
    # Check that value is simulated
    assert simulated["value"] != 60, "Value should be different after simulation"
    assert 0 <= simulated["value"] <= 100, "Simulated value should be within bounds"
    
    # Check that a simulated flag is added
    assert "simulated" in simulated
    assert simulated["simulated"] is True


def test_simulate_single_profile():
    """Test the simulate_single_profile function."""
    # Load a test profile
    profile_path = EXAMPLES_DIR / "Kai_profile.yaml"
    profile_data = load_profile(profile_path)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Simulate the profile
    simulated = simulate_single_profile(profile_data)
    
    # Check that the overall structure is preserved
    assert "metadata" in simulated
    assert "digital_archetype" in simulated
    assert "traits" in simulated["digital_archetype"]
    assert "attributes" in simulated["digital_archetype"]
    
    # Check that the simulation metadata is added
    assert "simulated" in simulated["metadata"]
    assert simulated["metadata"]["simulated"] is True
    
    # Check that the trait values are different
    orig_openness = profile_data["digital_archetype"]["traits"]["openness"]["value"]
    sim_openness = simulated["digital_archetype"]["traits"]["openness"]["value"]
    assert orig_openness != sim_openness, "Trait values should be different after simulation"


def test_simulate_profile():
    """Test the simulate_profile function."""
    # Load a test profile
    profile_path = EXAMPLES_DIR / "Kai_profile.yaml"
    
    # Simulate the profile with multiple iterations
    simulations = simulate_profile(profile_path, iterations=5)
    
    # Check that we get the expected number of simulations
    assert len(simulations) == 5, "Should return the requested number of simulations"
    
    # Check that all simulations are different
    openness_values = [
        sim["digital_archetype"]["traits"]["openness"]["value"]
        for sim in simulations
    ]
    assert len(set(openness_values)) > 1, "Multiple simulations should have different values"


def test_summarize_simulations():
    """Test the summarize_simulations function."""
    # Load a test profile
    profile_path = EXAMPLES_DIR / "Kai_profile.yaml"
    
    # Simulate the profile with multiple iterations
    simulations = simulate_profile(profile_path, iterations=10)
    
    # Generate summary
    summary = summarize_simulations(simulations)
    
    # Check that the summary contains expected traits
    assert "openness" in summary
    assert "conscientiousness" in summary
    assert "extraversion" in summary
    assert "agreeableness" in summary
    assert "neuroticism" in summary
    
    # Check that each trait summary has the expected statistics
    for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
        assert "mean" in summary[trait]
        assert "median" in summary[trait]
        assert "std_dev" in summary[trait]
        assert "min" in summary[trait]
        assert "max" in summary[trait]
        assert "samples" in summary[trait]
        assert summary[trait]["samples"] == 10


def test_empty_simulations_summary():
    """Test that summarize_simulations handles empty input."""
    summary = summarize_simulations([])
    assert summary == {}, "Summary of empty simulations should be an empty dict"
