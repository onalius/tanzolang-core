"""
Tests for the TanzoExporter class.
"""

import json
import os
from pathlib import Path

import pytest
import yaml

from clients.python.tanzo_schema import TanzoExporter, TanzoProfile


@pytest.fixture
def example_profile_path():
    """Return the path to an example profile."""
    return Path(__file__).parent.parent / "examples" / "Kai_profile.yaml"


@pytest.fixture
def example_profile(example_profile_path):
    """Load and parse the example profile."""
    with open(example_profile_path, "r") as f:
        data = yaml.safe_load(f)
    return TanzoProfile(**data)


@pytest.fixture
def example_exporter(example_profile):
    """Return a TanzoExporter for the example profile."""
    return TanzoExporter(example_profile)


def test_exporter_initialization(example_profile):
    """Test that the exporter initializes correctly."""
    exporter = TanzoExporter(example_profile)
    assert exporter.profile == example_profile


def test_to_json(example_exporter, example_profile):
    """Test exporting to JSON format."""
    json_output = example_exporter.to_json()
    
    # Check that the output is valid JSON
    data = json.loads(json_output)
    
    # Check key attributes
    assert data["identity"]["name"] == example_profile.identity.name
    assert data["archetype"]["primary"] == example_profile.archetype.primary


def test_to_yaml(example_exporter, example_profile):
    """Test exporting to YAML format."""
    yaml_output = example_exporter.to_yaml()
    
    # Check that the output is valid YAML
    data = yaml.safe_load(yaml_output)
    
    # Check key attributes
    assert data["identity"]["name"] == example_profile.identity.name
    assert data["archetype"]["primary"] == example_profile.archetype.primary


def test_to_shorthand(example_exporter):
    """Test exporting to shorthand format."""
    shorthand = example_exporter.to_shorthand()
    
    # Check that the shorthand contains key information
    assert "Kai Yamamoto" in shorthand
    assert "Mentor" in shorthand
    
    # The shorthand should be a single line summary
    assert isinstance(shorthand, str)
    assert len(shorthand.strip().split("\n")) == 1


def test_to_file(example_exporter, tmp_path):
    """Test exporting to a file."""
    # Test JSON export
    json_path = tmp_path / "profile.json"
    example_exporter.to_file(str(json_path))
    
    assert json_path.exists()
    with open(json_path, "r") as f:
        json_data = json.load(f)
    assert json_data["identity"]["name"] == "Kai Yamamoto"
    
    # Test YAML export
    yaml_path = tmp_path / "profile.yaml"
    example_exporter.to_file(str(yaml_path))
    
    assert yaml_path.exists()
    with open(yaml_path, "r") as f:
        yaml_data = yaml.safe_load(f)
    assert yaml_data["identity"]["name"] == "Kai Yamamoto"
    
    # Test shorthand export
    txt_path = tmp_path / "profile.txt"
    example_exporter.to_file(str(txt_path))
    
    assert txt_path.exists()
    with open(txt_path, "r") as f:
        content = f.read()
    assert "Kai Yamamoto" in content


def test_to_file_with_format_override(example_exporter, tmp_path):
    """Test exporting to a file with format override."""
    # Export JSON to a file with a different extension
    weird_path = tmp_path / "profile.weird"
    example_exporter.to_file(str(weird_path), format_type="json")
    
    assert weird_path.exists()
    with open(weird_path, "r") as f:
        json_data = json.load(f)
    assert json_data["identity"]["name"] == "Kai Yamamoto"


def test_to_file_invalid_format(example_exporter, tmp_path):
    """Test error handling for invalid format types."""
    invalid_path = tmp_path / "profile.inv"
    
    # Should raise ValueError with invalid format
    with pytest.raises(ValueError):
        example_exporter.to_file(str(invalid_path), format_type="invalid")
    
    # Should also raise ValueError with unrecognized extension and no format specified
    with pytest.raises(ValueError):
        example_exporter.to_file(str(invalid_path))
