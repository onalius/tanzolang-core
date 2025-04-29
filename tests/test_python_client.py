"""
Tests for the Python SDK client.
"""

import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from clients.python.tanzo_schema import (
    TanzoProfile,
    DigitalArchetype,
    Identity,
    Trait,
    CognitiveModel,
    simulate_profile,
    export_shorthand,
)
from clients.python.tanzo_schema.utils import (
    to_dict,
    to_json,
    to_yaml,
)


def test_create_profile_programmatically():
    """Test creating a profile using the Python SDK."""
    profile = TanzoProfile(
        profile={
            "name": "Test Profile",
            "version": "0.1.0",
            "author": "Test Author"
        },
        digital_archetype=DigitalArchetype(
            identity=Identity(
                name="Test Character",
                age=25
            ),
            traits={
                "trait1": Trait(value=0.5),
                "trait2": Trait(value=0.7, variance=0.1)
            }
        )
    )
    
    assert profile.profile.name == "Test Profile"
    assert profile.digital_archetype.identity.name == "Test Character"
    assert profile.digital_archetype.traits["trait1"].value == 0.5


def test_trait_validations():
    """Test trait value validations."""
    # Valid trait
    trait = Trait(value=0.5, variance=0.1)
    assert trait.value == 0.5
    
    # Invalid trait value (too high)
    with pytest.raises(ValidationError):
        Trait(value=1.5)
    
    # Invalid trait value (too low)
    with pytest.raises(ValidationError):
        Trait(value=-0.5)
    
    # Invalid trait variance (too high)
    with pytest.raises(ValidationError):
        Trait(value=0.5, variance=1.5)


def test_profile_simulation(sample_profile):
    """Test profile simulation functionality."""
    # Run simulation
    results = simulate_profile(sample_profile, num_iterations=50, seed=42)
    
    # Check results
    assert results.profile_name == "Test Profile"
    assert results.num_iterations == 50
    
    # Check that we have all traits
    for trait_name in sample_profile.digital_archetype.traits:
        assert trait_name in results.trait_means
        assert trait_name in results.trait_stddevs
        assert trait_name in results.trait_ranges
    
    # Check output summary
    summary = results.summary()
    assert "Simulation Results for 'Test Profile'" in summary
    assert "Number of iterations: 50" in summary


def test_export_shorthand(sample_profile):
    """Test shorthand export functionality."""
    shorthand = export_shorthand(sample_profile)
    
    # Expected components in the shorthand
    assert "Test Character" in shorthand
    assert "age:25" in shorthand
    assert "traits:" in shorthand


def test_serialization_functions(sample_profile):
    """Test serialization utility functions."""
    # Convert to dict
    profile_dict = to_dict(sample_profile)
    assert isinstance(profile_dict, dict)
    assert profile_dict["profile"]["name"] == "Test Profile"
    
    # Convert to JSON
    json_str = to_json(sample_profile)
    assert isinstance(json_str, str)
    assert "Test Profile" in json_str
    
    # Convert to YAML
    yaml_str = to_yaml(sample_profile)
    assert isinstance(yaml_str, str)
    assert "Test Profile" in yaml_str
