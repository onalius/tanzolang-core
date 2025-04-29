"""Tests for tanzo_schema utility functions."""

import uuid
from datetime import datetime
from pathlib import Path

import pytest

from tanzo_schema import (
    TanzoProfile,
    DigitalArchetype,
    PersonalityTraits,
    Identity,
    export_profile,
    simulate_profile,
)


def test_export_profile():
    """Test exporting a profile to shorthand."""
    profile = TanzoProfile(
        profile_version="0.1.0",
        profile_id=uuid.uuid4(),
        profile_name="Test Profile",
        creation_date=datetime.now(),
        digital_archetype=DigitalArchetype(
            personality_traits=PersonalityTraits(
                openness=0.7,
                conscientiousness=0.6,
                extraversion=0.5,
                agreeableness=0.8,
                neuroticism=0.3,
            ),
            identity=Identity(
                name="TestBot",
                background="This is a test profile",
            ),
        ),
    )
    
    shorthand = export_profile(profile)
    assert shorthand == "TestBot(O7C6E5A8N3)"


def test_export_profile_from_file():
    """Test exporting a profile from file."""
    profile_path = Path(__file__).parent.parent / "examples" / "Kai_profile.yaml"
    shorthand = export_profile(profile_path)
    assert shorthand == "Kai(O8C9E6A9N2)"


def test_simulate_profile():
    """Test simulating a profile."""
    profile = TanzoProfile(
        profile_version="0.1.0",
        profile_id=uuid.uuid4(),
        profile_name="Test Profile",
        creation_date=datetime.now(),
        digital_archetype=DigitalArchetype(
            personality_traits=PersonalityTraits(
                openness=0.7,
                conscientiousness=0.6,
                extraversion=0.5,
                agreeableness=0.8,
                neuroticism=0.3,
            ),
            identity=Identity(
                name="TestBot",
                background="This is a test profile",
            ),
        ),
    )
    
    # Run a deterministic simulation (no variance)
    results = simulate_profile(profile, iterations=10, variance=0.0)
    
    # Check structure and values
    assert results["iterations"] == 10
    assert results["profile_name"] == "Test Profile"
    assert results["openness"]["mean"] == 0.7
    assert results["conscientiousness"]["mean"] == 0.6
    assert results["extraversion"]["mean"] == 0.5
    assert results["agreeableness"]["mean"] == 0.8
    assert results["neuroticism"]["mean"] == 0.3


def test_simulate_profile_with_variance():
    """Test simulating a profile with variance."""
    profile = TanzoProfile(
        profile_version="0.1.0",
        profile_id=uuid.uuid4(),
        profile_name="Test Profile",
        creation_date=datetime.now(),
        digital_archetype=DigitalArchetype(
            personality_traits=PersonalityTraits(
                openness=0.5,
                conscientiousness=0.5,
                extraversion=0.5,
                agreeableness=0.5,
                neuroticism=0.5,
            ),
            identity=Identity(
                name="TestBot",
                background="This is a test profile",
            ),
        ),
    )
    
    # Run simulation with high variance
    results = simulate_profile(profile, iterations=100, variance=0.5)
    
    # Check that values have variance
    for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
        assert results[trait]["min"] < results[trait]["mean"] < results[trait]["max"]
        assert results[trait]["std_dev"] > 0
