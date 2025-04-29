"""
Tests for the TanzoLang schema validation.
"""

import json
import os
import pathlib
import pytest
import yaml

from clients.python.tanzo_schema import (
    TanzoProfile,
    Archetype,
    TraitScore,
    Skill,
    SimulationParameters,
    Metadata,
    validate_profile,
    SchemaValidationError,
)


# Test fixtures
@pytest.fixture
def valid_profile_dict():
    """Return a dictionary representing a valid Tanzo profile."""
    return {
        "version": "0.1.0",
        "profile_type": "full",
        "archetype": {
            "name": "Test Archetype",
            "description": "Test description",
            "core_traits": {
                "intelligence": {"base": 8.0},
                "creativity": {"base": 7.5},
                "sociability": {"base": 6.0}
            },
            "skills": [
                {
                    "name": "Problem Solving",
                    "proficiency": {"base": 8.5},
                    "category": "Cognitive"
                }
            ],
            "interests": ["Testing", "Validation"],
            "values": ["Accuracy", "Reliability"]
        },
        "simulation_parameters": {
            "variation_factor": 0.2,
            "seed": 12345,
            "iterations": 100
        },
        "metadata": {
            "author": "Test Author",
            "created_at": "2023-06-01T10:00:00Z",
            "tags": ["test", "validation"]
        }
    }


@pytest.fixture
def valid_profile_path(valid_profile_dict, tmp_path):
    """Save a valid profile to a temporary YAML file and return the path."""
    file_path = tmp_path / "valid_profile.yaml"
    with open(file_path, "w") as f:
        yaml.dump(valid_profile_dict, f)
    return str(file_path)


@pytest.fixture
def invalid_profile_dict():
    """Return a dictionary representing an invalid Tanzo profile."""
    return {
        "version": "0.1.0",
        "profile_type": "full",
        "archetype": {
            "name": "Invalid Archetype",
            # Missing required core_traits
            "skills": []  # Empty skills array (should have at least 1)
        }
    }


@pytest.fixture
def invalid_profile_path(invalid_profile_dict, tmp_path):
    """Save an invalid profile to a temporary YAML file and return the path."""
    file_path = tmp_path / "invalid_profile.yaml"
    with open(file_path, "w") as f:
        yaml.dump(invalid_profile_dict, f)
    return str(file_path)


# Example profiles
def test_example_profiles_exist():
    """Test that example profiles exist and are valid YAML files."""
    examples_dir = pathlib.Path(__file__).parent.parent / "examples"
    assert examples_dir.exists(), "Examples directory doesn't exist"
    
    kai_profile = examples_dir / "Kai_profile.yaml"
    archetype_only = examples_dir / "digital_archetype_only.yaml"
    
    assert kai_profile.exists(), "Kai_profile.yaml doesn't exist"
    assert archetype_only.exists(), "digital_archetype_only.yaml doesn't exist"
    
    # Try to load them as YAML
    with open(kai_profile, "r") as f:
        kai_data = yaml.safe_load(f)
    
    with open(archetype_only, "r") as f:
        archetype_data = yaml.safe_load(f)
    
    assert kai_data is not None, "Kai_profile.yaml couldn't be parsed as YAML"
    assert archetype_data is not None, "digital_archetype_only.yaml couldn't be parsed as YAML"


def test_validate_example_profiles():
    """Test that example profiles validate against the schema."""
    examples_dir = pathlib.Path(__file__).parent.parent / "examples"
    kai_profile = examples_dir / "Kai_profile.yaml"
    archetype_only = examples_dir / "digital_archetype_only.yaml"
    
    # Validate Kai profile
    kai_validated = validate_profile(kai_profile)
    assert kai_validated.profile_type.value == "full"
    assert kai_validated.archetype.name == "Kai"
    
    # Validate archetype-only profile
    archetype_validated = validate_profile(archetype_only)
    assert archetype_validated.profile_type.value == "archetype_only"
    assert archetype_validated.archetype.name == "Nova"


# Pydantic model tests
def test_trait_score_model():
    """Test the TraitScore model."""
    # Valid trait score
    trait = TraitScore(base=7.5, range=(6.5, 8.5), distribution="normal")
    assert trait.base == 7.5
    assert trait.range == (6.5, 8.5)
    assert trait.distribution.value == "normal"
    
    # Minimal trait score
    trait_minimal = TraitScore(base=5.0)
    assert trait_minimal.base == 5.0
    assert trait_minimal.range is None
    assert trait_minimal.distribution is None
    
    # Invalid trait score (base out of range)
    with pytest.raises(ValueError):
        TraitScore(base=11.0)
    
    # Invalid trait score (range minimum > maximum)
    with pytest.raises(ValueError):
        TraitScore(base=5.0, range=(6.0, 5.0))


def test_skill_model():
    """Test the Skill model."""
    # Valid skill
    skill = Skill(
        name="Test Skill",
        proficiency=TraitScore(base=8.0),
        category="Test Category",
        experience_years=3.5
    )
    assert skill.name == "Test Skill"
    assert skill.proficiency.base == 8.0
    assert skill.category == "Test Category"
    assert skill.experience_years == 3.5
    
    # Minimal skill
    skill_minimal = Skill(
        name="Minimal Skill",
        proficiency=TraitScore(base=5.0)
    )
    assert skill_minimal.name == "Minimal Skill"
    assert skill_minimal.proficiency.base == 5.0
    assert skill_minimal.category is None
    assert skill_minimal.experience_years is None


def test_archetype_model():
    """Test the Archetype model."""
    # Valid archetype
    archetype = Archetype(
        name="Test Archetype",
        description="Test description",
        core_traits={
            "intelligence": TraitScore(base=8.0),
            "creativity": TraitScore(base=7.5),
            "sociability": TraitScore(base=6.0)
        },
        skills=[
            Skill(name="Test Skill", proficiency=TraitScore(base=8.0))
        ],
        interests=["Test Interest"],
        values=["Test Value"]
    )
    assert archetype.name == "Test Archetype"
    assert archetype.description == "Test description"
    assert len(archetype.core_traits) == 3
    assert len(archetype.skills) == 1
    assert len(archetype.interests) == 1
    assert len(archetype.values) == 1
    
    # Missing required trait
    with pytest.raises(ValueError):
        Archetype(
            name="Invalid Archetype",
            core_traits={
                "intelligence": TraitScore(base=8.0),
                "creativity": TraitScore(base=7.5)
                # Missing sociability
            },
            skills=[
                Skill(name="Test Skill", proficiency=TraitScore(base=8.0))
            ]
        )
    
    # Empty skills list
    with pytest.raises(ValueError):
        Archetype(
            name="Invalid Archetype",
            core_traits={
                "intelligence": TraitScore(base=8.0),
                "creativity": TraitScore(base=7.5),
                "sociability": TraitScore(base=6.0)
            },
            skills=[]  # Empty list
        )


def test_tanzo_profile_model():
    """Test the TanzoProfile model."""
    # Valid profile
    profile = TanzoProfile(
        version="0.1.0",
        profile_type="full",
        archetype=Archetype(
            name="Test Archetype",
            core_traits={
                "intelligence": TraitScore(base=8.0),
                "creativity": TraitScore(base=7.5),
                "sociability": TraitScore(base=6.0)
            },
            skills=[
                Skill(name="Test Skill", proficiency=TraitScore(base=8.0))
            ]
        ),
        simulation_parameters=SimulationParameters(
            variation_factor=0.2,
            seed=12345,
            iterations=100
        ),
        metadata=Metadata(
            author="Test Author",
            created_at="2023-06-01T10:00:00Z",
            tags=["test", "validation"]
        )
    )
    assert profile.version == "0.1.0"
    assert profile.profile_type.value == "full"
    assert profile.archetype.name == "Test Archetype"
    assert profile.simulation_parameters.variation_factor == 0.2
    assert profile.metadata.author == "Test Author"
    
    # Invalid version format
    with pytest.raises(ValueError):
        TanzoProfile(
            version="invalid",
            profile_type="full",
            archetype=Archetype(
                name="Test Archetype",
                core_traits={
                    "intelligence": TraitScore(base=8.0),
                    "creativity": TraitScore(base=7.5),
                    "sociability": TraitScore(base=6.0)
                },
                skills=[
                    Skill(name="Test Skill", proficiency=TraitScore(base=8.0))
                ]
            )
        )


# Validation function tests
def test_validate_valid_dict(valid_profile_dict):
    """Test validating a valid profile dictionary."""
    profile = validate_profile(valid_profile_dict)
    assert isinstance(profile, TanzoProfile)
    assert profile.version == "0.1.0"
    assert profile.profile_type.value == "full"
    assert profile.archetype.name == "Test Archetype"


def test_validate_valid_file(valid_profile_path):
    """Test validating a valid profile file."""
    profile = validate_profile(valid_profile_path)
    assert isinstance(profile, TanzoProfile)
    assert profile.version == "0.1.0"
    assert profile.profile_type.value == "full"
    assert profile.archetype.name == "Test Archetype"


def test_validate_invalid_dict(invalid_profile_dict):
    """Test validating an invalid profile dictionary raises an error."""
    with pytest.raises(SchemaValidationError):
        validate_profile(invalid_profile_dict)


def test_validate_invalid_file(invalid_profile_path):
    """Test validating an invalid profile file raises an error."""
    with pytest.raises(SchemaValidationError):
        validate_profile(invalid_profile_path)


def test_validate_nonexistent_file():
    """Test validating a nonexistent file raises an error."""
    with pytest.raises(SchemaValidationError):
        validate_profile("/nonexistent/path/to/profile.yaml")


def test_validate_invalid_yaml_string():
    """Test validating an invalid YAML string raises an error."""
    with pytest.raises(SchemaValidationError):
        validate_profile("invalid: yaml: - content")
