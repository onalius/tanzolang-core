# TanzoLang Schema Reference

This document provides a comprehensive reference for the TanzoLang JSON Schema specification.

## Overview

TanzoLang uses JSON Schema Draft-07 to define the structure and validation rules for Tanzo profiles. The schema defines the following main components:

- Profile metadata (version, type)
- Digital archetype definitions
- Simulation parameters
- Additional metadata

## Schema Location

The canonical schema is available at:

- JSON: `/spec/tanzo-schema.json`
- YAML: `/spec/tanzo-schema.yaml`

## Top-Level Structure

A Tanzo profile document is a JSON or YAML object with the following top-level properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `version` | String | Yes | TanzoLang schema version (e.g., "0.1.0") |
| `profile_type` | String | Yes | Profile type: "full", "archetype_only", or "simulation" |
| `archetype` | Object | Yes | Digital archetype definition |
| `simulation_parameters` | Object | No | Parameters for simulation runs |
| `metadata` | Object | No | Additional metadata about the profile |

## Profile Types

TanzoLang supports three profile types:

- **full**: Complete profile with archetype and simulation parameters
- **archetype_only**: Profile containing only archetype definition without simulation
- **simulation**: Profile focused on simulation parameters for an existing archetype

## Archetype Definition

The `archetype` object defines a digital entity with the following properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | String | Yes | Name of the digital archetype |
| `description` | String | No | Description of the archetype |
| `core_traits` | Object | Yes | Map of trait names to trait scores |
| `skills` | Array | Yes | List of skills possessed by the archetype |
| `interests` | Array | No | List of interest strings |
| `values` | Array | No | List of value strings |

### Core Traits

The `core_traits` object must contain at least the following required traits:

- `intelligence`
- `creativity`
- `sociability`

Additional traits can be defined as needed. Each trait is defined with a `TraitScore` object.

### Trait Score

Trait and skill scores are defined with objects containing:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `base` | Number | Yes | Base score (0-10) |
| `range` | Array | No | Range of possible values [min, max] |
| `distribution` | String | No | Statistical distribution: "normal", "uniform", or "exponential" |

### Skills

The `skills` array must contain at least one skill. Each skill has:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | String | Yes | Name of the skill |
| `proficiency` | Object | Yes | Skill proficiency as a TraitScore |
| `category` | String | No | Skill category |
| `experience_years` | Number | No | Years of experience with this skill |

## Simulation Parameters

The optional `simulation_parameters` object contains:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `variation_factor` | Number | No | Factor for variation (0-1) |
| `seed` | Integer | No | Random seed for reproducible simulations |
| `iterations` | Integer | No | Default number of simulation iterations |
| `environments` | Array | No | List of simulation environment names |

## Metadata

The optional `metadata` object contains:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `author` | String | No | Profile author |
| `created_at` | String | No | Creation timestamp (ISO format) |
| `tags` | Array | No | List of tag strings |

## Examples

See the `/examples` directory for complete examples:

- `Kai_profile.yaml`: A full profile with simulation parameters
- `digital_archetype_only.yaml`: A minimal archetype-only profile

## JSON Schema Reference

For the complete JSON Schema definition, see `/spec/tanzo-schema.json`.
