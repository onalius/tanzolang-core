/**
 * Zod schema definitions for TanzoLang.
 * 
 * This module provides Zod schemas for validating TanzoLang documents,
 * as well as TypeScript type definitions derived from these schemas.
 */

import { z } from 'zod';

// Enum definitions
export const TemperamentEnum = z.enum([
  'analytical',
  'diplomatic',
  'assertive',
  'supportive',
  'creative',
  'practical',
  'mixed',
]);

export type Temperament = z.infer<typeof TemperamentEnum>;

export const LanguageProficiencyEnum = z.enum([
  'native',
  'fluent',
  'advanced',
  'intermediate',
  'basic',
]);

export type LanguageProficiency = z.infer<typeof LanguageProficiencyEnum>;

// Base schema components
export const PersonalityTraitSchema = z.object({
  name: z.string().min(2).max(50),
  value: z.number().min(0).max(10),
  description: z.string().max(500).optional(),
});

export type PersonalityTrait = z.infer<typeof PersonalityTraitSchema>;

export const DomainSchema = z.object({
  name: z.string().min(2).max(100),
  proficiency: z.number().min(0).max(10),
  description: z.string().max(500).optional(),
});

export type Domain = z.infer<typeof DomainSchema>;

export const LanguageSchema = z.object({
  name: z.string().min(2).max(50),
  proficiency: LanguageProficiencyEnum,
});

export type Language = z.infer<typeof LanguageSchema>;

export const CapabilitySchema = z.object({
  name: z.string().min(2).max(100),
  proficiency: z.number().min(0).max(10),
  description: z.string().max(500).optional(),
});

export type Capability = z.infer<typeof CapabilitySchema>;

// Archetype component schemas
export const ArchetypePersonalitySchema = z.object({
  traits: z.array(PersonalityTraitSchema).min(1).max(20),
  values: z.array(z.string().min(2).max(50)).max(10).optional(),
  temperament: TemperamentEnum.optional(),
});

export type ArchetypePersonality = z.infer<typeof ArchetypePersonalitySchema>;

export const ArchetypeKnowledgeSchema = z.object({
  domains: z.array(DomainSchema).min(1).max(20),
  languages: z.array(LanguageSchema).max(10).optional(),
});

export type ArchetypeKnowledge = z.infer<typeof ArchetypeKnowledgeSchema>;

export const ArchetypeCapabilitiesSchema = z.object({
  skills: z.array(CapabilitySchema).min(1).max(30),
  tools: z.array(z.string().min(2).max(100)).max(20).optional(),
});

export type ArchetypeCapabilities = z.infer<typeof ArchetypeCapabilitiesSchema>;

export const ArchetypeAttributesSchema = z.object({
  personality: ArchetypePersonalitySchema,
  knowledge: ArchetypeKnowledgeSchema,
  capabilities: ArchetypeCapabilitiesSchema,
});

export type ArchetypeAttributes = z.infer<typeof ArchetypeAttributesSchema>;

export const ArchetypeIdentitySchema = z.object({
  name: z.string().min(2).max(100),
  role: z.string().min(2).max(100),
  description: z.string().max(1000).optional(),
  tags: z.array(z.string().min(1).max(50)).max(10).optional(),
});

export type ArchetypeIdentity = z.infer<typeof ArchetypeIdentitySchema>;

export const ArchetypeSchema = z.object({
  identity: ArchetypeIdentitySchema,
  attributes: ArchetypeAttributesSchema,
});

export type Archetype = z.infer<typeof ArchetypeSchema>;

// Profile component schemas
export const ProfileInstanceSchema = z.object({
  name: z.string().min(2).max(100),
  created_at: z.string().datetime(),
  version: z.string().regex(/^\d+\.\d+\.\d+$/).optional(),
  description: z.string().max(1000).optional(),
});

export type ProfileInstance = z.infer<typeof ProfileInstanceSchema>;

export const ProfileParametersSchema = z.object({
  temperature: z.number().min(0).max(2).optional(),
  max_tokens: z.number().int().min(1).max(32000).optional(),
  constraints: z.array(z.string().min(2).max(500)).max(10).optional(),
});

export type ProfileParameters = z.infer<typeof ProfileParametersSchema>;

export const ProfileCustomizationsSchema = z.object({
  traits: z.array(PersonalityTraitSchema).max(20).optional(),
  knowledge: z.array(DomainSchema).max(10).optional(),
  skills: z.array(CapabilitySchema).max(10).optional(),
});

export type ProfileCustomizations = z.infer<typeof ProfileCustomizationsSchema>;

export const ProfileSchema = z.object({
  instance: ProfileInstanceSchema,
  parameters: ProfileParametersSchema.optional(),
  customizations: ProfileCustomizationsSchema.optional(),
});

export type Profile = z.infer<typeof ProfileSchema>;

// Top-level document schema
export const TanzoDocumentSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  archetype: ArchetypeSchema,
  profile: ProfileSchema.optional(),
});

export type TanzoDocument = z.infer<typeof TanzoDocumentSchema>;
