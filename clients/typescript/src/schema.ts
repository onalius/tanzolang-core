/**
 * Zod schema definitions for TanzoLang
 */

import { z } from 'zod';

// Enums
export const ProfileTypeEnum = z.enum(['human', 'digital', 'hybrid']);
export type ProfileType = z.infer<typeof ProfileTypeEnum>;

export const RelationshipTypeEnum = z.enum([
  'friend', 
  'family', 
  'colleague', 
  'acquaintance', 
  'mentor', 
  'student', 
  'other'
]);
export type RelationshipType = z.infer<typeof RelationshipTypeEnum>;

// Trait schema
export const TraitSchema = z.object({
  name: z.string(),
  value: z.number().min(0).max(100),
  variance: z.number().min(0).max(50).optional(),
});
export type Trait = z.infer<typeof TraitSchema>;

// Archetype schema
export const ArchetypeSchema = z.object({
  name: z.string(),
  influence: z.number().min(0).max(100),
  description: z.string().optional(),
  traits: z.array(TraitSchema).optional(),
});
export type Archetype = z.infer<typeof ArchetypeSchema>;

// Capability schema
export const CapabilitySchema = z.object({
  name: z.string(),
  level: z.number().min(0).max(100),
  description: z.string().optional(),
});
export type Capability = z.infer<typeof CapabilitySchema>;

// Relationship schema
export const RelationshipSchema = z.object({
  target: z.string(),
  type: RelationshipTypeEnum,
  strength: z.number().min(0).max(100),
  description: z.string().optional(),
});
export type Relationship = z.infer<typeof RelationshipSchema>;

// Profile properties schema
export const ProfilePropertiesSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  traits: z.array(TraitSchema).optional(),
  archetypes: z.array(ArchetypeSchema).optional(),
  capabilities: z.array(CapabilitySchema).optional(),
  relationships: z.array(RelationshipSchema).optional(),
});
export type ProfileProperties = z.infer<typeof ProfilePropertiesSchema>;

// Profile schema
export const ProfileSchema = z.object({
  id: z.string().regex(/^[a-zA-Z0-9_-]+$/),
  type: ProfileTypeEnum,
  properties: ProfilePropertiesSchema,
  metadata: z.record(z.any()).optional(),
});
export type Profile = z.infer<typeof ProfileSchema>;

// TanzoDocument schema (top-level)
export const TanzoDocumentSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  profile: ProfileSchema,
});
export type TanzoDocument = z.infer<typeof TanzoDocumentSchema>;
