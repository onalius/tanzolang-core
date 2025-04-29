/**
 * Zod schemas for the TanzoLang specification
 */

import { z } from 'zod';

// Define the possible archetype types
export const archetypeTypeSchema = z.enum([
  'digital',
  'physical',
  'social',
  'emotional',
  'cognitive'
]);

export type ArchetypeType = z.infer<typeof archetypeTypeSchema>;

// Define a trait
export const traitSchema = z.object({
  name: z.string().min(1),
  value: z.number().min(0).max(1),
  variance: z.number().min(0).max(1).optional().default(0.1),
  description: z.string().optional()
});

export type Trait = z.infer<typeof traitSchema>;

// Define an archetype
export const archetypeSchema = z.object({
  type: archetypeTypeSchema,
  weight: z.number().min(0).max(1),
  traits: z.array(traitSchema).optional(),
  attributes: z.record(z.any()).optional()
});

export type Archetype = z.infer<typeof archetypeSchema>;

// Define a profile
export const profileSchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  archetypes: z.array(archetypeSchema).min(1),
  metadata: z.record(z.any()).optional()
}).passthrough();

export type Profile = z.infer<typeof profileSchema>;

// Define the root TanzoLang document
export const tanzoDocumentSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/).default("0.1.0"),
  profile: profileSchema
}).passthrough();

export type TanzoDocument = z.infer<typeof tanzoDocumentSchema>;

// Define simulation result type
export type SimulationResult = {
  traitMeans: Record<string, Record<string, number>>;
  traitStdDevs: Record<string, Record<string, number>>;
  archetypeWeights: Record<string, number>;
  numIterations: number;
};
