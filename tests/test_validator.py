"""
Tests for the validator module of the Python SDK.
"""

import os
from pathlib import Path
import pytest
import yaml
from clients.python.tanzo_schema import SchemaValidator, ValidationResult
from clients.python.tanzo_schema.models import Profile


class TestValidator:
    """Tests for the SchemaValidator class."""

    def test_validate_valid_json(self, schema_validator, example_profile_path):
        """Test validating valid JSON data."""
        with open(example_profile_path, 'r') as f:
            profile = yaml.safe_load(f)
        
        result = schema_validator.validate_json(profile)
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert not result.errors

    def test_validate_invalid_json(self, schema_validator):
        """Test validating invalid JSON data."""
        invalid_profile = {
            "profile": {
                "name": "Invalid Profile"
                # Missing required version field
            },
            "archetypes": []  # Empty array, requires at least one item
        }
        
        result = schema_validator.validate_json(invalid_profile)
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_validate_valid_yaml(self, schema_validator, example_profile_path):
        """Test validating valid YAML data."""
        with open(example_profile_path, 'r') as f:
            yaml_string = f.read()
        
        result = schema_validator.validate_yaml(yaml_string)
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert not result.errors

    def test_validate_invalid_yaml(self, schema_validator):
        """Test validating invalid YAML data."""
        invalid_yaml = """
        profile:
          name: Invalid Profile
          # Missing required version field
        archetypes: []  # Empty array, requires at least one item
        """
        
        result = schema_validator.validate_yaml(invalid_yaml)
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_validate_valid_file(self, schema_validator, example_profile_path):
        """Test validating a valid file."""
        result = schema_validator.validate_file(example_profile_path)
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert not result.errors

    def test_validate_nonexistent_file(self, schema_validator):
        """Test validating a nonexistent file."""
        result = schema_validator.validate_file("nonexistent.yaml")
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert "not found" in result.errors[0]

    def test_validate_pydantic(self, schema_validator, example_profile_path):
        """Test validating using Pydantic models."""
        with open(example_profile_path, 'r') as f:
            profile = yaml.safe_load(f)
        
        result = schema_validator.validate_pydantic(profile)
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert not result.errors

    def test_bool_conversion(self):
        """Test that ValidationResult can be used in boolean context."""
        valid_result = ValidationResult(True)
        invalid_result = ValidationResult(False, ["Error"])
        
        assert bool(valid_result) is True
        assert bool(invalid_result) is False
        
        # Test in if statements
        if valid_result:
            pass  # This should execute
        else:
            pytest.fail("Valid result evaluated as False")
        
        if not invalid_result:
            pass  # This should execute
        else:
            pytest.fail("Invalid result evaluated as True")


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
