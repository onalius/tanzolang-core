/**
 * Zod models for TanzoLang schema.
 * 
 * This module provides type-safe data models for working with TanzoLang profiles.
 */

import { z } from 'zod';

// Enums
export const ArchetypeEnum = z.enum([
  'Mentor',
  'Hero',
  'Creator',
  'Explorer',
  'Sage',
  'Rebel',
  'Magician',
  'Ruler',
  'Caregiver',
  'Lover',
  'Jester',
  'Innocent',
]);

export const RelationshipTypeEnum = z.enum([
  'Ally',
  'Mentor',
  'Friend',
  'Rival',
  'Enemy',
  'Family',
  'Colleague',
  'Acquaintance',
  'Other',
]);

export const TimelineEnum = z.enum([
  'Immediate',
  'Short-term',
  'Medium-term',
  'Long-term',
  'Lifelong',
]);

export const ProficiencyEnum = z.enum([
  'Native',
  'Fluent',
  'Proficient',
  'Conversational',
  'Basic',
]);

// Base schemas
export const MetaSchema = z.object({
  version: z.string().default('1.0.0'),
  created: z.string().datetime().optional(),
  updated: z.string().datetime().optional(),
});

export const IdentitySchema = z.object({
  name: z.string(),
  aliases: z.array(z.string()).optional(),
  description: z.string().optional(),
});

export const ArchetypeSchema = z.object({
  primary: ArchetypeEnum,
  secondary: ArchetypeEnum.optional(),
  shadow: ArchetypeEnum.optional(),
});

export const EmotionalRangeSchema = z.object({
  primary: z.string().optional(),
  range: z.object({
    extrovert_introvert: z.number().int().min(-10).max(10).optional(),
    thinking_feeling: z.number().int().min(-10).max(10).optional(),
    practical_imaginative: z.number().int().min(-10).max(10).optional(),
  }).optional(),
});

export const TraitsSchema = z.object({
  strengths: z.array(z.string()).optional(),
  weaknesses: z.array(z.string()).optional(),
  values: z.array(z.string()).optional(),
  emotion_range: EmotionalRangeSchema.optional(),
});

export const CommunicationStyleSchema = z.object({
  formality: z.number().int().min(1).max(10).optional(),
  verbosity: z.number().int().min(1).max(10).optional(),
  directness: z.number().int().min(1).max(10).optional(),
  humor: z.number().int().min(1).max(10).optional(),
});

export const DecisionMakingSchema = z.object({
  impulsivity: z.number().int().min(1).max(10).optional(),
  risk_tolerance: z.number().int().min(1).max(10).optional(),
  deliberation: z.number().int().min(1).max(10).optional(),
});

export const BehaviorSchema = z.object({
  communication_style: CommunicationStyleSchema.optional(),
  decision_making: DecisionMakingSchema.optional(),
  interaction_pattern: z.array(z.string()).optional(),
});

export const LanguageSchema = z.object({
  name: z.string(),
  proficiency: ProficiencyEnum,
});

export const BackgroundSchema = z.object({
  profession: z.string().optional(),
  expertise: z.array(z.string()).optional(),
  education: z.array(z.string()).optional(),
  culture: z.string().optional(),
  languages: z.array(LanguageSchema).optional(),
});

export const RelationshipSchema = z.object({
  entity: z.string(),
  relationship_type: RelationshipTypeEnum,
  dynamics: z.string().optional(),
});

export const GoalSchema = z.object({
  description: z.string(),
  importance: z.number().int().min(1).max(10).optional(),
  timeline: TimelineEnum.optional(),
});

export const StressResponseSchema = z.object({
  primary: z.string().optional(),
  threshold: z.number().int().min(1).max(10).optional(),
  behaviors: z.array(z.string()).optional(),
});

export const AdaptationSchema = z.object({
  flexibility: z.number().int().min(1).max(10).optional(),
  learning_rate: z.number().int().min(1).max(10).optional(),
});

export const RandomizationSchema = z.object({
  variance: z.number().int().min(1).max(10).optional(),
  seed: z.number().int().optional(),
});

export const SimulationsSchema = z.object({
  stress_response: StressResponseSchema.optional(),
  adaptation: AdaptationSchema.optional(),
  randomization: RandomizationSchema.optional(),
});

// Main TanzoProfile schema
export const TanzoProfileSchema = z.object({
  meta: MetaSchema.optional().default({}),
  identity: IdentitySchema,
  archetype: ArchetypeSchema,
  traits: TraitsSchema,
  behavior: BehaviorSchema.optional(),
  background: BackgroundSchema.optional(),
  relationships: z.array(RelationshipSchema).optional(),
  goals: z.array(GoalSchema).optional(),
  simulations: SimulationsSchema.optional(),
});

// Types derived from schemas
export type ArchetypeType = z.infer<typeof ArchetypeEnum>;
export type RelationshipType = z.infer<typeof RelationshipTypeEnum>;
export type TimelineType = z.infer<typeof TimelineEnum>;
export type ProficiencyType = z.infer<typeof ProficiencyEnum>;

export type Meta = z.infer<typeof MetaSchema>;
export type Identity = z.infer<typeof IdentitySchema>;
export type Archetype = z.infer<typeof ArchetypeSchema>;
export type EmotionalRange = z.infer<typeof EmotionalRangeSchema>;
export type Traits = z.infer<typeof TraitsSchema>;
export type CommunicationStyle = z.infer<typeof CommunicationStyleSchema>;
export type DecisionMaking = z.infer<typeof DecisionMakingSchema>;
export type Behavior = z.infer<typeof BehaviorSchema>;
export type Language = z.infer<typeof LanguageSchema>;
export type Background = z.infer<typeof BackgroundSchema>;
export type Relationship = z.infer<typeof RelationshipSchema>;
export type Goal = z.infer<typeof GoalSchema>;
export type StressResponse = z.infer<typeof StressResponseSchema>;
export type Adaptation = z.infer<typeof AdaptationSchema>;
export type Randomization = z.infer<typeof RandomizationSchema>;
export type Simulations = z.infer<typeof SimulationsSchema>;
export type TanzoProfile = z.infer<typeof TanzoProfileSchema>;

/**
 * TanzoProfile class that provides utility methods for working with profiles
 */
export class TanzoProfileClass {
  private profile: TanzoProfile;

  constructor(data: unknown) {
    this.profile = TanzoProfileSchema.parse(data);
  }

  /**
   * Get the underlying profile data
   */
  get data(): TanzoProfile {
    return this.profile;
  }

  /**
   * Create a shorthand string representation of the profile
   */
  toShorthand(): string {
    const parts: string[] = [];
    
    // Identity
    parts.push(this.profile.identity.name);
    
    // Archetype
    let archetypeStr = `[${this.profile.archetype.primary}`;
    if (this.profile.archetype.secondary) {
      archetypeStr += `/${this.profile.archetype.secondary}`;
    }
    if (this.profile.archetype.shadow) {
      archetypeStr += `, shadow:${this.profile.archetype.shadow}`;
    }
    archetypeStr += ']';
    parts.push(archetypeStr);
    
    // Core traits
    if (this.profile.traits.strengths && this.profile.traits.strengths.length > 0) {
      const strengths = this.profile.traits.strengths.slice(0, 3);
      let traitsStr = `Strengths: ${strengths.join(', ')}`;
      if (this.profile.traits.strengths.length > 3) {
        traitsStr += '...';
      }
      parts.push(traitsStr);
    }
    
    return parts.join(' - ');
  }
}
