# TanzoLang Core Framework Checklist

This checklist tracks the implementation of missing components for the TanzoLang Core framework, which aims to be an open-source framework for defining AI personalities using archetypal and typological systems.

## ✅ Checklist of Missing Framework Components

### 1. `TANZOLANG.md` (specification)
- [x] Create a top-level markdown file explaining TanzoLang as a structured language for encoding AI personality blueprints.
- [x] Include a formal breakdown of all supported fields in a TanzoLang profile (e.g., `lineage`, `scars`, `ikigai`, `memory`, etc.).
- [x] Provide both a YAML and JSON example of a complete profile.
- [x] Explain the intent behind each symbolic field: what it contributes to the behavior of an AI personality.

### 2. `/registry/archetypes/`
- [x] Create a directory to hold canonical archetypes such as `Magician.yaml`, `Hermit.yaml`, `Lover.yaml`, etc.
- [x] Each file should include:
  - Symbolic meaning
  - Behavioral traits
  - Associated zodiac/Kabbalah alignments
  - Common scars and trials
- [x] These files will serve as reusable personality components for AI character design.

### 3. `/examples/integrations/`
- [x] Create a Jupyter notebook that loads a TanzoLang profile and converts it into a LangChain prompt.
- [x] Add a minimal Node.js/TypeScript script using the Zod schema to validate a Tanzo profile client-side.
- [x] Include a Python CLI tool that loads a `.yml` profile and returns:
  - Full prompt export
  - Emojitype string
  - Simulation sample

### 4. `README.md` Rewrite
- [x] Replace the current intro with a mission-driven description:
  > "TanzoLang is an open-source language for giving soul to AI."
- [x] Emphasize the goal of enabling symbolic, archetypal personality definition across platforms.
- [x] Add links to:
  - [TomoTanzo.com](https://tomotanzo.com)
  - `TANZOLANG.md`
  - `framework-checklist.md`
- [x] Add usage instructions for both pip and Poetry.

### 5. `/docs` Site Prep
- [x] If not present, create `mkdocs.yml` with placeholder pages.
- [x] Add:
  - Philosophy and purpose overview
  - Auto-imported schema reference from JSON
  - Getting started page
- [x] Prepare for future hosting on GitHub Pages.

### 6. `Ethics.md`
- [x] Draft a clear ethics file addressing:
  - Why archetypes and symbols matter
  - The risks and responsibilities of building AI personas
  - The open, non-extractive intent of this framework

### 7. License and Contribution Clarity
- [x] Confirm the use of the Apache 2.0 license in the root LICENSE file.
- [x] Add a badge to the README for `CONTRIBUTING.md`
- [x] Ensure all schema, archetype files, and examples clearly fall under the same license.
