"""
Pydantic models representing the TanzoLang schema.
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ArchetypeType(str, Enum):
    ADVISOR = "advisor"
    COMPANION = "companion"
    CREATOR = "creator"
    EDUCATOR = "educator"
    ENTERTAINER = "entertainer"
    EXPERT = "expert"
    GUIDE = "guide"


class BehaviorContext(str, Enum):
    ALWAYS = "always"
    SITUATIONAL = "situational"
    TRIGGERED = "triggered"


class CommunicationStyle(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    TECHNICAL = "technical"
    FRIENDLY = "friendly"
    DIRECT = "direct"
    NURTURING = "nurturing"
    PLAYFUL = "playful"


class CommunicationTone(str, Enum):
    PROFESSIONAL = "professional"
    WARM = "warm"
    ENTHUSIASTIC = "enthusiastic"
    NEUTRAL = "neutral"
    ACADEMIC = "academic"
    HUMOROUS = "humorous"


class ResponseStructure(str, Enum):
    BULLET_POINTS = "bullet-points"
    PARAGRAPHS = "paragraphs"
    STEP_BY_STEP = "step-by-step"
    NARRATIVE = "narrative"
    FLEXIBLE = "flexible"


class FormatPreference(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    CODE = "code"
    MIXED = "mixed"


class Archetype(BaseModel):
    """Defines the primary and optional secondary archetype for a profile."""
    primary: ArchetypeType
    secondary: Optional[ArchetypeType] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid"
    )

    @field_validator('secondary')
    @classmethod
    def secondary_must_differ_from_primary(cls, v, values):
        if v is not None and v == values.data.get('primary'):
            raise ValueError("Secondary archetype must differ from primary")
        return v


class Behavior(BaseModel):
    """Defines a behavior trait with name, description, and strength."""
    name: str
    description: str
    strength: float = Field(ge=0.0, le=1.0)
    context: Optional[BehaviorContext] = BehaviorContext.ALWAYS
    trigger: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid"
    )

    @field_validator('trigger')
    @classmethod
    def validate_trigger(cls, v, values):
        if values.data.get('context') == BehaviorContext.TRIGGERED and not v:
            raise ValueError("Trigger must be provided for triggered behaviors")
        return v


class PersonalityTraits(BaseModel):
    """OCEAN personality model traits."""
    openness: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    conscientiousness: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    extraversion: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    agreeableness: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    neuroticism: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)


class Personality(BaseModel):
    """Defines personality characteristics."""
    traits: Optional[PersonalityTraits] = None
    values: Optional[List[str]] = None
    character: Optional[str] = None


class Communication(BaseModel):
    """Defines communication preferences."""
    style: Optional[CommunicationStyle] = None
    tone: Optional[CommunicationTone] = None
    complexity: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    verbosity: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)


class KnowledgeDomain(BaseModel):
    """Defines a specific knowledge domain with proficiency level."""
    name: str
    proficiency: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    description: Optional[str] = None


class Knowledge(BaseModel):
    """Defines knowledge domains and limitations."""
    domains: Optional[List[KnowledgeDomain]] = None
    limitations: Optional[List[str]] = None


class InteractionPreferences(BaseModel):
    """Defines interaction preferences."""
    proactivity: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
    detail: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)


class ResponsePreferences(BaseModel):
    """Defines response format preferences."""
    structure: Optional[ResponseStructure] = None
    formatPreference: Optional[FormatPreference] = None


class Preferences(BaseModel):
    """Defines general preferences."""
    interaction: Optional[InteractionPreferences] = None
    response: Optional[ResponsePreferences] = None


class SimulationParameters(BaseModel):
    """Parameters for profile simulation."""
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)
    randomness: Optional[float] = Field(default=0.3, ge=0.0, le=1.0)
    creativity: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)


class Simulation(BaseModel):
    """Defines simulation parameters and constraints."""
    parameters: Optional[SimulationParameters] = None
    constraints: Optional[List[str]] = None


class ProfileData(BaseModel):
    """Core profile data model."""
    name: str
    description: Optional[str] = None
    archetype: Archetype
    behaviors: Optional[List[Behavior]] = None
    personality: Optional[Personality] = None
    communication: Optional[Communication] = None
    knowledge: Optional[Knowledge] = None
    preferences: Optional[Preferences] = None
    simulation: Optional[Simulation] = None
    metadata: Optional[Dict[str, Any]] = None


class TanzoProfile(BaseModel):
    """Complete TanzoLang profile."""
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    profile: ProfileData

    model_config = ConfigDict(
        extra="forbid"
    )
