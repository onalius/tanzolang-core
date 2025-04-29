"""
Pytest configuration file for Tanzo Schema tests.
"""

import json
import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def sample_profile_dict():
    """Return a sample profile dictionary for testing."""
    return {
        "version": "0.1.0",
        "profile": {
            "id": "test-profile",
            "type": "human",
            "properties": {
                "name": "Test Person",
                "description": "A test profile for unit tests",
                "traits": [
                    {"name": "creativity", "value": 75, "variance": 10},
                    {"name": "logic", "value": 80, "variance": 5},
                ],
                "archetypes": [
                    {
                        "name": "tester",
                        "influence": 90,
                        "description": "Testing archetype",
                        "traits": [
                            {"name": "precision", "value": 85},
                            {"name": "thoroughness", "value": 90},
                        ],
                    }
                ],
                "capabilities": [
                    {
                        "name": "testing",
                        "level": 95,
                        "description": "Software testing capability",
                    }
                ],
            },
        },
    }


@pytest.fixture
def sample_profile_file(tmp_path, sample_profile_dict):
    """Create a sample profile YAML file for testing."""
    # Create a temporary YAML file
    test_file = tmp_path / "test_profile.yaml"
    with open(test_file, "w") as f:
        yaml.dump(sample_profile_dict, f)
    return test_file


@pytest.fixture
def sample_invalid_profile_file(tmp_path):
    """Create an invalid profile YAML file for testing."""
    # Create a temporary invalid YAML file
    test_file = tmp_path / "invalid_profile.yaml"
    invalid_profile = {
        "version": "0.1.0",
        "profile": {
            "id": "invalid-profile",
            # Missing required 'type' field
            "properties": {
                "name": "Invalid Profile",
                # Missing required 'name' field in traits
                "traits": [{"value": 75, "variance": 10}],
            },
        },
    }
    with open(test_file, "w") as f:
        yaml.dump(invalid_profile, f)
    return test_file


@pytest.fixture
def schema_file():
    """Return the path to the schema file."""
    schema_path = Path(__file__).resolve().parent.parent / "spec" / "tanzo-schema.json"
    return schema_path
