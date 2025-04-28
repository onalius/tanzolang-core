/**
 * Zod schema definition for TanzoLang
 */
import { z } from 'zod';

// Enums
export const ArchetypeTypeEnum = z.enum([
  'advisor',
  'companion',
  'creator',
  'educator',
  'entertainer',
  'expert',
  'guide'
]);

export const BehaviorContextEnum = z.enum([
  'always',
  'situational',
  'triggered'
]);

export const CommunicationStyleEnum = z.enum([
  'formal',
  'casual',
  'technical',
  'friendly',
  'direct',
  'nurturing',
  'playful'
]);

export const CommunicationToneEnum = z.enum([
  'professional',
  'warm',
  'enthusiastic',
  'neutral',
  'academic',
  'humorous'
]);

export const ResponseStructureEnum = z.enum([
  'bullet-points',
  'paragraphs',
  'step-by-step',
  'narrative',
  'flexible'
]);

export const FormatPreferenceEnum = z.enum([
  'text',
  'markdown',
  'code',
  'mixed'
]);

// Type alias for values between 0.0 and 1.0
const Ratio = z.number().min(0).max(1);

// Schema definitions
export const ArchetypeSchema = z.object({
  primary: ArchetypeTypeEnum,
  secondary: ArchetypeTypeEnum.optional(),
  description: z.string().optional()
}).refine(data => {
  // If secondary is provided, it must differ from primary
  if (data.secondary && data.secondary === data.primary) {
    return false;
  }
  return true;
}, {
  message: "Secondary archetype must differ from primary"
});

export const BehaviorSchema = z.object({
  name: z.string(),
  description: z.string(),
  strength: Ratio,
  context: BehaviorContextEnum.optional().default('always'),
  trigger: z.string().optional()
}).refine(data => {
  // If context is 'triggered', trigger must be provided
  if (data.context === 'triggered' && !data.trigger) {
    return false;
  }
  return true;
}, {
  message: "Trigger must be provided for triggered behaviors"
});

export const PersonalityTraitsSchema = z.object({
  openness: Ratio.optional().default(0.5),
  conscientiousness: Ratio.optional().default(0.5),
  extraversion: Ratio.optional().default(0.5),
  agreeableness: Ratio.optional().default(0.5),
  neuroticism: Ratio.optional().default(0.5)
});

export const PersonalitySchema = z.object({
  traits: PersonalityTraitsSchema.optional(),
  values: z.array(z.string()).optional(),
  character: z.string().optional()
});

export const CommunicationSchema = z.object({
  style: CommunicationStyleEnum.optional(),
  tone: CommunicationToneEnum.optional(),
  complexity: Ratio.optional().default(0.5),
  verbosity: Ratio.optional().default(0.5)
});

export const KnowledgeDomainSchema = z.object({
  name: z.string(),
  proficiency: Ratio.optional().default(0.5),
  description: z.string().optional()
});

export const KnowledgeSchema = z.object({
  domains: z.array(KnowledgeDomainSchema).optional(),
  limitations: z.array(z.string()).optional()
});

export const InteractionPreferencesSchema = z.object({
  proactivity: Ratio.optional().default(0.5),
  detail: Ratio.optional().default(0.5)
});

export const ResponsePreferencesSchema = z.object({
  structure: ResponseStructureEnum.optional(),
  formatPreference: FormatPreferenceEnum.optional()
});

export const PreferencesSchema = z.object({
  interaction: InteractionPreferencesSchema.optional(),
  response: ResponsePreferencesSchema.optional()
});

export const SimulationParametersSchema = z.object({
  temperature: Ratio.optional().default(0.7),
  randomness: Ratio.optional().default(0.3),
  creativity: Ratio.optional().default(0.5)
});

export const SimulationSchema = z.object({
  parameters: SimulationParametersSchema.optional(),
  constraints: z.array(z.string()).optional()
});

export const ProfileDataSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  archetype: ArchetypeSchema,
  behaviors: z.array(BehaviorSchema).optional(),
  personality: PersonalitySchema.optional(),
  communication: CommunicationSchema.optional(),
  knowledge: KnowledgeSchema.optional(),
  preferences: PreferencesSchema.optional(),
  simulation: SimulationSchema.optional(),
  metadata: z.record(z.any()).optional()
});

export const TanzoProfileSchema = z.object({
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  profile: ProfileDataSchema
});

// TypeScript type definitions derived from Zod schemas
export type ArchetypeType = z.infer<typeof ArchetypeTypeEnum>;
export type BehaviorContext = z.infer<typeof BehaviorContextEnum>;
export type CommunicationStyle = z.infer<typeof CommunicationStyleEnum>;
export type CommunicationTone = z.infer<typeof CommunicationToneEnum>;
export type ResponseStructure = z.infer<typeof ResponseStructureEnum>;
export type FormatPreference = z.infer<typeof FormatPreferenceEnum>;

export type Archetype = z.infer<typeof ArchetypeSchema>;
export type Behavior = z.infer<typeof BehaviorSchema>;
export type PersonalityTraits = z.infer<typeof PersonalityTraitsSchema>;
export type Personality = z.infer<typeof PersonalitySchema>;
export type Communication = z.infer<typeof CommunicationSchema>;
export type KnowledgeDomain = z.infer<typeof KnowledgeDomainSchema>;
export type Knowledge = z.infer<typeof KnowledgeSchema>;
export type InteractionPreferences = z.infer<typeof InteractionPreferencesSchema>;
export type ResponsePreferences = z.infer<typeof ResponsePreferencesSchema>;
export type Preferences = z.infer<typeof PreferencesSchema>;
export type SimulationParameters = z.infer<typeof SimulationParametersSchema>;
export type Simulation = z.infer<typeof SimulationSchema>;
export type ProfileData = z.infer<typeof ProfileDataSchema>;
export type TanzoProfile = z.infer<typeof TanzoProfileSchema>;
