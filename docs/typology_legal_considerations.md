# Legal Considerations for Typological Systems in TanzoLang

## Overview

This document outlines the legal considerations and recommendations for using various typological systems within the TanzoLang framework. The goal is to ensure that our implementation remains open-source and free from intellectual property conflicts while still leveraging the symbolic power of these systems.

## Typological Systems Status

### 1. Zodiac

The zodiac is an ancient astrological system with origins dating back thousands of years. The basic zodiac signs, their attributes, and interpretations are considered common knowledge and part of the public domain.

**Legal Status**: Public domain

**Implementation Guidelines**:
- We can freely implement the twelve zodiac signs with their traditional attributes and meanings
- Our implementation is in `/registry/zodiac/` with each sign having its own YAML file
- We can reference astrological positions like "sun," "moon," and "rising" in profiles

### 2. Kabbalah

Kabbalah is an esoteric tradition within Jewish mysticism, with the Tree of Life (sefirot) being a central concept. The basic structure and traditional interpretations are historical religious teachings.

**Legal Status**: Religious tradition, basic concepts in public domain

**Implementation Guidelines**:
- We can implement the traditional sefirot of the Tree of Life with their established meanings
- Our implementation is in `/registry/kabbalah/` with each sefira having its own YAML file
- We should maintain respectful treatment of these religious concepts
- Modern commercial applications or specific interpretive frameworks might be protected and should be avoided

### 3. Ikigai / Purpose Quadrant

Ikigai is a Japanese concept related to finding purpose in life, often visualized as a Venn diagram with four overlapping elements.

**Legal Status**: The concept is cultural, but specific frameworks may be protected

**Legal Considerations**:
- The term "Ikigai" itself is a general cultural concept
- **Specific concerns**:
  - Commercial frameworks like "Ikigai Types" or "Ikigai Archetypes" may be trademarked
  - Quadrant-based personality classification systems derived from Ikigai could be proprietary
  - Some coaching frameworks using Ikigai have registered trademarks in the US

**Implementation Guidelines**:
- We have renamed this framework to "Purpose Quadrant" or "Soul Compass" to avoid potential trademark issues
- Our implementation is in `/registry/purpose_quadrant/` using a generic structure
- We focus on the four dimensions (passion, expertise, contribution, sustainability) without creating a typology
- We avoid offering predefined "types" unless they are community-generated and openly licensed
- The implementation uses general language like "What you love" rather than proprietary terminology

## Recommendations for Implementation

1. **Prefer generic terminology** over potentially protected commercial terms
2. **Focus on symbolic meaning** rather than diagnostic or prescriptive frameworks
3. **Document sources** transparently where appropriate
4. **Avoid claims** about psychological validity or scientific basis
5. **Emphasize creative and generative use** rather than assessment or classification

## Documentation Guidelines

In all public-facing files and code:
- Avoid terms that suggest formal adoption of trademarked typology systems
- Emphasize symbolic inspiration, open mythos, and culturally sensitive interpretation
- Be clear that TanzoLang is a symbolic language, not a psychological test
- Present typological elements as narrative and symbolic tools, not scientific measurements

> **TanzoLang is a symbolic language, not a test. We encode purpose, not prescribe type.**