"""
Tests for the exporter functionality.
"""

import json
import yaml
import pytest
import tempfile
from pathlib import Path

from clients.python.tanzo_schema import (
    TanzoProfile, export_profile_shorthand,
    load_profile_from_yaml
)
from clients.python.tanzo_schema.exporters import (
    export_profile_json, export_profile_yaml
)


def test_export_profile_shorthand():
    """Test exporting profile as shorthand string."""
    # Test minimal profile
    minimal_profile = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            }
        }
    )
    
    shorthand = export_profile_shorthand(minimal_profile)
    assert shorthand == "Test Profile [guide]"
    
    # Test with secondary archetype
    profile_with_secondary = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide",
                "secondary": "educator"
            }
        }
    )
    
    shorthand = export_profile_shorthand(profile_with_secondary)
    assert shorthand == "Test Profile [guide/educator]"
    
    # Test with personality traits
    profile_with_personality = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            },
            "personality": {
                "traits": {
                    "openness": 0.7,
                    "conscientiousness": 0.6,
                    "extraversion": 0.5,
                    "agreeableness": 0.8,
                    "neuroticism": 0.3
                }
            }
        }
    )
    
    shorthand = export_profile_shorthand(profile_with_personality)
    assert "Test Profile [guide]" in shorthand
    assert "O:0.7 C:0.6 E:0.5 A:0.8 N:0.3" in shorthand
    
    # Test with communication style
    profile_with_communication = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            },
            "communication": {
                "style": "technical",
                "tone": "professional"
            }
        }
    )
    
    shorthand = export_profile_shorthand(profile_with_communication)
    assert "Test Profile [guide]" in shorthand
    assert "technical, professional" in shorthand


def test_export_profile_json():
    """Test exporting profile as JSON."""
    minimal_profile = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            }
        }
    )
    
    # Test exporting as string
    json_str = export_profile_json(minimal_profile)
    data = json.loads(json_str)
    assert data["version"] == "0.1.0"
    assert data["profile"]["name"] == "Test Profile"
    assert data["profile"]["archetype"]["primary"] == "guide"
    
    # Test exporting to file
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        tmp_path = Path(tmp.name)
        export_profile_json(minimal_profile, tmp_path)
        
        with open(tmp_path, "r") as f:
            file_content = f.read()
        
        data = json.loads(file_content)
        assert data["version"] == "0.1.0"
        assert data["profile"]["name"] == "Test Profile"


def test_export_profile_yaml():
    """Test exporting profile as YAML."""
    minimal_profile = TanzoProfile(
        version="0.1.0",
        profile={
            "name": "Test Profile",
            "archetype": {
                "primary": "guide"
            }
        }
    )
    
    # Test exporting as string
    yaml_str = export_profile_yaml(minimal_profile)
    data = yaml.safe_load(yaml_str)
    assert data["version"] == "0.1.0"
    assert data["profile"]["name"] == "Test Profile"
    assert data["profile"]["archetype"]["primary"] == "guide"
    
    # Test exporting to file
    with tempfile.NamedTemporaryFile(suffix=".yaml") as tmp:
        tmp_path = Path(tmp.name)
        export_profile_yaml(minimal_profile, tmp_path)
        
        with open(tmp_path, "r") as f:
            file_content = f.read()
        
        data = yaml.safe_load(file_content)
        assert data["version"] == "0.1.0"
        assert data["profile"]["name"] == "Test Profile"


def test_export_kai_profile():
    """Test exporting the Kai example profile."""
    examples_dir = Path(__file__).parent.parent / "examples"
    kai_path = examples_dir / "Kai_profile.yaml"
    profile = load_profile_from_yaml(kai_path)
    
    # Test shorthand export
    shorthand = export_profile_shorthand(profile)
    assert "Kai - Technical Advisor" in shorthand
    assert "[advisor/expert]" in shorthand
    
    # Test JSON export
    json_str = export_profile_json(profile)
    data = json.loads(json_str)
    assert data["profile"]["name"] == "Kai - Technical Advisor"
    
    # Test YAML export
    yaml_str = export_profile_yaml(profile)
    data = yaml.safe_load(yaml_str)
    assert data["profile"]["name"] == "Kai - Technical Advisor"
