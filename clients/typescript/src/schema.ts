/**
 * Zod schema definitions for TanzoLang
 */
import { z } from 'zod';

// Define the personality trait schema
export const personalityTrait = z.object({
  name: z.string().describe('Name of the personality trait'),
  value: z.number()
    .min(0)
    .max(1)
    .describe('Strength of the trait between 0 and 1'),
  variance: z.number()
    .min(0)
    .max(1)
    .describe('Variance of the trait value (for simulation)')
    .optional(),
});

export type PersonalityTraitType = z.infer<typeof personalityTrait>;

// Define the personality schema
export const personality = z.object({
  traits: z.array(personalityTrait).describe('Personality traits'),
  values: z.array(z.string())
    .describe('Core values that guide the archetype\'s behavior')
    .optional(),
  background: z.string()
    .describe('Backstory or origin of the archetype')
    .optional(),
});

export type PersonalityType = z.infer<typeof personality>;

// Define appearance schemas
export const physicalAppearance = z.object({
  height: z.string().optional(),
  build: z.string().optional(),
  age: z.number().optional(),
  features: z.array(z.string()).optional(),
});

export type PhysicalAppearanceType = z.infer<typeof physicalAppearance>;

export const digitalAppearance = z.object({
  avatar: z.string()
    .describe('Description of digital avatar')
    .optional(),
  style: z.string()
    .describe('Visual style of digital representation')
    .optional(),
});

export type DigitalAppearanceType = z.infer<typeof digitalAppearance>;

export const appearance = z.object({
  physical: physicalAppearance.optional(),
  digital: digitalAppearance.optional(),
});

export type AppearanceType = z.infer<typeof appearance>;

// Define behavior schemas
export const behaviorPattern = z.object({
  name: z.string().describe('Name of the behavior pattern'),
  description: z.string().describe('Description of the behavior pattern'),
  triggers: z.array(z.string())
    .describe('Events that trigger this behavior')
    .optional(),
  probability: z.number()
    .min(0)
    .max(1)
    .describe('Probability of exhibiting this behavior when triggered')
    .optional(),
});

export type BehaviorPatternType = z.infer<typeof behaviorPattern>;

export const behavior = z.object({
  patterns: z.array(behaviorPattern).optional(),
  reactions: z.record(z.string(), z.string())
    .describe('How the archetype reacts to different stimuli')
    .optional(),
});

export type BehaviorType = z.infer<typeof behavior>;

// Define archetype schemas
export const archetypeType = z.enum(['digital', 'physical', 'hybrid']);

export type ArchetypeType = z.infer<typeof archetypeType>;

export const archetypeAttributes = z.object({
  personality: personality.describe('Personality attributes'),
  appearance: appearance.optional().describe('Appearance attributes'),
  capabilities: z.array(z.string())
    .describe('Capabilities of the archetype')
    .optional(),
  behavior: behavior.optional().describe('Behavior attributes'),
});

export type ArchetypeAttributesType = z.infer<typeof archetypeAttributes>;

export const archetype = z.object({
  type: archetypeType.describe('The type of archetype'),
  attributes: archetypeAttributes.describe('Attributes of the archetype'),
});

// Define profile schema
export const profile = z.object({
  name: z.string().describe('The name of the profile'),
  description: z.string()
    .describe('A description of the profile')
    .optional(),
  archetype: archetype.describe('The archetype definition'),
  parameters: z.record(z.string(), z.any())
    .describe('Custom parameters that affect the behavior of the profile')
    .optional(),
  metadata: z.record(z.string(), z.any())
    .describe('Additional metadata about the profile')
    .optional(),
});

export type ProfileType = z.infer<typeof profile>;

// Define the top-level schema
export const tanzoSchema = z.object({
  version: z.string()
    .describe('The version of the TanzoLang schema being used')
    .refine(v => v === '0.1.0', {
      message: "Only version '0.1.0' is currently supported",
    }),
  profile: profile.describe('The profile definition'),
});

export type TanzoSchemaType = z.infer<typeof tanzoSchema>;
