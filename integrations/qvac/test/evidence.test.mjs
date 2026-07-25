import assert from 'node:assert/strict'
import test from 'node:test'

import { buildBoundedEvidencePrompt, sanitizeCogniPrintProfile } from '../src/evidence.mjs'

const fixture = {
  metrics: { word_count: 42, char_count: 240 },
  raw_fingerprint: { mean_word_length: 4.2 },
  fingerprint: { mean_word_length: 0.275 },
  fingerprint_vector: [0.275],
  content_hash: 'a'.repeat(64),
  fingerprint_version: 'cognitive-fingerprint-v2.0',
  feature_schema: [],
  normalization: { method: 'bounded_minmax_v1' },
  disclaimer: 'descriptive research only',
  source: { type: 'file', ref: '/private/path/to/source.txt' },
  saved_profile: '/private/path/to/saved.json',
  raw_text: 'TOP_SECRET_TEXT'
}

test('sanitizer removes local paths and raw/unapproved fields', () => {
  const evidence = sanitizeCogniPrintProfile(fixture)
  const serialized = JSON.stringify(evidence)

  assert.equal(evidence.schema, 'cogniprint-local-evidence-v1')
  assert.equal(evidence.content_hash, 'a'.repeat(64))
  assert.equal(evidence.fingerprint_version, 'cognitive-fingerprint-v2.0')
  assert.equal(evidence.claim_boundary.exact_model_attribution, false)
  assert.equal(evidence.claim_boundary.actor_or_commissioner_identification, false)
  assert.equal(serialized.includes('TOP_SECRET_TEXT'), false)
  assert.equal(serialized.includes('/private/path'), false)
  assert.equal('source' in evidence, false)
  assert.equal('raw_text' in evidence, false)
})

test('bounded prompt carries explicit non-claims and only sanitized evidence', () => {
  const evidence = sanitizeCogniPrintProfile(fixture)
  const prompt = buildBoundedEvidencePrompt(evidence)

  assert.match(prompt, /Never identify an author, exact neural model, AI origin/i)
  assert.match(prompt, /commissioning actor/i)
  assert.match(prompt, /Evidence JSON:/)
  assert.equal(prompt.includes('TOP_SECRET_TEXT'), false)
  assert.equal(prompt.includes('/private/path'), false)
})

test('sanitizer rejects malformed hash', () => {
  assert.throws(
    () => sanitizeCogniPrintProfile({ ...fixture, content_hash: 'not-a-sha256' }),
    /valid SHA-256/
  )
})
