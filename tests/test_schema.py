"""
Tests for the TanzoLang schema validation.
"""

import json
import os
from pathlib import Path

import pytest
import yaml

from tanzo_schema import TanzoProfile, validate_profile
from tanzo_schema.validator import load_profile, validate_profile_against_schema, validate_profile_with_pydantic


# Find the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
SPEC_DIR = ROOT_DIR / "spec"


def test_schema_exists():
    """Test that the schema file exists."""
    schema_file = SPEC_DIR / "tanzo-schema.json"
    assert schema_file.exists(), "tanzo-schema.json not found in /spec directory"


def test_schema_is_valid_json():
    """Test that the schema is valid JSON."""
    schema_file = SPEC_DIR / "tanzo-schema.json"
    with open(schema_file, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Schema is not valid JSON: {e}")


def test_yaml_schema_exists():
    """Test that the YAML schema file exists."""
    schema_file = SPEC_DIR / "tanzo-schema.yaml"
    assert schema_file.exists(), "tanzo-schema.yaml not found in /spec directory"


def test_yaml_schema_is_valid():
    """Test that the YAML schema is valid."""
    schema_file = SPEC_DIR / "tanzo-schema.yaml"
    with open(schema_file, "r") as f:
        try:
            yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Schema is not valid YAML: {e}")


def test_example_profiles_exist():
    """Test that example profiles exist."""
    profile_files = list(EXAMPLES_DIR.glob("*.yaml"))
    assert len(profile_files) > 0, "No example profiles found in /examples directory"
    
    assert (EXAMPLES_DIR / "Kai_profile.yaml").exists(), "Kai_profile.yaml not found"
    assert (EXAMPLES_DIR / "digital_archetype_only.yaml").exists(), "digital_archetype_only.yaml not found"


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_example_profiles_are_valid_yaml(example_file):
    """Test that example profiles are valid YAML."""
    example_path = EXAMPLES_DIR / example_file
    with open(example_path, "r") as f:
        try:
            yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"{example_file} is not valid YAML: {e}")


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_example_profiles_validate_against_schema(example_file):
    """Test that example profiles validate against the schema."""
    example_path = EXAMPLES_DIR / example_file
    errors = validate_profile_against_schema(load_profile(example_path))
    assert len(errors) == 0, f"{example_file} schema validation errors: {errors}"


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_example_profiles_validate_with_pydantic(example_file):
    """Test that example profiles validate with Pydantic."""
    example_path = EXAMPLES_DIR / example_file
    errors = validate_profile_with_pydantic(load_profile(example_path))
    assert len(errors) == 0, f"{example_file} Pydantic validation errors: {errors}"


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_example_profiles_validate_with_cli_validator(example_file):
    """Test that example profiles validate with the CLI validator."""
    example_path = EXAMPLES_DIR / example_file
    errors = validate_profile(example_path)
    assert len(errors) == 0, f"{example_file} CLI validation errors: {errors}"


def test_invalid_profile_fails_validation():
    """Test that an invalid profile fails validation."""
    # Create a temporary invalid profile
    invalid_profile = {
        "metadata": {
            "version": "invalid",  # Should be in format X.Y.Z
            "name": "Invalid Profile"
        },
        "digital_archetype": {
            "traits": {
                "openness": {
                    "value": 200  # Value out of range (0-100)
                },
                # Missing required traits
            }
        }
    }
    
    # Test validation
    errors = validate_profile_against_schema(invalid_profile)
    assert len(errors) > 0, "Invalid profile should fail schema validation"
    
    errors = validate_profile_with_pydantic(invalid_profile)
    assert len(errors) > 0, "Invalid profile should fail Pydantic validation"


def test_pydantic_model_creation():
    """Test that we can create a Pydantic model from valid data."""
    example_path = EXAMPLES_DIR / "Kai_profile.yaml"
    profile_data = load_profile(example_path)
    
    try:
        profile = TanzoProfile(**profile_data)
        assert profile.metadata.name == "Kai"
        assert profile.digital_archetype.traits.openness.value == 75
    except Exception as e:
        pytest.fail(f"Failed to create Pydantic model: {e}")
