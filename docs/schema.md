# TanzoLang Schema

This page documents the TanzoLang schema specification.

## Overview

The TanzoLang schema defines a format for describing profiles with archetypes and traits. The schema is defined using JSON Schema and is available in both JSON and YAML formats.

## Schema Structure

A TanzoLang document consists of:

- `version`: The version of the schema being used, following semantic versioning.
- `profile`: The main profile object.

### Profile

A profile represents a complete set of archetypes and traits that define a personality or identity within the Tomodaichi Tanzo ecosystem.

Properties:

- `name` (required): The name of the profile.
- `description` (optional): A description of the profile.
- `archetypes` (required): An array of archetype objects that define the profile.
- `metadata` (optional): Additional metadata for the profile.

### Archetype

An archetype represents a specific aspect or dimension of a profile.

Properties:

- `type` (required): The type of the archetype. Must be one of:
  - `digital`
  - `physical`
  - `social`
  - `emotional`
  - `cognitive`
- `weight` (required): The weight of this archetype in the profile, from 0.0 to 1.0.
- `traits` (optional): An array of trait objects associated with this archetype.
- `attributes` (optional): Additional attributes specific to this archetype.

### Trait

A trait represents a specific characteristic within an archetype.

Properties:

- `name` (required): The name of the trait.
- `value` (required): The value of the trait, from 0.0 to 1.0.
- `variance` (optional, default: 0.1): The variance of the trait for simulation, from 0.0 to 1.0.
- `description` (optional): A description of the trait.

## Example

Here's a minimal example of a TanzoLang document:

```yaml
version: "0.1.0"
profile:
  name: "Example Profile"
  description: "A simple example profile"
  archetypes:
    - type: "digital"
      weight: 0.8
      traits:
        - name: "tech_savvy"
          value: 0.9
          variance: 0.05
          description: "Comfortable with latest technology"
