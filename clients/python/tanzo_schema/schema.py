"""
Pydantic models for TanzoLang schema.

This module defines the Pydantic models that correspond to the TanzoLang JSON Schema.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

class Skill(BaseModel):
    """Represents a skill in a TanzoLang profile."""
    
    name: str = Field(..., description="Name of the skill")
    proficiency: float = Field(
        ...,
        description="Proficiency level (0-1)",
        ge=0.0,
        le=1.0,
    )
    description: Optional[str] = Field(None, description="Description of the skill")
    domain: Optional[str] = Field(None, description="Domain of the skill")

class Behavior(BaseModel):
    """Represents a behavior in a TanzoLang profile."""
    
    name: str = Field(..., description="Name of the behavior")
    probability: float = Field(
        ...,
        description="Probability of exhibiting the behavior (0-1)",
        ge=0.0,
        le=1.0,
    )
    description: Optional[str] = Field(None, description="Description of the behavior")
    triggers: Optional[List[str]] = Field(None, description="Triggers for the behavior")

class Knowledge(BaseModel):
    """Represents a knowledge domain in a TanzoLang profile."""
    
    domain: str = Field(..., description="Domain of knowledge")
    depth: float = Field(
        ...,
        description="Depth of knowledge (0-1)",
        ge=0.0,
        le=1.0,
    )
    sources: Optional[List[str]] = Field(None, description="Sources of knowledge")

class Protocol(BaseModel):
    """Represents an interaction protocol in a TanzoLang profile."""
    
    name: str = Field(..., description="Name of the protocol")
    rules: List[str] = Field(..., description="Rules of the protocol")
    priority: Optional[float] = Field(None, description="Priority level of the protocol")

class Core(BaseModel):
    """Represents the core attributes of an archetype."""
    
    name: str = Field(..., description="Name of the archetype")
    purpose: str = Field(..., description="Purpose of the archetype")
    persona: Optional[str] = Field(None, description="Persona description for the archetype")

class Context(BaseModel):
    """Represents the context attributes of an archetype."""
    
    domain: Optional[str] = Field(None, description="Domain of expertise")
    background: Optional[str] = Field(None, description="Background information")
    constraints: Optional[List[str]] = Field(None, description="Constraints for this archetype")

class Capabilities(BaseModel):
    """Represents the capabilities of an archetype."""
    
    skills: List[Skill] = Field(..., description="Skills of the archetype")
    behaviors: Optional[List[Behavior]] = Field(None, description="Behaviors of the archetype")
    knowledge: Optional[List[Knowledge]] = Field(None, description="Knowledge of the archetype")

class Interaction(BaseModel):
    """Represents the interaction characteristics of an archetype."""
    
    communication_style: Optional[str] = Field(None, description="Communication style for interactions")
    preferences: Optional[List[str]] = Field(None, description="Interaction preferences")
    protocols: Optional[List[Protocol]] = Field(None, description="Interaction protocols")

class Attributes(BaseModel):
    """Represents the attributes of an archetype."""
    
    core: Core = Field(..., description="Core attributes of the archetype")
    context: Context = Field(..., description="Context attributes of the archetype")
    capabilities: Capabilities = Field(..., description="Capabilities of the archetype")

class Archetype(BaseModel):
    """Represents an archetype in a TanzoLang profile."""
    
    type: Literal["digital", "analog", "hybrid"] = Field(..., description="Type of the archetype")
    weight: float = Field(
        ...,
        description="Weight of the archetype in the overall profile (0-1)",
        ge=0.0,
        le=1.0,
    )
    attributes: Attributes = Field(..., description="Attributes of the archetype")
    interaction: Optional[Interaction] = Field(None, description="Interaction characteristics of the archetype")

    @field_validator('weight')
    @classmethod
    def validate_weight(cls, v: float) -> float:
        """Validate that the weight is between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError("Weight must be between 0 and 1")
        return v

class Identity(BaseModel):
    """Represents the identity of a TanzoLang profile."""
    
    name: str = Field(..., description="Name of the profile")
    version: str = Field(..., description="Version of the profile")
    description: Optional[str] = Field(None, description="Description of the profile")
    author: Optional[str] = Field(None, description="Author of the profile")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the profile")

    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate that the version follows semantic versioning."""
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError("Version must follow semantic versioning (e.g., 1.0.0)")
        return v

class Metadata(BaseModel):
    """Represents the metadata of a TanzoLang profile."""
    
    created_at: Optional[datetime] = Field(None, description="When the profile was created")
    updated_at: Optional[datetime] = Field(None, description="When the profile was last updated")
    custom: Optional[Dict[str, Any]] = Field(None, description="Custom metadata fields")

class ProfileContent(BaseModel):
    """Represents the content of a TanzoLang profile."""
    
    identity: Identity = Field(..., description="Identity of the profile")
    archetypes: List[Archetype] = Field(..., description="List of archetypes in the profile")
    metadata: Optional[Metadata] = Field(None, description="Metadata of the profile")

    @field_validator('archetypes')
    @classmethod
    def validate_archetypes(cls, v: List[Archetype]) -> List[Archetype]:
        """Validate that there is at least one archetype."""
        if not v:
            raise ValueError("There must be at least one archetype")
        
        # Check that the sum of weights is approximately 1.0 (allowing for floating point imprecision)
        total_weight = sum(archetype.weight for archetype in v)
        if not 0.99 <= total_weight <= 1.01:
            raise ValueError(f"The sum of archetype weights should be 1.0, got {total_weight}")
        
        return v

class TanzoProfile(BaseModel):
    """Represents a complete TanzoLang profile."""
    
    profile: ProfileContent = Field(..., description="Content of the TanzoLang profile")
