/**
 * Validation utilities for TanzoLang documents.
 * 
 * This module provides functions for validating TanzoLang documents
 * using the Zod schemas defined in the models module.
 */

import { z } from 'zod';
import { load } from 'js-yaml';
import { promises as fs } from 'fs';
import path from 'path';
import { TanzoDocumentSchema, TanzoDocument } from './models';

/**
 * Validate a TanzoLang document against the Zod schema.
 * 
 * @param document The document to validate
 * @returns The validated document if successful
 * @throws If validation fails
 */
export function validateDocument(document: unknown): TanzoDocument {
  return TanzoDocumentSchema.parse(document);
}

/**
 * Validate a TanzoLang document from a YAML string.
 * 
 * @param yamlStr The YAML string to validate
 * @returns The validated document if successful
 * @throws If validation fails or if the YAML is invalid
 */
export function validateYaml(yamlStr: string): TanzoDocument {
  const document = load(yamlStr) as unknown;
  return validateDocument(document);
}

/**
 * Validate a TanzoLang document from a file.
 * 
 * @param filePath Path to the YAML file
 * @returns A promise that resolves to the validated document if successful
 * @throws If validation fails, if the YAML is invalid, or if the file cannot be read
 */
export async function validateFile(filePath: string): Promise<TanzoDocument> {
  const yamlStr = await fs.readFile(filePath, 'utf-8');
  return validateYaml(yamlStr);
}

/**
 * Performs extended validation beyond the basic schema validation.
 * 
 * This includes checks that can't be expressed in the Zod schema alone,
 * such as ensuring trait customizations reference traits that exist in the archetype.
 * 
 * @param document The document to validate
 * @returns true if the extended validation passes
 * @throws If extended validation fails
 */
export function performExtendedValidation(document: TanzoDocument): boolean {
  if (!document.profile || !document.profile.customizations || !document.profile.customizations.traits) {
    return true;
  }

  // Collect trait names from the archetype
  const archetypeTraitNames = new Set(
    document.archetype.attributes.personality.traits.map(trait => trait.name)
  );
  
  // Check that each customized trait exists in the archetype
  for (const trait of document.profile.customizations.traits) {
    if (!archetypeTraitNames.has(trait.name)) {
      throw new Error(`Customized trait '${trait.name}' does not exist in the archetype`);
    }
  }
  
  return true;
}
