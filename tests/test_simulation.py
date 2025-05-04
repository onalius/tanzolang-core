"""
Tests for simulation functionality
"""

import os
from pathlib import Path

import pytest

from clients.python.tanzo_schema.models import TanzoProfile
from clients.python.tanzo_schema.simulator import simulate_profile
from clients.python.tanzo_schema.simulator import extract_typologies

# Root directory of the repo
ROOT_DIR = Path(__file__).parent.parent


class TestSimulation:
    """Tests for the simulation functions"""
    
    def test_simulation_with_typologies(self):
        """Test simulation with a profile that includes typologies"""
        # Load a profile with typologies
        example_path = ROOT_DIR / "examples" / "profiles" / "hermit_with_typologies.yaml"
        with open(example_path, "r") as f:
            import yaml
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Verify typologies exist before simulation
        assert profile.profile.typologies is not None, "Typologies should be present"
        assert profile.profile.typologies.zodiac is not None, "Zodiac typology should be present"
        assert profile.profile.typologies.kabbalah is not None, "Kabbalah typology should be present"
        assert profile.profile.typologies.purpose_quadrant is not None, "Purpose quadrant typology should be present"
        
        # Extract typologies and verify their content
        typologies = extract_typologies(profile)
        assert "zodiac" in typologies, "Zodiac should be extracted"
        assert "sun" in typologies["zodiac"], "Sun sign should be extracted"
        assert typologies["zodiac"]["sun"] == "Virgo", "Sun sign should be Virgo"
        
        assert "kabbalah" in typologies, "Kabbalah should be extracted"
        assert "primary_sefira" in typologies["kabbalah"], "Primary sefira should be extracted"
        assert typologies["kabbalah"]["primary_sefira"] == "Binah", "Primary sefira should be Binah"
        
        assert "purpose_quadrant" in typologies, "Purpose quadrant should be extracted"
        assert "passion" in typologies["purpose_quadrant"], "Passion should be extracted"
        assert typologies["purpose_quadrant"]["passion"] == "Seeking inner truth", "Passion should match"
    
    def test_apply_variance(self):
        """Test that variance is applied correctly"""
        # Test with no variance
        base_value = 50.0
        result = _apply_variance(base_value, None)
        assert result == base_value, "Applying no variance should return the base value"
        
        result = _apply_variance(base_value, 0)
        assert result == base_value, "Applying zero variance should return the base value"
        
        # Test with variance (run multiple times since it's random)
        variance = 10.0
        results = set()
        
        for _ in range(20):
            result = _apply_variance(base_value, variance)
            results.add(result)
            
            # Ensure result is within valid range
            assert 0 <= result <= 100, "Result should be within valid range (0-100)"
        
        # Ensure we got different values (randomness test)
        assert len(results) > 1, "Multiple calls with variance should produce different values"
    
    def test_should_activate_capability(self):
        """Test capability activation probability"""
        # Test with power 0 (should never activate)
        activations = sum(_should_activate_capability(0) for _ in range(100))
        assert activations == 0, "Power 0 should never activate"
        
        # Test with power 10 (should always activate)
        activations = sum(_should_activate_capability(10) for _ in range(100))
        assert activations == 100, "Power 10 should always activate"
        
        # Test with power 5 (should activate ~50% of the time)
        activations = sum(_should_activate_capability(5) for _ in range(1000))
        assert 400 <= activations <= 600, "Power 5 should activate roughly 50% of the time"
    
    def test_simulate_profile(self):
        """Test profile simulation"""
        # Load a test profile
        example_path = ROOT_DIR / "examples" / "Kai_profile.yaml"
        with open(example_path, "r") as f:
            import yaml
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Run simulation with a small number of iterations
        iterations = 10
        result = simulate_profile(profile, iterations)
        
        # Check that the result contains the expected data
        assert result.profile_name == profile.profile.name
        assert result.iterations == iterations
        assert len(result.energy_values) == iterations
        assert len(result.resilience_values) == iterations
        assert len(result.adaptability_values) == iterations
        
        # Check that capability activations were tracked
        capability_names = {cap.name for cap in profile.properties.capabilities}
        for name in capability_names:
            assert name in result.capability_activations
        
        # Test that we can get a summary
        summary = result.get_summary()
        assert summary["profile_name"] == profile.profile.name
        assert summary["iterations"] == iterations
        assert "energy" in summary
        assert "resilience" in summary
        assert "adaptability" in summary
        assert "capability_activations" in summary
        
        # Test string representation
        str_result = str(result)
        assert profile.profile.name in str_result
        assert str(iterations) in str_result
    
    def test_simulation_with_minimal_profile(self):
        """Test simulation with a minimal profile"""
        # Load a minimal test profile
        example_path = ROOT_DIR / "examples" / "digital_archetype_only.yaml"
        with open(example_path, "r") as f:
            import yaml
            profile_data = yaml.safe_load(f)
        
        profile = TanzoProfile.model_validate(profile_data)
        
        # Run simulation
        result = simulate_profile(profile)
        
        # Basic checks
        assert result.profile_name == profile.profile.name
        assert result.iterations == 100  # Default value
        
        # Test string representation
        str_result = str(result)
        assert profile.profile.name in str_result
