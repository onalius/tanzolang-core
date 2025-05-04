"""
Tests for validation functionality
"""

import os
from pathlib import Path

import pytest

from clients.python.tanzo_schema import validate_tanzo_profile, TanzoProfile

# Root directory of the repo
ROOT_DIR = Path(__file__).parent.parent


class TestValidation:
    """Tests for the validation functions"""
    
    def test_validation_with_typologies(self):
        """Test validation with a profile that includes typologies"""
        example_path = ROOT_DIR / "examples" / "profiles" / "hermit_with_typologies.yaml"
        is_valid, errors = validate_tanzo_profile(example_path)
        
        assert is_valid, f"Validation should pass for profile with typologies but failed with: {errors}"
        assert errors is None, "No errors should be returned for valid profile with typologies"
        
        # Load the profile as a model to check typology properties
        from clients.python.tanzo_schema.validator import validate_profile
        profile = validate_profile(example_path)
        
        # Verify typologies exist and have expected values
        assert profile.profile.typologies is not None, "Typologies should be loaded"
        assert profile.profile.typologies.zodiac is not None, "Zodiac typology should be loaded"
        assert profile.profile.typologies.zodiac.sun == "Virgo", "Sun sign should be Virgo"
        assert profile.profile.typologies.kabbalah is not None, "Kabbalah typology should be loaded"
        assert profile.profile.typologies.kabbalah.primary_sefira == "Binah", "Primary sefira should be Binah"
        assert profile.profile.typologies.purpose_quadrant is not None, "Purpose quadrant typology should be loaded"
    
    def test_validation_on_valid_profile(self):
        """Test validation with a valid profile"""
        example_path = ROOT_DIR / "examples" / "legacy" / "Kai_profile.yaml"
        is_valid, errors = validate_tanzo_profile(example_path)
        
        assert is_valid, f"Validation should pass but failed with: {errors}"
        assert errors is None, "No errors should be returned for valid profile"
    
    def test_validation_on_minimal_profile(self):
        """Test validation with a minimal profile"""
        example_path = ROOT_DIR / "examples" / "profiles" / "digital_archetype_only.yaml"
        is_valid, errors = validate_tanzo_profile(example_path)
        
        assert is_valid, f"Validation should pass but failed with: {errors}"
        assert errors is None, "No errors should be returned for valid profile"
    
    def test_validation_on_invalid_profile(self):
        """Test validation with an invalid profile"""
        invalid_profile = {
            # Missing required version field
            "profile": {
                "name": "Invalid Profile",
                "archetypes": [{
                    "type": "digital",
                    "attributes": []  # Empty attributes (should have at least 1)
                }]
            }
        }
        
        is_valid, errors = validate_tanzo_profile(invalid_profile)
        
        assert not is_valid, "Validation should fail for invalid profile"
        assert errors is not None, "Errors should be returned for invalid profile"
        assert len(errors) >= 1, "At least one error should be identified"
    
    def test_validation_with_invalid_json_content(self):
        """Test validation with invalid JSON content"""
        invalid_content = '{"profile": {"name": "Invalid", "version": "1.0.0"}, "incomplete": true'
        
        is_valid, errors = validate_tanzo_profile(invalid_content)
        
        assert not is_valid, "Validation should fail for invalid JSON/YAML content"
        assert errors is not None, "Errors should be returned for invalid content"
    
    def test_pydantic_model_validation(self):
        """Test validation through the Pydantic model"""
        valid_profile = {
            "version": "1.0.0",
            "profile": {
                "name": "Test Profile",
                "archetypes": [{
                    "type": "digital",
                    "attributes": [{
                        "name": "test attribute",
                        "value": "test"
                    }]
                }]
            }
        }
        
        # This should not raise an exception
        profile = TanzoProfile.parse_obj(valid_profile)
        assert profile.profile.name == "Test Profile"
        
        # Test with an invalid value
        invalid_profile = valid_profile.copy()
        # Need to create a deep copy for nested dictionaries
        invalid_profile["profile"] = dict(valid_profile["profile"])
        invalid_profile["profile"]["archetypes"] = list(valid_profile["profile"]["archetypes"])
        invalid_profile["profile"]["archetypes"][0] = dict(valid_profile["profile"]["archetypes"][0])
        invalid_profile["profile"]["archetypes"][0]["type"] = "unknown"  # Invalid enum value
        
        with pytest.raises(Exception):
            TanzoProfile.parse_obj(invalid_profile)
