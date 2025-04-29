"""
Tanzo Schema Python SDK package.

This package provides Pydantic models and validation utilities for working
with TanzoLang schema in Python applications.
"""

__version__ = "0.1.0"

from .models import (
    TraitScore,
    Skill,
    Archetype,
    SimulationParameters,
    Metadata,
    TanzoProfile,
)
from .validation import validate_profile, SchemaValidationError

__all__ = [
    "TraitScore",
    "Skill",
    "Archetype",
    "SimulationParameters",
    "Metadata",
    "TanzoProfile",
    "validate_profile",
    "SchemaValidationError",
]
