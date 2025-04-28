"""
Tests for export functionality
"""

import os
import json
from pathlib import Path

import pytest
import yaml

from clients.python.tanzo_schema import TanzoProfile, export_profile

# Root directory of the repo
ROOT_DIR = Path(__file__).parent.parent


class TestExport:
    """Tests for the export functions"""
    
    def test_export_shorthand(self):
        """Test export to shorthand format"""
        # Load a test profile
        example_path = ROOT_DIR / "examples" / "Kai_profile.yaml"
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Export to shorthand
        result = export_profile(profile, format="shorthand")
        
        # Check basic format
        assert profile.profile.name in result
        assert profile.profile.version in result
        assert profile.archetype.type.value in result
        
        # Check for specific shorthand elements
        assert "@" in result  # Separator between name and version
        assert "[" in result and "]" in result  # Archetype brackets
        assert "E" in result and "R" in result and "A" in result  # State markers
        assert "«" in result and "»" in result  # Capability markers
    
    def test_export_json(self):
        """Test export to JSON format"""
        # Load a test profile
        example_path = ROOT_DIR / "examples" / "Kai_profile.yaml"
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Export to JSON
        result = export_profile(profile, format="json")
        
        # Verify the result is valid JSON and contains expected data
        json_data = json.loads(result)
        assert json_data["profile"]["name"] == profile.profile.name
        assert json_data["profile"]["version"] == profile.profile.version
        assert json_data["archetype"]["type"] == profile.archetype.type.value
    
    def test_export_yaml(self):
        """Test export to YAML format"""
        # Load a test profile
        example_path = ROOT_DIR / "examples" / "Kai_profile.yaml"
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Export to YAML
        result = export_profile(profile, format="yaml")
        
        # Verify the result is valid YAML and contains expected data
        yaml_data = yaml.safe_load(result)
        assert yaml_data["profile"]["name"] == profile.profile.name
        assert yaml_data["profile"]["version"] == profile.profile.version
        assert yaml_data["archetype"]["type"] == profile.archetype.type.value
    
    def test_export_invalid_format(self):
        """Test export with an invalid format"""
        # Load a test profile
        example_path = ROOT_DIR / "examples" / "Kai_profile.yaml"
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Try to export with an invalid format
        with pytest.raises(ValueError):
            export_profile(profile, format="invalid")
    
    def test_export_minimal_profile(self):
        """Test export with a minimal profile"""
        # Load a minimal test profile
        example_path = ROOT_DIR / "examples" / "digital_archetype_only.yaml"
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Export to all formats
        shorthand = export_profile(profile, format="shorthand")
        json_data = json.loads(export_profile(profile, format="json"))
        yaml_data = yaml.safe_load(export_profile(profile, format="yaml"))
        
        # Check that the exports contain the expected data
        assert profile.profile.name in shorthand
        assert json_data["profile"]["name"] == profile.profile.name
        assert yaml_data["profile"]["name"] == profile.profile.name
