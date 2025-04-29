/**
 * Zod schemas for Tanzo Schema validation
 */

import { z } from 'zod';

// Enums
export enum ProfileType {
  FULL = 'full',
  ARCHETYPE_ONLY = 'archetype_only',
  SIMULATION = 'simulation'
}

export enum DistributionType {
  NORMAL = 'normal',
  UNIFORM = 'uniform',
  EXPONENTIAL = 'exponential'
}

// Trait score schema
export const TraitScoreSchema = z.object({
  base: z.number().min(0).max(10).describe('Base score for the trait'),
  range: z.tuple([z.number(), z.number()]).optional()
    .describe('Range of possible values [min, max]')
    .refine(
      (range) => range ? range[0] <= range[1] : true,
      { message: 'Minimum value must be less than or equal to maximum value' }
    ),
  distribution: z.nativeEnum(DistributionType).optional()
    .describe('Statistical distribution for simulation')
});

export type TraitScore = z.infer<typeof TraitScoreSchema>;

// Skill schema
export const SkillSchema = z.object({
  name: z.string().describe('Name of the skill'),
  proficiency: TraitScoreSchema.describe('Proficiency level for this skill'),
  category: z.string().optional().describe('Skill category'),
  experience_years: z.number().min(0).optional()
    .describe('Years of experience with this skill')
});

export type Skill = z.infer<typeof SkillSchema>;

// Archetype schema
export const ArchetypeSchema = z.object({
  name: z.string().describe('Name of the digital archetype'),
  description: z.string().optional().describe('Description of the digital archetype'),
  core_traits: z.record(TraitScoreSchema).describe('Core personality traits of the archetype')
    .refine(
      (traits) => {
        const requiredTraits = ['intelligence', 'creativity', 'sociability'];
        return requiredTraits.every(trait => trait in traits);
      },
      {
        message: 'Core traits must include: intelligence, creativity, and sociability'
      }
    ),
  skills: z.array(SkillSchema).min(1).describe('Skills possessed by the archetype'),
  interests: z.array(z.string()).optional().describe('Interests of the archetype'),
  values: z.array(z.string()).optional().describe('Core values of the archetype')
});

export type Archetype = z.infer<typeof ArchetypeSchema>;

// Simulation parameters schema
export const SimulationParametersSchema = z.object({
  variation_factor: z.number().min(0).max(1).optional()
    .describe('Factor for variation in simulations'),
  seed: z.number().int().optional()
    .describe('Random seed for reproducible simulations'),
  iterations: z.number().int().min(1).default(100)
    .describe('Number of simulation iterations'),
  environments: z.array(z.string()).optional()
    .describe('Simulation environments')
});

export type SimulationParameters = z.infer<typeof SimulationParametersSchema>;

// Metadata schema
export const MetadataSchema = z.object({
  author: z.string().optional(),
  created_at: z.string().datetime().optional(),
  tags: z.array(z.string()).optional()
});

export type Metadata = z.infer<typeof MetadataSchema>;

// Top-level Tanzo profile schema
export const TanzoProfileSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/)
    .describe('The TanzoLang schema version'),
  profile_type: z.nativeEnum(ProfileType)
    .describe('Type of Tanzo profile'),
  archetype: ArchetypeSchema
    .describe('Digital archetype definition'),
  simulation_parameters: SimulationParametersSchema.optional()
    .describe('Parameters for simulation runs'),
  metadata: MetadataSchema.optional()
    .describe('Additional metadata')
});

export type TanzoProfile = z.infer<typeof TanzoProfileSchema>;
