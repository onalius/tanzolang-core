/**
 * TanzoLang Profile Validator
 * 
 * A minimal TypeScript script using Zod to validate a TanzoLang profile client-side.
 */

import { z } from 'zod';

// Define schema for normal distribution
const normalDistributionSchema = z.object({
  distribution: z.literal('normal'),
  mean: z.number(),
  stdDev: z.number().positive(),
});

// Define schema for uniform distribution
const uniformDistributionSchema = z.object({
  distribution: z.literal('uniform'),
  min: z.number(),
  max: z.number(),
});

// Define schema for discrete distribution
const discreteDistributionSchema = z.object({
  distribution: z.literal('discrete'),
  values: z.array(z.union([z.string(), z.number(), z.boolean()])),
  weights: z.array(z.number()).optional(),
});

// Combine into a single distribution schema
const distributionSchema = z.union([
  normalDistributionSchema,
  uniformDistributionSchema,
  discreteDistributionSchema,
]);

// Define schema for an attribute value (can be a string, number, boolean, or distribution)
const attributeValueSchema = z.union([
  z.string(),
  z.number(),
  z.boolean(),
  distributionSchema,
]);

// Define schema for an attribute
const attributeSchema = z.object({
  name: z.string(),
  value: attributeValueSchema,
  description: z.string().optional(),
  unit: z.string().optional(),
});

// Define schema for an archetype
const archetypeSchema = z.object({
  type: z.enum(['digital', 'physical', 'hybrid', 'social', 'emotional', 'cognitive']),
  name: z.string(),
  description: z.string().optional(),
  attributes: z.array(attributeSchema),
});

// Define schema for lineage items
const lineageItemSchema = z.object({
  name: z.string(),
  influence: z.number().min(0).max(1),
  description: z.string().optional(),
});

// Define schema for ikigai
const ikigaiSchema = z.object({
  passion: z.string(),
  mission: z.string(),
  profession: z.string(),
  vocation: z.string(),
}).partial();

// Define schema for memory
const memorySchema = z.object({
  episodic: z.object({
    strength: z.number().min(0).max(1),
    decay_rate: z.number().min(0).max(1).optional(),
  }).optional(),
  semantic: z.object({
    strength: z.number().min(0).max(1),
    organization: z.string().optional(),
  }).optional(),
  emotional: z.object({
    strength: z.number().min(0).max(1),
    attachment_bias: z.string().optional(),
  }).optional(),
});

// Define schema for scars
const scarSchema = z.object({
  name: z.string(),
  intensity: z.number().min(0).max(1),
  resolution: z.number().min(0).max(1).optional(),
  triggers: z.array(z.string()).optional(),
  response: z.string().optional(),
});

// Define schema for symbolism
const symbolismSchema = z.object({
  primary_element: z.string().optional(),
  color: z.string().optional(),
  animal: z.string().optional(),
  season: z.string().optional(),
  time_of_day: z.string().optional(),
  recurring_motifs: z.array(z.string()).optional(),
});

// Define schema for a profile
const profileSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  archetypes: z.array(archetypeSchema).min(1),
  lineage: z.array(lineageItemSchema).optional(),
  ikigai: ikigaiSchema.optional(),
  memory: memorySchema.optional(),
  scars: z.array(scarSchema).optional(),
  symbolism: symbolismSchema.optional(),
});

// Define schema for the full TanzoLang document
const tanzoLangSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  profile: profileSchema,
});

// Type for the full TanzoLang document
type TanzoLang = z.infer<typeof tanzoLangSchema>;

/**
 * Validates a TanzoLang profile
 * 
 * @param profile The profile object to validate
 * @returns A result object with success flag and errors or data
 */
function validateTanzoProfile(profile: unknown) {
  try {
    const result = tanzoLangSchema.parse(profile);
    return {
      success: true,
      data: result,
    };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        errors: error.format(),
      };
    }
    return {
      success: false,
      errors: [String(error)],
    };
  }
}

// Example usage
function example() {
  // Example valid profile
  const validProfile = {
    version: '0.1.0',
    profile: {
      name: 'Example Profile',
      description: 'An example TanzoLang profile',
      archetypes: [
        {
          type: 'digital',
          name: 'Digital Self',
          attributes: [
            {
              name: 'creativity',
              value: {
                distribution: 'normal',
                mean: 0.8,
                stdDev: 0.1,
              },
              description: 'Creative capability',
            },
            {
              name: 'username',
              value: 'digital_self',
              description: 'Online identifier',
            },
          ],
        },
      ],
      ikigai: {
        passion: 'Creating digital experiences',
        mission: 'Helping others express themselves',
      },
      symbolism: {
        primary_element: 'air',
        animal: 'owl',
      },
    },
  };

  // Example invalid profile (missing required fields)
  const invalidProfile = {
    version: '0.1.0',
    profile: {
      // Missing name
      archetypes: [
        {
          // Missing type
          name: 'Digital Self',
          attributes: [
            {
              // Missing name
              value: 0.8,
            },
          ],
        },
      ],
    },
  };

  console.log('Validating valid profile:');
  const validResult = validateTanzoProfile(validProfile);
  console.log(JSON.stringify(validResult, null, 2));

  console.log('\nValidating invalid profile:');
  const invalidResult = validateTanzoProfile(invalidProfile);
  console.log(JSON.stringify(invalidResult, null, 2));
}

// Run the example
example();

// Export the validation function and schema
export {
  validateTanzoProfile,
  tanzoLangSchema,
  type TanzoLang,
};
