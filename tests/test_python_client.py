"""
Tests for the Python client library.
"""
import json
import os
from pathlib import Path

import pytest
import yaml

from clients.python.tanzo_schema import (
    TanzoProfile, 
    validate_file, 
    load_profile,
)
from clients.python.tanzo_schema.models import (
    ArchetypeEnum,
    CommunicationStyleEnum,
    Trait,
    Expertise,
    Communication,
    ProfileAttributes,
    PersonalityTraits,
    Profile,
    ProfileMetadata,
)


def test_import_modules():
    """Test that all modules can be imported."""
    import clients.python.tanzo_schema
    import clients.python.tanzo_schema.models
    import clients.python.tanzo_schema.validators


def test_load_profile(kai_profile_path):
    """Test loading a profile from a file."""
    profile = load_profile(kai_profile_path)
    
    assert isinstance(profile, TanzoProfile)
    assert profile.metadata.name == "Kai"
    assert profile.metadata.id == "kai-mentor-profile"
    assert profile.profile.archetype == ArchetypeEnum.MENTOR
    assert len(profile.profile.attributes.personality.traits) == 4


def test_validate_file_with_jsonschema(kai_profile_path):
    """Test validating a file using jsonschema."""
    result = validate_file(kai_profile_path, validator="jsonschema")
    assert result is True


def test_create_profile_programmatically():
    """Test creating a profile programmatically."""
    # Create a minimal valid profile
    profile = TanzoProfile(
        metadata=ProfileMetadata(
            version="0.1.0",
            id="test-profile",
            name="Test Profile",
        ),
        profile=Profile(
            archetype=ArchetypeEnum.GUIDE,
            attributes=ProfileAttributes(
                personality=PersonalityTraits(
                    traits=[
                        Trait(name="helpfulness", value=90),
                    ],
                ),
                expertise=[
                    Expertise(domain="testing", level=80),
                ],
                communication=Communication(
                    style=CommunicationStyleEnum.DIRECT,
                ),
            ),
        ),
    )
    
    assert profile.metadata.name == "Test Profile"
    assert profile.profile.archetype == ArchetypeEnum.GUIDE
    assert profile.profile.attributes.personality.traits[0].name == "helpfulness"
    assert profile.profile.attributes.personality.traits[0].value == 90


def test_profile_model_validation():
    """Test that the profile model validates correctly."""
    # Create an invalid profile (missing required fields)
    with pytest.raises(Exception):
        TanzoProfile(
            metadata=ProfileMetadata(
                # Missing required 'version', 'id', and 'name'
                description="Invalid profile",
            ),
            profile=Profile(
                archetype=ArchetypeEnum.GUIDE,
                attributes=ProfileAttributes(
                    personality=PersonalityTraits(
                        traits=[
                            Trait(name="helpfulness", value=90),
                        ],
                    ),
                    expertise=[
                        Expertise(domain="testing", level=80),
                    ],
                    communication=Communication(
                        style=CommunicationStyleEnum.DIRECT,
                    ),
                ),
            ),
        )


def test_profile_immutability():
    """Test that profile models are immutable."""
    profile = TanzoProfile(
        metadata=ProfileMetadata(
            version="0.1.0",
            id="test-profile",
            name="Test Profile",
        ),
        profile=Profile(
            archetype=ArchetypeEnum.GUIDE,
            attributes=ProfileAttributes(
                personality=PersonalityTraits(
                    traits=[
                        Trait(name="helpfulness", value=90),
                    ],
                ),
                expertise=[
                    Expertise(domain="testing", level=80),
                ],
                communication=Communication(
                    style=CommunicationStyleEnum.DIRECT,
                ),
            ),
        ),
    )
    
    # Attempting to modify should raise an error
    with pytest.raises(Exception):
        profile.metadata.name = "Modified Name"


def test_profile_model_dumping(tmp_path):
    """Test that profile models can be dumped to dict and JSON."""
    profile = TanzoProfile(
        metadata=ProfileMetadata(
            version="0.1.0",
            id="test-profile",
            name="Test Profile",
        ),
        profile=Profile(
            archetype=ArchetypeEnum.GUIDE,
            attributes=ProfileAttributes(
                personality=PersonalityTraits(
                    traits=[
                        Trait(name="helpfulness", value=90),
                    ],
                ),
                expertise=[
                    Expertise(domain="testing", level=80),
                ],
                communication=Communication(
                    style=CommunicationStyleEnum.DIRECT,
                ),
            ),
        ),
    )
    
    # Dump to dict
    profile_dict = profile.model_dump()
    assert isinstance(profile_dict, dict)
    assert profile_dict["metadata"]["name"] == "Test Profile"
    
    # Dump to JSON
    profile_json = profile.model_dump_json()
    assert isinstance(profile_json, str)
    assert "Test Profile" in profile_json
    
    # Save to file
    output_path = tmp_path / "test_profile.json"
    with open(output_path, "w") as f:
        f.write(profile_json)
    
    # Reload from file
    with open(output_path, "r") as f:
        loaded_dict = json.load(f)
    
    assert loaded_dict["metadata"]["name"] == "Test Profile"
