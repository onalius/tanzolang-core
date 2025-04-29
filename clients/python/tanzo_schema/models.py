"""
Pydantic models for Tanzo Schema.

This module contains Pydantic models that represent the structure and validation
rules of the TanzoLang schema.
"""

import enum
from datetime import datetime
from typing import Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, Field, conlist, field_validator


class DistributionType(str, enum.Enum):
    """Statistical distribution types for simulations."""

    NORMAL = "normal"
    UNIFORM = "uniform"
    EXPONENTIAL = "exponential"


class ProfileType(str, enum.Enum):
    """Types of Tanzo profiles."""

    FULL = "full"
    ARCHETYPE_ONLY = "archetype_only"
    SIMULATION = "simulation"


class TraitScore(BaseModel):
    """Model for trait and skill scores with optional simulation parameters."""

    base: float = Field(..., description="Base score for the trait", ge=0, le=10)
    range: Optional[Tuple[float, float]] = Field(
        None, description="Range of possible values [min, max]"
    )
    distribution: Optional[DistributionType] = Field(
        None, description="Statistical distribution for simulation"
    )

    @field_validator("range")
    @classmethod
    def validate_range(cls, v):
        """Validate that the range values are within 0-10 and min <= max."""
        if v is None:
            return v
        
        min_val, max_val = v
        if not (0 <= min_val <= 10 and 0 <= max_val <= 10):
            raise ValueError("Range values must be between 0 and 10")
        if min_val > max_val:
            raise ValueError("Minimum value must be less than or equal to maximum value")
        return v


class Skill(BaseModel):
    """Model for skills in a Tanzo profile."""

    name: str = Field(..., description="Name of the skill")
    proficiency: TraitScore = Field(..., description="Proficiency level for this skill")
    category: Optional[str] = Field(None, description="Skill category")
    experience_years: Optional[float] = Field(
        None, description="Years of experience with this skill", ge=0
    )


class Archetype(BaseModel):
    """Model for a digital archetype in a Tanzo profile."""

    name: str = Field(..., description="Name of the digital archetype")
    description: Optional[str] = Field(None, description="Description of the digital archetype")
    core_traits: Dict[str, TraitScore] = Field(
        ..., description="Core personality traits of the archetype"
    )
    skills: List[Skill] = Field(..., description="Skills possessed by the archetype", min_length=1)
    interests: Optional[List[str]] = Field(None, description="Interests of the archetype")
    values: Optional[List[str]] = Field(None, description="Core values of the archetype")

    @field_validator("core_traits")
    @classmethod
    def validate_core_traits(cls, v):
        """Validate that required core traits are present."""
        required_traits = {"intelligence", "creativity", "sociability"}
        missing_traits = required_traits - set(v.keys())
        if missing_traits:
            raise ValueError(f"Missing required core traits: {', '.join(missing_traits)}")
        return v


class SimulationParameters(BaseModel):
    """Model for simulation parameters in a Tanzo profile."""

    variation_factor: Optional[float] = Field(
        None, description="Factor for variation in simulations", ge=0, le=1
    )
    seed: Optional[int] = Field(None, description="Random seed for reproducible simulations")
    iterations: Optional[int] = Field(
        100, description="Number of simulation iterations", ge=1
    )
    environments: Optional[List[str]] = Field(None, description="Simulation environments")


class Metadata(BaseModel):
    """Model for metadata in a Tanzo profile."""

    author: Optional[str] = None
    created_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TanzoProfile(BaseModel):
    """Top-level model for a complete Tanzo profile."""

    version: str = Field(..., description="The TanzoLang schema version", pattern=r"^\d+\.\d+\.\d+$")
    profile_type: ProfileType = Field(..., description="Type of Tanzo profile")
    archetype: Archetype = Field(..., description="Digital archetype definition")
    simulation_parameters: Optional[SimulationParameters] = Field(
        None, description="Parameters for simulation runs"
    )
    metadata: Optional[Metadata] = Field(None, description="Additional metadata")
