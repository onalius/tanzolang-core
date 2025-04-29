"""
Tests for the exporter module of the tanzo_schema package.
"""

import json
import yaml
import pytest

from clients.python.tanzo_schema import export_shorthand
from clients.python.tanzo_schema.exporter import export_to_json, export_to_yaml
from clients.python.tanzo_schema.models import Archetype, Profile, Trait, TanzoDocument


def test_export_to_json():
    """Test exporting a document to JSON."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8,
                    traits=[
                        Trait(
                            name="trait1",
                            value=0.5
                        )
                    ]
                )
            ]
        )
    )
    
    json_str = export_to_json(document)
    parsed = json.loads(json_str)
    
    assert parsed["version"] == "0.1.0"
    assert parsed["profile"]["name"] == "Test Profile"
    assert parsed["profile"]["archetypes"][0]["type"] == "digital"
    assert parsed["profile"]["archetypes"][0]["traits"][0]["name"] == "trait1"


def test_export_to_yaml():
    """Test exporting a document to YAML."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8,
                    traits=[
                        Trait(
                            name="trait1",
                            value=0.5
                        )
                    ]
                )
            ]
        )
    )
    
    yaml_str = export_to_yaml(document)
    parsed = yaml.safe_load(yaml_str)
    
    assert parsed["version"] == "0.1.0"
    assert parsed["profile"]["name"] == "Test Profile"
    assert parsed["profile"]["archetypes"][0]["type"] == "digital"
    assert parsed["profile"]["archetypes"][0]["traits"][0]["name"] == "trait1"


def test_export_shorthand_document():
    """Test exporting a document to shorthand format."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8,
                    traits=[
                        Trait(
                            name="trait1",
                            value=0.5
                        ),
                        Trait(
                            name="trait2",
                            value=0.7
                        )
                    ]
                ),
                Archetype(
                    type="social",
                    weight=0.6
                )
            ]
        )
    )
    
    shorthand = export_shorthand(document)
    
    assert "Test Profile" in shorthand
    assert "dig:0.8" in shorthand
    assert "trait1:0.5" in shorthand
    assert "trait2:0.7" in shorthand
    assert "soc:0.6" in shorthand


def test_export_shorthand_file(example_file_path):
    """Test exporting a file to shorthand format."""
    shorthand = export_shorthand(example_file_path)
    
    assert isinstance(shorthand, str)
    assert len(shorthand) > 0


def test_export_to_json_pretty():
    """Test exporting a document to pretty-printed JSON."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8
                )
            ]
        )
    )
    
    json_str = export_to_json(document, pretty=True)
    
    # Pretty-printed JSON should include line breaks
    assert "\n" in json_str
    
    json_str_compact = export_to_json(document, pretty=False)
    
    # Compact JSON should not include line breaks
    assert "\n" not in json_str_compact
    
    # But both should parse to the same object
    assert json.loads(json_str) == json.loads(json_str_compact)
