/**
 * Zod schema models for TanzoLang profiles
 */

import { z } from 'zod';

/**
 * Types of probability distributions
 */
export const DistributionType = z.enum(['normal', 'uniform', 'discrete']);
export type DistributionType = z.infer<typeof DistributionType>;

/**
 * Normal (Gaussian) probability distribution
 */
export const NormalDistribution = z.object({
  distribution: z.literal('normal'),
  mean: z.number(),
  stdDev: z.number().positive('Standard deviation must be greater than 0'),
});
export type NormalDistribution = z.infer<typeof NormalDistribution>;

/**
 * Uniform probability distribution
 */
export const UniformDistribution = z.object({
  distribution: z.literal('uniform'),
  min: z.number(),
  max: z.number(),
}).refine(data => data.max > data.min, {
  message: 'Max must be greater than min',
  path: ['max'],
});
export type UniformDistribution = z.infer<typeof UniformDistribution>;

/**
 * Discrete probability distribution with weighted values
 */
export const DiscreteDistribution = z.object({
  distribution: z.literal('discrete'),
  values: z.array(z.union([z.string(), z.number(), z.boolean()])),
  weights: z.array(z.number().min(0).max(1)),
}).refine(data => data.values.length === data.weights.length, {
  message: 'Number of weights must match number of values',
  path: ['weights'],
});
export type DiscreteDistribution = z.infer<typeof DiscreteDistribution>;

/**
 * Any probability distribution
 */
export const ProbabilityDistribution = z.union([
  NormalDistribution,
  UniformDistribution,
  DiscreteDistribution,
]);
export type ProbabilityDistribution = z.infer<typeof ProbabilityDistribution>;

/**
 * Value of an attribute
 */
export const AttributeValue = z.union([
  z.string(),
  z.number(),
  z.boolean(),
  ProbabilityDistribution,
]);
export type AttributeValue = z.infer<typeof AttributeValue>;

/**
 * An attribute in a TanzoLang profile
 */
export const Attribute = z.object({
  name: z.string(),
  value: AttributeValue,
  description: z.string().optional(),
  unit: z.string().optional(),
});
export type Attribute = z.infer<typeof Attribute>;

/**
 * Types of archetypes
 */
export const ArchetypeType = z.enum(['digital', 'physical', 'hybrid']);
export type ArchetypeType = z.infer<typeof ArchetypeType>;

/**
 * An archetype in a TanzoLang profile
 */
export const Archetype = z.object({
  type: ArchetypeType,
  name: z.string().optional(),
  description: z.string().optional(),
  attributes: z.array(Attribute).nonempty('Archetype must have at least one attribute'),
});
export type Archetype = z.infer<typeof Archetype>;

/**
 * The main profile section in a TanzoLang profile
 */
export const Profile = z.object({
  name: z.string(),
  description: z.string().optional(),
  archetypes: z.array(Archetype).nonempty('Profile must have at least one archetype'),
});
export type Profile = z.infer<typeof Profile>;

/**
 * A complete TanzoLang profile
 */
export const TanzoProfile = z.object({
  version: z.string().default('0.1.0'),
  profile: Profile,
});
export type TanzoProfile = z.infer<typeof TanzoProfile>;
