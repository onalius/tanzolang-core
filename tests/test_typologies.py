"""Tests for typology functionality in TanzoLang"""

import json
import os
from pathlib import Path
import yaml
import pytest

from clients.python.tanzo_schema.models import TanzoProfile
from clients.python.tanzo_schema.validator import validate_profile
from clients.python.tanzo_schema.simulator import extract_typologies

# Root directory of the repo
ROOT_DIR = Path(__file__).parent.parent


class TestTypologySupport:
    """Tests for typology systems in TanzoLang"""
    
    def test_load_profile_with_typologies(self):
        """Test loading a profile that includes multiple typology systems"""
        example_path = ROOT_DIR / "examples" / "profiles" / "hermit_with_typologies.yaml"
        
        # Skip if file doesn't exist
        if not example_path.exists():
            pytest.skip(f"Test file not found: {example_path}")
        
        # Load profile directly
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        # Validate via model
        profile = TanzoProfile.parse_obj(profile_data)
        
        # Verify typologies exist and have correct structure
        assert profile.profile.typologies is not None, "Typologies should be present"
        
        # Check Zodiac typology
        assert profile.profile.typologies.zodiac is not None, "Zodiac typology should be present"
        assert profile.profile.typologies.zodiac.sun == "Virgo", "Sun sign should be Virgo"
        assert profile.profile.typologies.zodiac.moon == "Capricorn", "Moon sign should be Capricorn"
        assert profile.profile.typologies.zodiac.rising == "Scorpio", "Rising sign should be Scorpio"
        
        # Check Kabbalah typology
        assert profile.profile.typologies.kabbalah is not None, "Kabbalah typology should be present"
        assert profile.profile.typologies.kabbalah.primary_sefira == "Binah", "Primary sefira should be Binah"
        assert profile.profile.typologies.kabbalah.secondary_sefira == "Hokhmah", "Secondary sefira should be Hokhmah"
        
        # Check Purpose Quadrant typology
        assert profile.profile.typologies.purpose_quadrant is not None, "Purpose quadrant typology should be present"
        assert profile.profile.typologies.purpose_quadrant.passion == "Seeking inner truth", "Passion should match"
        assert profile.profile.typologies.purpose_quadrant.expertise == "Reflection and discernment", "Expertise should match"
    
    def test_extract_typologies(self):
        """Test extracting typology information from a profile"""
        example_path = ROOT_DIR / "examples" / "profiles" / "hermit_with_typologies.yaml"
        
        # Skip if file doesn't exist
        if not example_path.exists():
            pytest.skip(f"Test file not found: {example_path}")
        
        # Load profile directly
        with open(example_path, "r") as f:
            profile_data = yaml.safe_load(f)
        
        # Validate via model
        profile = TanzoProfile.parse_obj(profile_data)
        
        # Extract typologies
        typologies = extract_typologies(profile)
        
        # Verify typology information was extracted correctly
        assert isinstance(typologies, dict), "Extracted typologies should be a dictionary"
        assert len(typologies) >= 3, "At least three typology systems should be extracted"
        
        # Check Zodiac typology extraction
        assert "zodiac" in typologies, "Zodiac should be extracted"
        assert "sun" in typologies["zodiac"], "Sun sign should be extracted"
        assert typologies["zodiac"]["sun"] == "Virgo", "Sun sign should be Virgo"
        assert "moon" in typologies["zodiac"], "Moon sign should be extracted"
        assert typologies["zodiac"]["moon"] == "Capricorn", "Moon sign should be Capricorn"
        
        # Check Kabbalah typology extraction
        assert "kabbalah" in typologies, "Kabbalah should be extracted"
        assert "primary_sefira" in typologies["kabbalah"], "Primary sefira should be extracted"
        assert typologies["kabbalah"]["primary_sefira"] == "Binah", "Primary sefira should be Binah"
        
        # Check Purpose Quadrant typology extraction
        assert "purpose_quadrant" in typologies, "Purpose quadrant should be extracted"
        assert "passion" in typologies["purpose_quadrant"], "Passion should be extracted"
        assert typologies["purpose_quadrant"]["passion"] == "Seeking inner truth", "Passion should match"
        assert "expertise" in typologies["purpose_quadrant"], "Expertise should be extracted"
        assert typologies["purpose_quadrant"]["expertise"] == "Reflection and discernment", "Expertise should match"
        
    def test_typology_validation(self):
        """Test validation with typology references"""
        example_path = ROOT_DIR / "examples" / "profiles" / "hermit_with_typologies.yaml"
        
        # Skip if file doesn't exist
        if not example_path.exists():
            pytest.skip(f"Test file not found: {example_path}")
            
        # Validate profile
        profile = validate_profile(example_path)
        
        # Verify the profile validates successfully with typologies
        assert profile.profile.typologies is not None, "Typologies should be validated"
        assert profile.profile.typologies.zodiac is not None, "Zodiac typology should be validated"
        assert profile.profile.typologies.kabbalah is not None, "Kabbalah typology should be validated"
        assert profile.profile.typologies.purpose_quadrant is not None, "Purpose quadrant typology should be validated"
