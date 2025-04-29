# TanzoLang Client SDKs

TanzoLang provides client SDKs for multiple programming languages to help you work with TanzoLang documents programmatically.

## Available SDKs

Currently, the following SDKs are available:

- [Python SDK](clients/python.md) - Based on Pydantic v2
- [TypeScript SDK](clients/typescript.md) - Based on Zod

## Common Functionality

All SDKs provide similar core functionality:

1. **Schema Models** - Type-safe representations of TanzoLang schema components
2. **Validation** - Methods to validate TanzoLang documents against the schema
3. **Loading** - Utilities to load TanzoLang documents from files
4. **Simulation** - Methods to run Monte Carlo simulations on document distributions
5. **Export** - Functions to convert documents to a shorthand string representation

## Example Usage

### Python SDK

```python
from tanzo_schema import load_tanzo_file, validate_tanzo_document

# Load a document
document = load_tanzo_file("profile.yaml")

# Validate
is_valid, errors = validate_tanzo_document(document)
if is_valid:
    print("Document is valid!")
else:
    print("Validation errors:", errors)

# Access data
print(f"Profile: {document.profile.name}")
for archetype in document.profile.archetypes:
    print(f"- Archetype: {archetype.name} ({archetype.type})")
