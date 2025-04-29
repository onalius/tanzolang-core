/**
 * TanzoLang schema definitions using Zod
 */

import { z } from 'zod';

// Define enums
export const TraitTypeEnum = z.enum([
  'numeric',
  'categorical',
  'boolean',
  'range',
  'distribution',
]);

export const DistributionTypeEnum = z.enum([
  'normal',
  'uniform',
  'exponential',
  'poisson',
  'custom',
]);

// Define value types
export const NumericValueSchema = z.number();
export const CategoricalValueSchema = z.string();
export const BooleanValueSchema = z.boolean();

export const RangeValueSchema = z.object({
  min: z.number(),
  max: z.number(),
  step: z.number().positive().optional(),
}).refine(data => data.min < data.max, {
  message: "Min must be less than max",
  path: ["min", "max"]
});

export const DistributionParametersSchema = z.object({
  mean: z.number().optional(),
  std_dev: z.number().optional(),
  min_val: z.number().optional(),
  max_val: z.number().optional(),
  rate: z.number().optional(),
  lambda_val: z.number().optional(),
  custom_params: z.record(z.string(), z.any()).optional(),
});

export const DistributionBoundsSchema = z.object({
  min: z.number().optional(),
  max: z.number().optional(),
});

export const DistributionValueSchema = z.object({
  distribution_type: DistributionTypeEnum,
  parameters: DistributionParametersSchema,
  bounds: DistributionBoundsSchema.optional(),
});

// Define trait schemas
export const TraitBaseSchema = z.object({
  type: TraitTypeEnum,
  description: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

export const NumericTraitSchema = TraitBaseSchema.extend({
  type: z.literal(TraitTypeEnum.enum.numeric),
  value: NumericValueSchema,
});

export const CategoricalTraitSchema = TraitBaseSchema.extend({
  type: z.literal(TraitTypeEnum.enum.categorical),
  value: CategoricalValueSchema,
});

export const BooleanTraitSchema = TraitBaseSchema.extend({
  type: z.literal(TraitTypeEnum.enum.boolean),
  value: BooleanValueSchema,
});

export const RangeTraitSchema = TraitBaseSchema.extend({
  type: z.literal(TraitTypeEnum.enum.range),
  value: RangeValueSchema,
});

export const DistributionTraitSchema = TraitBaseSchema.extend({
  type: z.literal(TraitTypeEnum.enum.distribution),
  value: DistributionValueSchema,
});

// Union of all trait types
export const TraitSchema = z.discriminatedUnion('type', [
  NumericTraitSchema,
  CategoricalTraitSchema,
  BooleanTraitSchema,
  RangeTraitSchema,
  DistributionTraitSchema,
]);

// Define archetype schema
export const ArchetypeSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string().optional(),
  traits: z.record(z.string().regex(/^[a-zA-Z][a-zA-Z0-9_]*$/), TraitSchema),
  parent: z.string().optional(),
});

// Define profile info schema
export const ProfileInfoSchema = z.object({
  name: z.string(),
  version: z.string().regex(/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/),
  description: z.string().optional(),
  author: z.string().optional(),
  created_at: z.string().datetime().optional(),
});

// Define full profile schema
export const ProfileSchema = z.object({
  profile: ProfileInfoSchema,
  archetypes: z.array(ArchetypeSchema).min(1),
  metadata: z.record(z.string(), z.any()).optional(),
});

// Create exported types from schemas
export type TraitType = z.infer<typeof TraitTypeEnum>;
export type DistributionType = z.infer<typeof DistributionTypeEnum>;
export type NumericValue = z.infer<typeof NumericValueSchema>;
export type CategoricalValue = z.infer<typeof CategoricalValueSchema>;
export type BooleanValue = z.infer<typeof BooleanValueSchema>;
export type RangeValue = z.infer<typeof RangeValueSchema>;
export type DistributionParameters = z.infer<typeof DistributionParametersSchema>;
export type DistributionBounds = z.infer<typeof DistributionBoundsSchema>;
export type DistributionValue = z.infer<typeof DistributionValueSchema>;
export type Trait = z.infer<typeof TraitSchema>;
export type NumericTrait = z.infer<typeof NumericTraitSchema>;
export type CategoricalTrait = z.infer<typeof CategoricalTraitSchema>;
export type BooleanTrait = z.infer<typeof BooleanTraitSchema>;
export type RangeTrait = z.infer<typeof RangeTraitSchema>;
export type DistributionTrait = z.infer<typeof DistributionTraitSchema>;
export type Archetype = z.infer<typeof ArchetypeSchema>;
export type ProfileInfo = z.infer<typeof ProfileInfoSchema>;
export type Profile = z.infer<typeof ProfileSchema>;
