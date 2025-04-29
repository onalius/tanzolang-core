"""
Pydantic models for the TanzoLang schema.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class Trait(BaseModel):
    """Model representing a personality trait."""
    
    value: int = Field(..., ge=0, le=100, description="Trait value on scale of 0-100")
    variance: Optional[int] = Field(None, ge=0, le=50, description="Variance for simulation")
    description: Optional[str] = None


class Attribute(BaseModel):
    """Model representing a character attribute."""
    
    value: int = Field(..., ge=0, le=100, description="Attribute value on scale of 0-100")
    variance: Optional[int] = Field(None, ge=0, le=50, description="Variance for simulation")
    notes: Optional[str] = None


class Interest(BaseModel):
    """Model representing an interest."""
    
    name: str
    level: Optional[int] = Field(None, ge=1, le=10, description="Interest level from 1-10")


class KeyEvent(BaseModel):
    """Model representing a key event in a character's backstory."""
    
    age: Optional[int] = None
    description: str
    impact: Optional[str] = None


class CognitiveStyle(BaseModel):
    """Model for cognitive style attributes."""
    
    analytical: Optional[Attribute] = None
    creative: Optional[Attribute] = None
    practical: Optional[Attribute] = None


class CommunicationStyle(BaseModel):
    """Model for communication style attributes."""
    
    formal: Optional[Attribute] = None
    casual: Optional[Attribute] = None
    direct: Optional[Attribute] = None
    verbose: Optional[Attribute] = None


class SocialBehavior(BaseModel):
    """Model for social behavior attributes."""
    
    collaborative: Optional[Attribute] = None
    competitive: Optional[Attribute] = None
    supportive: Optional[Attribute] = None
    challenging: Optional[Attribute] = None


class ProblemSolvingBehavior(BaseModel):
    """Model for problem-solving behavior attributes."""
    
    systematic: Optional[Attribute] = None
    intuitive: Optional[Attribute] = None
    innovative: Optional[Attribute] = None
    cautious: Optional[Attribute] = None


class Behaviors(BaseModel):
    """Model for character behaviors."""
    
    social: Optional[SocialBehavior] = None
    problem_solving: Optional[ProblemSolvingBehavior] = None


class Backstory(BaseModel):
    """Model for character backstory information."""
    
    background: Optional[str] = None
    key_events: Optional[List[KeyEvent]] = None


class Attributes(BaseModel):
    """Model for character attributes."""
    
    cognitive_style: Optional[CognitiveStyle] = None
    communication_style: Optional[CommunicationStyle] = None
    interests: Optional[List[Interest]] = None
    values: Optional[List[str]] = None


class Traits(BaseModel):
    """Model for the Big Five personality traits."""
    
    openness: Trait
    conscientiousness: Trait
    extraversion: Trait
    agreeableness: Trait
    neuroticism: Trait


class DigitalArchetype(BaseModel):
    """Model for the digital archetype definition."""
    
    traits: Traits
    attributes: Attributes
    behaviors: Optional[Behaviors] = None
    backstory: Optional[Backstory] = None


class SimulationParameters(BaseModel):
    """Model for Monte-Carlo simulation parameters."""
    
    variance: Optional[float] = Field(None, ge=0, le=1, description="Variance factor")
    contexts: Optional[List[str]] = None


class Metadata(BaseModel):
    """Model for profile metadata."""
    
    version: str
    name: str
    description: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator('version')
    def validate_version(cls, v: str) -> str:
        """Validate the version format."""
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError('Version must be in the format X.Y.Z')
        return v


class TanzoProfile(BaseModel):
    """Root model for a complete TanzoLang profile."""
    
    metadata: Metadata
    digital_archetype: DigitalArchetype
    simulation_parameters: Optional[SimulationParameters] = None
