"""
Tests for the TanzoValidator class.
"""

import json
import os
from pathlib import Path

import pytest
import yaml

from clients.python.tanzo_schema import TanzoProfile, TanzoValidator


@pytest.fixture
def validator():
    """Return a TanzoValidator instance."""
    return TanzoValidator()


@pytest.fixture
def example_profile_path():
    """Return the path to an example profile."""
    return Path(__file__).parent.parent / "examples" / "Kai_profile.yaml"


@pytest.fixture
def digital_profile_path():
    """Return the path to the digital archetype example profile."""
    return Path(__file__).parent.parent / "examples" / "digital_archetype_only.yaml"


@pytest.fixture
def example_profile_data(example_profile_path):
    """Load example profile data."""
    with open(example_profile_path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture
def digital_profile_data(digital_profile_path):
    """Load digital profile data."""
    with open(digital_profile_path, "r") as f:
        return yaml.safe_load(f)


def test_validate_dict_valid(validator, example_profile_data):
    """Test validating a valid dictionary."""
    is_valid, errors = validator.validate_dict(example_profile_data)
    assert is_valid
    assert len(errors) == 0


def test_validate_dict_invalid(validator):
    """Test validating an invalid dictionary."""
    invalid_data = {
        "identity": {
            "name": "Test Entity"
        },
        # Missing required 'archetype' property
        "traits": {}
    }
    
    is_valid, errors = validator.validate_dict(invalid_data)
    assert not is_valid
    assert len(errors) > 0
    assert any("archetype" in error.lower() for error in errors)


def test_validate_file_valid(validator, example_profile_path):
    """Test validating a valid file."""
    is_valid, errors = validator.validate_file(str(example_profile_path))
    assert is_valid
    assert len(errors) == 0


def test_validate_file_nonexistent(validator):
    """Test validating a nonexistent file."""
    is_valid, errors = validator.validate_file("nonexistent.yaml")
    assert not is_valid
    assert len(errors) > 0
    assert any("error loading file" in error.lower() for error in errors)


def test_validate_file_invalid_extension(validator, tmp_path):
    """Test validating a file with an invalid extension."""
    file_path = tmp_path / "profile.txt"
    with open(file_path, "w") as f:
        f.write("This is not a YAML or JSON file")
    
    is_valid, errors = validator.validate_file(str(file_path))
    assert not is_valid
    assert len(errors) > 0
    assert any("unsupported file extension" in error.lower() for error in errors)


def test_validate_pydantic_valid(validator, example_profile_data):
    """Test validating a valid Pydantic model."""
    profile = TanzoProfile(**example_profile_data)
    is_valid, errors = validator.validate_pydantic(profile)
    assert is_valid
    assert len(errors) == 0


def test_validate_pydantic_missing_optional(validator):
    """Test validating a Pydantic model with missing optional fields."""
    minimal_data = {
        "identity": {
            "name": "Test Entity"
        },
        "archetype": {
            "primary": "Sage"
        },
        "traits": {}
    }
    
    profile = TanzoProfile(**minimal_data)
    is_valid, errors = validator.validate_pydantic(profile)
    assert is_valid
    assert len(errors) == 0


def test_validate_both_example_files(validator, example_profile_path, digital_profile_path):
    """Test validating both example files."""
    # Validate Kai profile
    is_valid, errors = validator.validate_file(str(example_profile_path))
    assert is_valid
    assert len(errors) == 0
    
    # Validate digital archetype profile
    is_valid, errors = validator.validate_file(str(digital_profile_path))
    assert is_valid
    assert len(errors) == 0
