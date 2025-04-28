"""
Tests for the schema validation functionality.
"""

import json
import yaml
import pytest
from pathlib import Path

from clients.python.tanzo_schema import (
    validate_tanzo_profile, load_profile_from_yaml,
    TanzoProfile, Archetype
)
from clients.python.tanzo_schema.validators import _load_schema


def test_load_schema():
    """Test that the schema can be loaded."""
    schema = _load_schema()
    assert schema is not None
    assert schema.get("$schema") == "https://json-schema.org/draft-07/schema#"
    assert schema.get("title") == "TanzoLang Schema"


def test_validate_minimal_profile():
    """Test validation of a minimal profile."""
    minimal_profile = {
        "version": "0.1.0",
        "profile": {
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            }
        }
    }
    
    profile = validate_tanzo_profile(minimal_profile)
    assert profile is not None
    assert profile.version == "0.1.0"
    assert profile.profile.name == "Test Profile"
    assert profile.profile.archetype.primary == "guide"


def test_validate_profile_with_json_string():
    """Test validation with a JSON string."""
    json_string = """
    {
        "version": "0.1.0",
        "profile": {
            "name": "JSON Test",
            "archetype": {
                "primary": "advisor"
            }
        }
    }
    """
    
    profile = validate_tanzo_profile(json_string)
    assert profile is not None
    assert profile.profile.name == "JSON Test"


def test_validate_profile_with_yaml_string():
    """Test validation with a YAML string."""
    yaml_string = """
    version: "0.1.0"
    profile:
      name: "YAML Test"
      archetype:
        primary: "expert"
    """
    
    profile = validate_tanzo_profile(yaml_string)
    assert profile is not None
    assert profile.profile.name == "YAML Test"


def test_load_example_profiles():
    """Test loading the example profiles."""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    # Load Kai profile
    kai_path = examples_dir / "Kai_profile.yaml"
    profile = load_profile_from_yaml(kai_path)
    assert profile is not None
    assert profile.profile.name == "Kai - Technical Advisor"
    
    # Load minimal profile
    minimal_path = examples_dir / "digital_archetype_only.yaml"
    profile = load_profile_from_yaml(minimal_path)
    assert profile is not None
    assert profile.profile.name == "Digital Guide"


def test_invalid_profile_validation():
    """Test validation of invalid profiles."""
    # Missing required field
    invalid_profile = {
        "version": "0.1.0",
        "profile": {
            "name": "Invalid Profile"
            # Missing archetype
        }
    }
    
    with pytest.raises(ValueError):
        validate_tanzo_profile(invalid_profile)
    
    # Invalid enum value
    invalid_profile = {
        "version": "0.1.0",
        "profile": {
            "name": "Invalid Profile",
            "archetype": {
                "primary": "invalid_archetype"  # Invalid value
            }
        }
    }
    
    with pytest.raises(ValueError):
        validate_tanzo_profile(invalid_profile)


def test_secondary_archetype_constraint():
    """Test that secondary archetype must differ from primary."""
    invalid_profile = {
        "version": "0.1.0",
        "profile": {
            "name": "Invalid Profile",
            "archetype": {
                "primary": "guide",
                "secondary": "guide"  # Same as primary
            }
        }
    }
    
    with pytest.raises(ValueError):
        validate_tanzo_profile(invalid_profile)


def test_ratio_constraints():
    """Test that ratio fields are constrained to 0.0-1.0."""
    # Test with value too high
    invalid_profile = {
        "version": "0.1.0",
        "profile": {
            "name": "Invalid Profile",
            "archetype": {
                "primary": "guide"
            },
            "behaviors": [
                {
                    "name": "Test Behavior",
                    "description": "A test behavior",
                    "strength": 1.5  # Invalid: > 1.0
                }
            ]
        }
    }
    
    with pytest.raises(ValueError):
        validate_tanzo_profile(invalid_profile)
    
    # Test with negative value
    invalid_profile["profile"]["behaviors"][0]["strength"] = -0.5
    
    with pytest.raises(ValueError):
        validate_tanzo_profile(invalid_profile)
