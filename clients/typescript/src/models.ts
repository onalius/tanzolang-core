/**
 * Zod schema models for the TanzoLang schema.
 */

import { z } from 'zod';

/**
 * Schema for a personality trait.
 */
export const TraitSchema = z.object({
  value: z.number().int().min(0).max(100).describe('Trait value on scale of 0-100'),
  variance: z.number().int().min(0).max(50).optional().describe('Variance for simulation'),
  description: z.string().optional(),
});

export type Trait = z.infer<typeof TraitSchema>;

/**
 * Schema for a character attribute.
 */
export const AttributeSchema = z.object({
  value: z.number().int().min(0).max(100).describe('Attribute value on scale of 0-100'),
  variance: z.number().int().min(0).max(50).optional().describe('Variance for simulation'),
  notes: z.string().optional(),
});

export type Attribute = z.infer<typeof AttributeSchema>;

/**
 * Schema for an interest.
 */
export const InterestSchema = z.object({
  name: z.string(),
  level: z.number().int().min(1).max(10).optional().describe('Interest level from 1-10'),
});

export type Interest = z.infer<typeof InterestSchema>;

/**
 * Schema for a key event in a character's backstory.
 */
export const KeyEventSchema = z.object({
  age: z.number().int().optional(),
  description: z.string(),
  impact: z.string().optional(),
});

export type KeyEvent = z.infer<typeof KeyEventSchema>;

/**
 * Schema for cognitive style attributes.
 */
export const CognitiveStyleSchema = z.object({
  analytical: AttributeSchema.optional(),
  creative: AttributeSchema.optional(),
  practical: AttributeSchema.optional(),
});

export type CognitiveStyle = z.infer<typeof CognitiveStyleSchema>;

/**
 * Schema for communication style attributes.
 */
export const CommunicationStyleSchema = z.object({
  formal: AttributeSchema.optional(),
  casual: AttributeSchema.optional(),
  direct: AttributeSchema.optional(),
  verbose: AttributeSchema.optional(),
});

export type CommunicationStyle = z.infer<typeof CommunicationStyleSchema>;

/**
 * Schema for social behavior attributes.
 */
export const SocialBehaviorSchema = z.object({
  collaborative: AttributeSchema.optional(),
  competitive: AttributeSchema.optional(),
  supportive: AttributeSchema.optional(),
  challenging: AttributeSchema.optional(),
});

export type SocialBehavior = z.infer<typeof SocialBehaviorSchema>;

/**
 * Schema for problem-solving behavior attributes.
 */
export const ProblemSolvingBehaviorSchema = z.object({
  systematic: AttributeSchema.optional(),
  intuitive: AttributeSchema.optional(),
  innovative: AttributeSchema.optional(),
  cautious: AttributeSchema.optional(),
});

export type ProblemSolvingBehavior = z.infer<typeof ProblemSolvingBehaviorSchema>;

/**
 * Schema for character behaviors.
 */
export const BehaviorsSchema = z.object({
  social: SocialBehaviorSchema.optional(),
  problem_solving: ProblemSolvingBehaviorSchema.optional(),
});

export type Behaviors = z.infer<typeof BehaviorsSchema>;

/**
 * Schema for character backstory information.
 */
export const BackstorySchema = z.object({
  background: z.string().optional(),
  key_events: z.array(KeyEventSchema).optional(),
});

export type Backstory = z.infer<typeof BackstorySchema>;

/**
 * Schema for character attributes.
 */
export const AttributesSchema = z.object({
  cognitive_style: CognitiveStyleSchema.optional(),
  communication_style: CommunicationStyleSchema.optional(),
  interests: z.array(InterestSchema).optional(),
  values: z.array(z.string()).optional(),
});

export type Attributes = z.infer<typeof AttributesSchema>;

/**
 * Schema for the Big Five personality traits.
 */
export const TraitsSchema = z.object({
  openness: TraitSchema,
  conscientiousness: TraitSchema,
  extraversion: TraitSchema,
  agreeableness: TraitSchema,
  neuroticism: TraitSchema,
});

export type Traits = z.infer<typeof TraitsSchema>;

/**
 * Schema for the digital archetype definition.
 */
export const DigitalArchetypeSchema = z.object({
  traits: TraitsSchema,
  attributes: AttributesSchema,
  behaviors: BehaviorsSchema.optional(),
  backstory: BackstorySchema.optional(),
});

export type DigitalArchetype = z.infer<typeof DigitalArchetypeSchema>;

/**
 * Schema for Monte-Carlo simulation parameters.
 */
export const SimulationParametersSchema = z.object({
  variance: z.number().min(0).max(1).optional().describe('Variance factor'),
  contexts: z.array(z.string()).optional(),
});

export type SimulationParameters = z.infer<typeof SimulationParametersSchema>;

/**
 * Schema for profile metadata.
 */
export const MetadataSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/, 'Version must be in the format X.Y.Z'),
  name: z.string(),
  description: z.string().optional(),
  author: z.string().optional(),
  created_at: z.string().datetime().optional(),
  updated_at: z.string().datetime().optional(),
});

export type Metadata = z.infer<typeof MetadataSchema>;

/**
 * Root schema for a complete TanzoLang profile.
 */
export const TanzoProfileSchema = z.object({
  metadata: MetadataSchema,
  digital_archetype: DigitalArchetypeSchema,
  simulation_parameters: SimulationParametersSchema.optional(),
});

export type TanzoProfile = z.infer<typeof TanzoProfileSchema>;
