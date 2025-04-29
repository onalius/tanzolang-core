"""
Pydantic models for TanzoLang profiles
"""

from typing import Dict, List, Literal, Optional, Union, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


class DistributionType(str, Enum):
    """Types of probability distributions"""
    NORMAL = "normal"
    UNIFORM = "uniform"
    DISCRETE = "discrete"


class NormalDistribution(BaseModel):
    """Normal (Gaussian) probability distribution"""
    distribution: Literal["normal"]
    mean: float
    stdDev: float

    @validator("stdDev")
    def validate_std_dev(cls, v: float) -> float:
        """Ensure standard deviation is positive"""
        if v <= 0:
            raise ValueError("Standard deviation must be greater than 0")
        return v


class UniformDistribution(BaseModel):
    """Uniform probability distribution"""
    distribution: Literal["uniform"]
    min: float
    max: float

    @validator("max")
    def validate_max(cls, v: float, values: Dict[str, Any]) -> float:
        """Ensure max is greater than min"""
        if "min" in values and v <= values["min"]:
            raise ValueError("Max must be greater than min")
        return v


class DiscreteDistribution(BaseModel):
    """Discrete probability distribution with weighted values"""
    distribution: Literal["discrete"]
    values: List[Union[str, float, bool]]
    weights: List[float]

    @validator("weights")
    def validate_weights(cls, v: List[float], values: Dict[str, Any]) -> List[float]:
        """Ensure weights are valid probabilities and match the number of values"""
        if any(weight < 0 or weight > 1 for weight in v):
            raise ValueError("All weights must be between 0 and 1")
        
        if "values" in values and len(v) != len(values["values"]):
            raise ValueError("Number of weights must match number of values")
        
        return v


ProbabilityDistribution = Union[NormalDistribution, UniformDistribution, DiscreteDistribution]
AttributeValue = Union[str, float, bool, ProbabilityDistribution]


class Attribute(BaseModel):
    """An attribute in a TanzoLang profile"""
    name: str
    value: AttributeValue
    description: Optional[str] = None
    unit: Optional[str] = None


class ArchetypeType(str, Enum):
    """Types of archetypes"""
    DIGITAL = "digital"
    PHYSICAL = "physical"
    HYBRID = "hybrid"


class Archetype(BaseModel):
    """An archetype in a TanzoLang profile"""
    type: ArchetypeType
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: List[Attribute]


class Profile(BaseModel):
    """The main profile section in a TanzoLang profile"""
    name: str
    description: Optional[str] = None
    archetypes: List[Archetype]


class TanzoProfile(BaseModel):
    """A complete TanzoLang profile"""
    version: str = Field("0.1.0", description="The TanzoLang version")
    profile: Profile
