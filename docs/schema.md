# TanzoLang Schema

The TanzoLang schema is a JSON Schema that defines the structure of Tomodaichi Tanzo profile documents. It allows for the creation of structured digital character profiles with consistent properties and validation.

## Schema Structure

The root schema object consists of:

- `version`: Schema version following semantic versioning format (e.g., "0.1.0")
- `profile`: The main profile object with all character properties

### Profile Object

The profile object is the main container for character information:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Profile name (required) |
| `description` | string | Profile description |
| `archetype` | object | Character archetype (required) |
| `behaviors` | array | List of behavior traits |
| `personality` | object | Personality characteristics |
| `communication` | object | Communication style & preferences |
| `knowledge` | object | Knowledge domains & limitations |
| `preferences` | object | General preferences |
| `simulation` | object | Simulation parameters |
| `metadata` | object | Additional custom metadata |

## Archetypes

The archetype defines the core role or function of a character:

| Property | Type | Description |
|----------|------|-------------|
| `primary` | string | Primary archetype (required) |
| `secondary` | string | Secondary/hybrid archetype |
| `description` | string | Custom archetype description |

Available archetype values:

- `advisor`
- `companion`
- `creator`
- `educator`
- `entertainer`
- `expert`
- `guide`

## Behaviors

Behaviors define specific character traits:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Behavior name (required) |
| `description` | string | Behavior description (required) |
| `strength` | number | Strength from 0.0-1.0 (required) |
| `context` | string | Context when behavior applies |
| `trigger` | string | Trigger pattern for situational behaviors |

Context values:
- `always` (default)
- `situational`
- `triggered` (requires `trigger` property)

## Personality

The personality section defines character traits and values:

| Property | Type | Description |
|----------|------|-------------|
| `traits` | object | OCEAN personality model traits |
| `values` | array | Core values list |
| `character` | string | Character description |

The personality traits follow the OCEAN (Big Five) model:

- `openness`: Openness to experience (0.0-1.0)
- `conscientiousness`: Conscientiousness (0.0-1.0)
- `extraversion`: Extraversion (0.0-1.0)
- `agreeableness`: Agreeableness (0.0-1.0)
- `neuroticism`: Neuroticism (0.0-1.0)

## Communication

Communication defines how the character expresses itself:

| Property | Type | Description |
|----------|------|-------------|
| `style` | string | Communication style |
| `tone` | string | Communication tone |
| `complexity` | number | Language complexity (0.0-1.0) |
| `verbosity` | number | Response verbosity (0.0-1.0) |

Available style values:
- `formal`
- `casual`
- `technical`
- `friendly`
- `direct`
- `nurturing`
- `playful`

Available tone values:
- `professional`
- `warm`
- `enthusiastic`
- `neutral`
- `academic`
- `humorous`

## Schema Example

Here's a simplified example of a TanzoLang profile in JSON format:

```json
{
  "version": "0.1.0",
  "profile": {
    "name": "Example Assistant",
    "description": "A helpful digital assistant",
    "archetype": {
      "primary": "advisor",
      "secondary": "companion"
    },
    "behaviors": [
      {
        "name": "Helpfulness",
        "description": "Offers assistance proactively",
        "strength": 0.9
      }
    ],
    "personality": {
      "traits": {
        "openness": 0.7,
        "conscientiousness": 0.8,
        "extraversion": 0.6,
        "agreeableness": 0.9,
        "neuroticism": 0.2
      }
    }
  }
}
