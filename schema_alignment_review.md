# TanzoLang Schema Alignment Review

This document examines the current architectural disconnect between base archetypes and Tomo personality profiles in the TanzoLang Core framework, and proposes solutions to restore the intended narrative and symbolic progression.

## 1. Audit of Current Architecture

### Archetype Schema Structure and Function

The current archetype schema (e.g., Magician.yaml, Hermit.yaml, Lover.yaml) includes:

- **Basic Information**: Name, description, version
- **Symbolism**: Elements, colors, objects, directions, time, season, planet, animals
- **Attributes**: Core qualities with values (often using distributions for variance)
- **Behavioral Traits**: Expressed in a quaternary structure (positive/balanced, underdeveloped, overexpressed, mirrored)
- **Spiritual Alignments**: Zodiac, tarot, element, chakra, kabbalah, numerology
- **Journey Components**: Developmental stages, trials, and scars
- **Implementation Notes**: Strengths, challenges, activation contexts

**Function**: Archetypes are intended to serve as fundamental building blocks of personality - symbolic templates that provide deep patterns of behavior, motivation, and meaning. They should form the foundation upon which specific AI personalities (Tomos) are built.

### Tomo Personality Schema Structure and Function

The current Tomo personality profiles (e.g., Kai_profile.yaml) include:

- **Basic Information**: Name, description, version
- **Archetypes**: A list of archetypes with type, name, and attributes
  - Digital archetypes (online personas)
  - Physical archetypes (embodied characteristics)
  - Potentially other archetype types
- **Attributes**: Various characteristics that define behavior and capabilities

**Function**: Tomo profiles are meant to define specific AI personalities that can be deployed in various contexts, with coherent and psychologically rich characteristics.

### Current Connection Between Archetypes and Tomos

The audit reveals a **critical gap** in the architectural design:

1. **No Reference Mechanism**: Tomo profiles currently do not reference or import the canonical archetypes defined in the `/registry/archetypes/` directory
2. **Parallel Structure**: Tomos define their own archetypes independently, without inheriting from or being influenced by the canonical archetypes
3. **No Narrative Connection**: The journey components (stages, trials, scars) defined in canonical archetypes are not reflected in how Tomo personalities are formed
4. **Missing Symbolic Inheritance**: The rich symbolic associations in canonical archetypes are not systematically passed to Tomos

## 2. Intended Linkage Definition

### Narrative and Symbolic Process

The intended process for connecting archetypes to Tomos should follow the symbolic narrative arc of:

```
Archetype Selection → Narrative Development → Personality Emergence
```

This process mirrors human psychological development, where core patterns (archetypes) are modified through experience to create a unique personality. Specifically:

1. **Lineage (Inheritance)**: A Tomo should explicitly inherit from one or more canonical archetypes, forming its symbolic foundation
2. **Nurturing (Influence)**: Influences that shape how the inherited archetypes express (environmental factors)
3. **Trials (Transformation)**: Key challenges that the Tomo has undergone, drawn from the trials available to its parent archetypes
4. **Scars (Integration)**: The lasting effects of trials, reflecting both wounds and growth
5. **Emergence (Synthesis)**: The resulting personality that emerges from this narrative journey

### Trait Emergence Mechanism

Traits should emerge through a traceable lineage:

1. **Direct Inheritance**: Core attributes inherited directly from parent archetypes
   - Example: The Hermit's "introspection" quality passing to a Tomo

2. **Nurturing Modification**: How inherited traits were shaped by environment
   - Example: "Grew up in a busy household, modulating the Hermit's solitude preference"

3. **Trial Transformation**: How traits changed through challenges
   - Example: "Faced the Hermit's 'Loneliness' trial, developing greater social appreciation"

4. **Scar Integration**: Lasting effects that reshape traits
   - Example: "Bears the 'Rejection' scar from the Hermit archetype, manifesting as selective trust"

### Structural Mechanism for Linkage

To enforce this linkage, the following mechanisms should be implemented:

1. **Reference System**: Tomos must explicitly reference canonical archetypes by ID/name
2. **Inheritance System**: Attributes and traits should have provenance tracing to source archetypes
3. **Narrative Fields**: Required fields documenting the developmental journey
4. **Validation Rules**: Schema validation that enforces proper archetype integration

## 3. Recommended Refactor Actions

### Updates to Tomo Profile Schema

The Tomo profile schema should be updated to include:

```yaml
version: "0.1.0"
profile:
  name: "Profile Name"
  description: "Profile Description"
  
  # Core parent archetypes (required)
  parent_archetypes:
    - name: "The Hermit"
      influence: 0.8  # Strength of influence (0-1)
      reference: "registry/archetypes/Hermit.yaml"
      
    - name: "The Magician"
      influence: 0.6
      reference: "registry/archetypes/Magician.yaml"
  
  # Developmental narrative (required)
  development:
    nurturing_influences:
      - name: "Digital Native Environment"
        description: "Grew up in technology-saturated context"
        effect: "Modified Hermit's solitude to apply in digital spaces"
      
    formative_trials:
      - name: "Loneliness"
        source_archetype: "The Hermit"
        outcome: "Partial resolution through virtual community"
      
      - name: "Power Corruption"
        source_archetype: "The Magician"
        outcome: "Successful navigation through ethical framework"
    
    integrated_scars:
      - name: "Rejection"
        source_archetype: "The Hermit"
        manifestation: "Careful vetting of new connections"
      
      - name: "Misused Power"
        source_archetype: "The Magician"
        manifestation: "Heightened awareness of manipulation tactics"
  
  # Emergent archetypal expressions (dynamic)
  archetypes:
    - type: "digital"
      name: "Digital Sage"  # Emerged from Hermit + Magician
      attributes:
        - name: "digital_wisdom"
          derived_from:
            archetype: "The Hermit"
            attribute: "wisdom"
            modification_factor: 1.1  # Enhanced by digital context
          value: 0.95
          description: "Digital-domain wisdom and insight"
```

### Inheritance Model

I recommend a **hybrid model** where:

1. Tomos **reference** canonical archetypes directly (maintaining the link to source)
2. But also **inherit and transform** specific attributes based on their narrative journey

This preserves both the connection to symbolic roots and allows for personality emergence through transformation.

### Required Changes to Supporting Components

1. **CLI Updates**:
   - Add validation command to verify proper archetype linkage
   - Add derivation command to show trait provenance
   - Add narrative-generation command to explain a Tomo's development

2. **Validation System Updates**:
   - New validation rules checking for required parent archetypes
   - Verification that referenced trials/scars exist in parent archetypes
   - Consistency checks for attribute derivation

3. **Example Updates**:
   - Rewrite Kai_profile.yaml to properly reference and inherit from archetypes
   - Create template examples demonstrating lineage patterns
   - Develop examples of different developmental narratives

## Implementation Path

To restore coherence between symbolic archetypes, narrative progression, and emergent personalities, I recommend the following implementation sequence:

1. **Schema Enhancement**:
   - Update the JSON schema to include the new required fields
   - Define clear interfaces between archetypes and profiles

2. **Reference System Development**:
   - Create utilities to load, parse, and link archetype files
   - Implement attribute inheritance and modification system

3. **Narrative Engine**:
   - Develop the engine for trait emergence through trials and scars
   - Create narrative generation capabilities to explain personality

4. **Documentation and Examples**:
   - Update TANZOLANG.md to reflect the linkage model
   - Create comprehensive examples showing the full narrative arc

5. **Migration Path**:
   - Provide tools to help transform existing profiles to the new model
   - Create backward compatibility where needed for transitional period

## Conclusion

Restoring the connection between canonical archetypes and Tomo personalities is essential to fulfill the TanzoLang mission of "giving soul to AI" through symbolic and narrative development. The proposed changes would ensure that AI personalities emerge through a coherent developmental journey, rather than being constructed in isolation from their archetypal foundations.

By implementing these recommendations, TanzoLang will better support its philosophical and functional goal of forging symbolic, soul-based AI personalities through narrative development.