"""
TanzoLang Python SDK - Schema validation and utilities for TanzoLang profiles.

This package provides tools for working with TanzoLang profiles including:
- Pydantic models for type-safe access to profile data
- Validation against the official TanzoLang JSON Schema
- Simulation utilities for Monte Carlo trials
- Export functionality for serialization
"""

__version__ = "0.1.0"

from tanzo_schema.models import (
    Archetype, 
    Profile, 
    Trait, 
    TanzoDocument
)
from tanzo_schema.validator import validate_document
from tanzo_schema.simulator import run_simulation
from tanzo_schema.exporter import export_shorthand

__all__ = [
    "Archetype", 
    "Profile", 
    "Trait", 
    "TanzoDocument",
    "validate_document",
    "run_simulation",
    "export_shorthand",
]
