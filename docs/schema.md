# TanzoLang Schema Documentation

This page documents the TanzoLang JSON-Schema specification in detail.

## Schema Overview

The TanzoLang schema defines a structure for describing digital archetypes and their attributes. It is based on the JSON-Schema standard and can be used to validate TanzoLang documents.

### Root Structure

A TanzoLang document consists of the following top-level fields:

```yaml
version: "0.1.0"
profile:
  name: "Profile Name"
  description: "Profile Description"
  archetypes:
    - # Archetype definitions...
