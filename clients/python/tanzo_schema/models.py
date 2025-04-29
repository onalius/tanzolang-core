"""
Pydantic models for the TanzoLang schema.

These models represent the various components of a TanzoLang profile and
provide type-safe access to profile data with validation.
"""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator

ArchetypeType = Literal["digital", "physical", "social", "emotional", "cognitive"]


class Trait(BaseModel):
    """A trait associated with an archetype."""
    
    name: str = Field(..., description="The name of the trait")
    value: float = Field(
        ..., 
        description="The value of the trait (0.0-1.0)", 
        ge=0.0, 
        le=1.0
    )
    variance: float = Field(
        default=0.1, 
        description="The variance of the trait for simulation (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    description: Optional[str] = Field(None, description="A description of the trait")
    
    @field_validator('value', 'variance')
    @classmethod
    def check_range(cls, v: float) -> float:
        """Validate that values are within range 0.0-1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Value must be between 0.0 and 1.0, got {v}")
        return v


class Archetype(BaseModel):
    """An archetype in a TanzoLang profile."""
    
    type: ArchetypeType = Field(..., description="The type of the archetype")
    weight: float = Field(
        ..., 
        description="The weight of this archetype in the profile (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    traits: Optional[List[Trait]] = Field(
        default=None, 
        description="Traits associated with this archetype"
    )
    attributes: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Specific attributes for this archetype"
    )
    
    @field_validator('weight')
    @classmethod
    def check_weight(cls, v: float) -> float:
        """Validate that weight is within range 0.0-1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {v}")
        return v


class Profile(BaseModel):
    """A TanzoLang profile."""
    
    name: str = Field(..., description="The name of the profile")
    description: Optional[str] = Field(None, description="A description of the profile")
    archetypes: List[Archetype] = Field(
        ..., 
        description="The archetypes defining this profile",
        min_length=1
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional metadata for the profile"
    )
    
    model_config = ConfigDict(extra='allow')


class TanzoDocument(BaseModel):
    """The root document for a TanzoLang profile."""
    
    version: str = Field(
        default="0.1.0", 
        description="The version of the TanzoLang schema",
        pattern=r"^\d+\.\d+\.\d+$"
    )
    profile: Profile = Field(..., description="The profile data")
    
    model_config = ConfigDict(extra='allow')
