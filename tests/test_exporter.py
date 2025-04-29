"""
Tests for the TanzoLang exporter.
"""

import json
import os
from pathlib import Path

import pytest

from tanzo_schema.exporter import (
    _get_trait_shorthand,
    _get_trait_summary,
    generate_shorthand,
    export_profile,
)
from tanzo_schema.validator import load_profile


# Find the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"


def test_get_trait_shorthand():
    """Test the _get_trait_shorthand function."""
    # Test trait with value only
    trait = {"value": 75}
    shorthand = _get_trait_shorthand(trait)
    assert shorthand == "75"
    
    # Test trait with value and variance
    trait = {"value": 75, "variance": 10}
    shorthand = _get_trait_shorthand(trait)
    assert shorthand == "75±10"
    
    # Test trait with description (should be ignored in shorthand)
    trait = {"value": 75, "variance": 10, "description": "Test trait"}
    shorthand = _get_trait_shorthand(trait)
    assert shorthand == "75±10"


def test_get_trait_summary():
    """Test the _get_trait_summary function."""
    traits = {
        "openness": {"value": 75, "variance": 10},
        "conscientiousness": {"value": 82, "variance": 8},
        "extraversion": {"value": 60, "variance": 15},
        "agreeableness": {"value": 70, "variance": 12},
        "neuroticism": {"value": 35, "variance": 10}
    }
    
    summary = _get_trait_summary(traits)
    
    # Check that all traits are included
    assert "O:75±10" in summary
    assert "C:82±8" in summary
    assert "E:60±15" in summary
    assert "A:70±12" in summary
    assert "N:35±10" in summary


def test_generate_shorthand():
    """Test the generate_shorthand function."""
    # Load a test profile
    profile_path = EXAMPLES_DIR / "Kai_profile.yaml"
    profile_data = load_profile(profile_path)
    
    shorthand = generate_shorthand(profile_data)
    
    # Check that the shorthand contains the profile name
    assert "Kai" in shorthand
    
    # Check that the shorthand contains trait codes
    assert "O:" in shorthand
    assert "C:" in shorthand
    assert "E:" in shorthand
    assert "A:" in shorthand
    assert "N:" in shorthand


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_export_profile_shorthand(example_file):
    """Test the export_profile function with shorthand format."""
    example_path = EXAMPLES_DIR / example_file
    
    shorthand = export_profile(example_path, "shorthand")
    
    # Load profile to verify
    profile_data = load_profile(example_path)
    profile_name = profile_data["metadata"]["name"]
    
    # Check that the shorthand contains the profile name
    assert profile_name in shorthand
    
    # Check that the shorthand contains trait codes
    assert "O:" in shorthand


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_export_profile_json(example_file):
    """Test the export_profile function with JSON format."""
    example_path = EXAMPLES_DIR / example_file
    
    json_export = export_profile(example_path, "json")
    
    # Check that the result is valid JSON
    try:
        data = json.loads(json_export)
        assert "metadata" in data
        assert "digital_archetype" in data
    except json.JSONDecodeError:
        pytest.fail("Export is not valid JSON")


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_export_profile_dict(example_file):
    """Test the export_profile function with dict format."""
    example_path = EXAMPLES_DIR / example_file
    
    dict_export = export_profile(example_path, "dict")
    
    # Check that the result is a dictionary with expected structure
    assert isinstance(dict_export, dict)
    assert "metadata" in dict_export
    assert "digital_archetype" in dict_export


def test_export_invalid_format():
    """Test that export_profile raises an error for invalid formats."""
    example_path = EXAMPLES_DIR / "Kai_profile.yaml"
    
    with pytest.raises(ValueError):
        export_profile(example_path, "invalid_format")
