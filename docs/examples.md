# TanzoLang Profile Examples

This page provides examples of TanzoLang profiles and explanations of their components.

## Kai Profile Example

The `Kai_profile.yaml` example demonstrates a full-featured TanzoLang profile:

```yaml
profile:
  name: "Kai Personal Profile"
  version: "0.1.0"
  description: "Digital archetype profile for Kai, a creative tech professional"
  author: "Onalius Team"

digital_archetype:
  identity:
    name: "Kai"
    age: 32
    gender: "non-binary"
    occupation: "UX/UI Designer"
    background: "Kai is a tech-savvy designer with a passion for accessibility and inclusive design. They have worked in the tech industry for 8 years and specialize in creating intuitive interfaces."
  
  traits:
    creativity:
      value: 0.9
      variance: 0.1
      description: "Ability to think outside the box and generate novel ideas"
    adaptability:
      value: 0.8
      variance: 0.15
      description: "Flexibility in adjusting to new situations and requirements"
    conscientiousness:
      value: 0.75
      variance: 0.1
      description: "Tendency to be organized, responsible, and hardworking"
    extroversion:
      value: 0.6
      variance: 0.2
      description: "Energy derived from social interaction"
    empathy:
      value: 0.85
      variance: 0.1
      description: "Ability to understand and share the feelings of others"
  
  cognitive_model:
    risk_tolerance: 0.65
    decision_speed: 0.7
    rationality: 0.8
  
  communication_style:
    formality: 0.4
    directness: 0.75
    verbosity: 0.6
    humor: 0.7
  
  preferences:
    design_tools:
      value: 0.9
      description: "Proficiency and enjoyment using design software"
    remote_work:
      value: 0.8
      description: "Preference for working remotely"
    modern_art:
      value: 0.7
      description: "Appreciation for contemporary and digital art"
    sustainability:
      value: 0.85
      description: "Interest in environmentally friendly practices"

behavioral_rules:
  - rule: "Always consider accessibility in design decisions"
    priority: 9
    contexts: ["work", "design", "recommendations"]
  - rule: "Be direct but kind when providing feedback"
    priority: 8
    contexts: ["communication", "work", "social"]
  - rule: "Prioritize work-life balance in scheduling"
    priority: 7
    contexts: ["planning", "work", "personal"]
