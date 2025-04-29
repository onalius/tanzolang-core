# TanzoLang Schema

TanzoLang provides a standardized format for defining digital archetypes using a JSON Schema specification. This document outlines the core components of the schema and how to use them.

## Schema Overview

The TanzoLang schema consists of three main sections:

1. **Metadata**: Information about the profile itself
2. **Digital Archetype**: The core definition of the character's traits and attributes
3. **Simulation Parameters**: Optional settings for Monte-Carlo simulations

### Metadata

The metadata section contains information about the profile:

```json
"metadata": {
  "version": "0.1.0",
  "name": "Character Name",
  "description": "Optional description",
  "author": "Optional author information",
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-15T14:30:00Z"
}
