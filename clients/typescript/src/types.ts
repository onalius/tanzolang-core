/**
 * Zod schema definitions for TanzoLang
 */

import { z } from 'zod';

// Trait schema
export const TraitSchema = z.object({
  name: z.string().describe('Name of the trait'),
  value: z.number()
    .min(-1)
    .max(1)
    .describe('Strength of the trait (-1.0 to 1.0)'),
  description: z.string().optional().describe('Description of the trait')
});

export type Trait = z.infer<typeof TraitSchema>;

// Behavioral Pattern schema
export const BehavioralPatternSchema = z.object({
  trigger: z.string().describe('Event or condition that triggers this behavior'),
  response: z.string().describe('The behavior or response to the trigger'),
  probability: z.number()
    .min(0)
    .max(1)
    .default(1.0)
    .describe('Probability of this response occurring (0.0 to 1.0)')
});

export type BehavioralPattern = z.infer<typeof BehavioralPatternSchema>;

// Archetype schema
export const ArchetypeSchema = z.object({
  name: z.string().describe('Name of the personality archetype'),
  description: z.string().optional().describe('Description of this archetype'),
  weight: z.number()
    .min(0)
    .max(1)
    .describe('Relative influence of this archetype (0.0 to 1.0)'),
  traits: z.array(TraitSchema).optional().describe('Specific traits of this archetype'),
  behavioral_patterns: z.array(BehavioralPatternSchema)
    .optional()
    .describe('Behavioral patterns associated with this archetype')
});

export type Archetype = z.infer<typeof ArchetypeSchema>;

// Physical Form schema
export const PhysicalFormTypeEnum = z.enum(['human', 'animal', 'robot', 'digital', 'other']);
export type PhysicalFormType = z.infer<typeof PhysicalFormTypeEnum>;

export const PhysicalFormSchema = z.object({
  type: PhysicalFormTypeEnum.describe('Type of physical form'),
  description: z.string().optional().describe('Description of the physical appearance'),
  attributes: z.record(z.any()).optional().describe('Physical attributes')
});

export type PhysicalForm = z.infer<typeof PhysicalFormSchema>;

// Relationship schema
export const RelationshipSchema = z.object({
  entity: z.string().describe('Name or identifier of the related entity'),
  type: z.string().describe('Type of relationship'),
  description: z.string().optional().describe('Description of the relationship'),
  strength: z.number()
    .min(-1)
    .max(1)
    .optional()
    .describe('Strength of the relationship (-1.0 to 1.0)')
});

export type Relationship = z.infer<typeof RelationshipSchema>;

// Metadata schema
export const MetadataSchema = z.object({
  name: z.string().optional().describe('Name of the profile'),
  description: z.string().optional().describe('Description of the profile'),
  author: z.string().optional().describe('Author of the profile'),
  created_at: z.string().datetime().optional().describe('Creation timestamp'),
  updated_at: z.string().datetime().optional().describe('Last update timestamp'),
  tags: z.array(z.string()).optional().describe('Tags associated with this profile')
});

export type Metadata = z.infer<typeof MetadataSchema>;

// Profile schema (root)
export const ProfileSchema = z.object({
  profile_version: z.string().default('1.0.0').describe('Version of the TanzoLang profile format'),
  metadata: MetadataSchema.optional().describe('Metadata about the profile'),
  archetypes: z.array(ArchetypeSchema)
    .min(1)
    .describe('Array of personality archetypes that make up this profile'),
  physical_form: PhysicalFormSchema.optional().describe('Physical characteristics of the entity'),
  relationships: z.array(RelationshipSchema)
    .optional()
    .describe('Relationships with other entities'),
  backstory: z.string().optional().describe('Background narrative for this profile')
});

export type Profile = z.infer<typeof ProfileSchema>;
