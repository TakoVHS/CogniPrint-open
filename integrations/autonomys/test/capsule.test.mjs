import assert from 'node:assert/strict'
import test from 'node:test'

import {
  buildEvidenceCapsule,
  canonicalJson,
  verifyEvidenceCapsule
} from '../src/capsule.mjs'

function fixtureProfile() {
  return {
    metrics: { word_count: 42, char_count: 240 },
    fingerprint: { mean_word_length: 0.275, type_token_ratio: 0.51 },
    fingerprint_vector: [0.275, 0.51],
    content_hash: 'a'.repeat(64),
    fingerprint_version: 'cognitive-fingerprint-v2.0',
    normalization: { method: 'bounded_minmax_v1' },
    disclaimer: 'descriptive research only',
    source: { type: 'file', ref: '/private/path/to/source.txt' },
    saved_profile: '/private/path/to/saved.json',
    raw_text: 'TOP_SECRET_TEXT'
  }
}

function fixtureContext() {
  return {
    publication_intent: 'public-audit',
    cogniprint_commit_sha: 'b'.repeat(40),
    experiment_id: 'raid-m1-clean-en',
    dataset_id: 'liamdugan/raid',
    dataset_revision: '865cac74188466cb0c3b7574a10204007b57a459',
    configuration_sha256: 'c'.repeat(64),
    calibration_context_sha256: 'd'.repeat(64),
    provenance_assertions: [
      {
        kind: 'publication-record',
        state: 'verified',
        reference_sha256: 'e'.repeat(64),
        dangerous_note: 'TOP_SECRET_CONTEXT'
      }
    ],
    private_path: '/another/private/path',
    hidden_prompt: 'DO_NOT_PERSIST_ME'
  }
}

test('capsule is deterministic and excludes unapproved source/context fields', () => {
  const profile = fixtureProfile()
  const context = fixtureContext()
  const left = buildEvidenceCapsule(profile, context)
  const right = buildEvidenceCapsule(
    { ...profile, metrics: { char_count: 240, word_count: 42 } },
    { ...context }
  )

  assert.equal(left.evidence_sha256, right.evidence_sha256)
  assert.equal(canonicalJson(left), canonicalJson(right))

  const serialized = canonicalJson(left)
  for (const forbidden of [
    'TOP_SECRET_TEXT',
    'TOP_SECRET_CONTEXT',
    'DO_NOT_PERSIST_ME',
    '/private/path',
    '/another/private/path'
  ]) {
    assert.equal(serialized.includes(forbidden), false, `forbidden value leaked: ${forbidden}`)
  }

  assert.equal(left.scientific_boundary.readiness, 'descriptive_only')
  assert.equal(left.scientific_boundary.exact_model_attribution, false)
  assert.equal(left.scientific_boundary.actor_or_commissioner_identification, false)
  assert.equal(left.provenance_assertions[0].kind, 'publication-record')
  assert.equal('dangerous_note' in left.provenance_assertions[0], false)
})

test('verification detects tampering', () => {
  const capsule = buildEvidenceCapsule(fixtureProfile(), fixtureContext())
  assert.deepEqual(verifyEvidenceCapsule(capsule), {
    ok: true,
    evidence_sha256: capsule.evidence_sha256
  })

  const tampered = structuredClone(capsule)
  tampered.metrics.word_count = 43
  const result = verifyEvidenceCapsule(tampered)
  assert.equal(result.ok, false)
  assert.equal(result.reason, 'evidence_sha256 mismatch')
})

test('encrypted intent is represented in the capsule without storing a password', () => {
  const capsule = buildEvidenceCapsule(fixtureProfile(), {
    ...fixtureContext(),
    publication_intent: 'encrypted',
    encryption_password: 'NEVER_STORE_THIS_PASSWORD'
  })
  const serialized = canonicalJson(capsule)
  assert.equal(capsule.publication_intent, 'encrypted')
  assert.equal(serialized.includes('NEVER_STORE_THIS_PASSWORD'), false)
})

test('invalid hashes, commit IDs, assertion kinds, and publication intents are rejected', () => {
  assert.throws(
    () => buildEvidenceCapsule({ ...fixtureProfile(), content_hash: 'bad' }, fixtureContext()),
    /SHA-256/
  )
  assert.throws(
    () => buildEvidenceCapsule(fixtureProfile(), { ...fixtureContext(), cogniprint_commit_sha: 'bad' }),
    /commit ID/
  )
  assert.throws(
    () => buildEvidenceCapsule(fixtureProfile(), {
      ...fixtureContext(),
      provenance_assertions: [{ kind: 'person-identity', state: 'verified' }]
    }),
    /unsupported provenance assertion kind/
  )
  assert.throws(
    () => buildEvidenceCapsule(fixtureProfile(), { ...fixtureContext(), publication_intent: 'auto-public' }),
    /publication_intent/
  )
})
