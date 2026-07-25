import { createHash } from 'node:crypto'

const HASH_RE = /^[0-9a-f]{64}$/i
const GIT_COMMIT_RE = /^[0-9a-f]{40}([0-9a-f]{24})?$/i
const SAFE_NUMERIC_KEY_RE = /^[a-z][a-z0-9_]{0,63}$/i
const SAFE_IDENTIFIER_RE = /^[a-z0-9][a-z0-9._:/@+-]{0,127}$/i
const SAFE_VERSION_RE = /^[a-z0-9][a-z0-9._-]{0,79}$/i
const CAPSULE_SCHEMA = 'cogniprint-evidence-capsule-v1'
const CAPSULE_DISCLAIMER = 'CogniPrint outputs are descriptive research measurements, not identity, source, model, legal, or forensic conclusions.'
const ALLOWED_ASSERTION_KINDS = new Set([
  'c2pa',
  'tool-log',
  'revision-history',
  'publication-record',
  'operator-declared',
  'other-authenticated-record'
])
const ALLOWED_ASSERTION_STATES = new Set(['verified', 'declared', 'missing', 'conflict'])

function requireSha256(value, label) {
  const normalized = String(value || '').toLowerCase()
  if (!HASH_RE.test(normalized)) {
    throw new TypeError(`${label} must be a 64-character SHA-256 hex string`)
  }
  return normalized
}

function optionalSha256(value, label) {
  if (value === undefined || value === null || value === '') return null
  return requireSha256(value, label)
}

function optionalGitCommit(value, label) {
  if (value === undefined || value === null || value === '') return null
  const normalized = String(value).toLowerCase()
  if (!GIT_COMMIT_RE.test(normalized)) {
    throw new TypeError(`${label} must be a 40- or 64-character hexadecimal commit ID`)
  }
  return normalized
}

function safeIdentifier(value, label, { required = false } = {}) {
  if (value === undefined || value === null || value === '') {
    if (required) throw new TypeError(`${label} is required`)
    return null
  }
  const normalized = String(value).trim()
  if (!SAFE_IDENTIFIER_RE.test(normalized)) {
    throw new TypeError(`${label} contains unsupported characters or exceeds 128 characters`)
  }
  return normalized
}

function safeVersion(value, label) {
  const normalized = String(value || '').trim()
  if (!SAFE_VERSION_RE.test(normalized)) {
    throw new TypeError(`${label} must be a safe version identifier`)
  }
  return normalized
}

function sanitizeNumericMap(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object of finite numeric values`)
  }
  const entries = Object.entries(value)
  if (!entries.length) throw new TypeError(`${label} must not be empty`)

  return Object.fromEntries(entries.map(([key, item]) => {
    if (!SAFE_NUMERIC_KEY_RE.test(key)) {
      throw new TypeError(`${label} contains an unsupported key: ${key}`)
    }
    if (typeof item !== 'number' || !Number.isFinite(item)) {
      throw new TypeError(`${label}.${key} must be a finite number`)
    }
    return [key, item]
  }))
}

function sanitizeNumericVector(value, label) {
  if (!Array.isArray(value) || !value.length) {
    throw new TypeError(`${label} must be a non-empty numeric array`)
  }
  return value.map((item, index) => {
    if (typeof item !== 'number' || !Number.isFinite(item)) {
      throw new TypeError(`${label}[${index}] must be a finite number`)
    }
    return item
  })
}

function sanitizeNormalization(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError('normalization must be an object')
  }
  if (value.method !== 'bounded_minmax_v1') {
    throw new TypeError('unsupported normalization.method')
  }
  if (value.bounds_source !== 'cogniprint.fingerprint.FEATURE_SPECS') {
    throw new TypeError('unsupported normalization.bounds_source')
  }
  if (typeof value.clip !== 'boolean') {
    throw new TypeError('normalization.clip must be boolean')
  }
  return {
    method: value.method,
    bounds_source: value.bounds_source,
    clip: value.clip
  }
}

function sanitizeAssertions(assertions) {
  if (assertions === undefined || assertions === null) return []
  if (!Array.isArray(assertions)) throw new TypeError('provenance_assertions must be an array')

  return assertions.map((assertion, index) => {
    if (!assertion || typeof assertion !== 'object' || Array.isArray(assertion)) {
      throw new TypeError(`provenance_assertions[${index}] must be an object`)
    }
    const kind = safeIdentifier(assertion.kind, `provenance_assertions[${index}].kind`, { required: true })
    const state = safeIdentifier(assertion.state, `provenance_assertions[${index}].state`, { required: true })
    if (!ALLOWED_ASSERTION_KINDS.has(kind)) {
      throw new TypeError(`unsupported provenance assertion kind: ${kind}`)
    }
    if (!ALLOWED_ASSERTION_STATES.has(state)) {
      throw new TypeError(`unsupported provenance assertion state: ${state}`)
    }

    return {
      kind,
      state,
      reference_sha256: optionalSha256(
        assertion.reference_sha256,
        `provenance_assertions[${index}].reference_sha256`
      )
    }
  })
}

function sortJson(value) {
  if (Array.isArray(value)) return value.map(sortJson)
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortJson(value[key])])
    )
  }
  return value
}

export function canonicalJson(value) {
  return JSON.stringify(sortJson(value))
}

export function sha256Canonical(value) {
  return createHash('sha256').update(canonicalJson(value), 'utf8').digest('hex')
}

export function buildEvidenceCapsule(profile, context = {}) {
  if (!profile || typeof profile !== 'object' || Array.isArray(profile)) {
    throw new TypeError('CogniPrint profile must be a JSON object')
  }

  const publicationIntent = safeIdentifier(context.publication_intent, 'publication_intent') || 'public-audit'
  if (!['public-audit', 'encrypted'].includes(publicationIntent)) {
    throw new TypeError('publication_intent must be public-audit or encrypted')
  }

  const body = {
    schema: CAPSULE_SCHEMA,
    publication_intent: publicationIntent,
    source_content_sha256: requireSha256(profile.content_hash, 'content_hash'),
    fingerprint_version: safeVersion(profile.fingerprint_version, 'fingerprint_version'),
    metrics: sanitizeNumericMap(profile.metrics, 'metrics'),
    fingerprint: sanitizeNumericMap(profile.fingerprint, 'fingerprint'),
    fingerprint_vector: sanitizeNumericVector(profile.fingerprint_vector, 'fingerprint_vector'),
    normalization: sanitizeNormalization(profile.normalization),
    scientific_boundary: {
      readiness: 'descriptive_only',
      exact_model_attribution: false,
      authorship_identification: false,
      definitive_ai_origin: false,
      actor_or_commissioner_identification: false,
      intent_or_responsibility: false,
      legal_or_forensic_provenance: false
    },
    reproducibility: {
      cogniprint_commit_sha: optionalGitCommit(context.cogniprint_commit_sha, 'cogniprint_commit_sha'),
      experiment_id: safeIdentifier(context.experiment_id, 'experiment_id'),
      dataset_id: safeIdentifier(context.dataset_id, 'dataset_id'),
      dataset_revision: safeIdentifier(context.dataset_revision, 'dataset_revision'),
      configuration_sha256: optionalSha256(context.configuration_sha256, 'configuration_sha256'),
      calibration_context_sha256: optionalSha256(
        context.calibration_context_sha256,
        'calibration_context_sha256'
      )
    },
    provenance_assertions: sanitizeAssertions(context.provenance_assertions),
    disclaimer: CAPSULE_DISCLAIMER
  }

  const evidenceSha256 = sha256Canonical(body)
  return {
    ...body,
    evidence_sha256: evidenceSha256
  }
}

export function verifyEvidenceCapsule(capsule) {
  if (!capsule || typeof capsule !== 'object' || Array.isArray(capsule)) {
    return { ok: false, reason: 'capsule must be an object' }
  }
  if (capsule.schema !== CAPSULE_SCHEMA) {
    return { ok: false, reason: `unexpected schema: ${capsule.schema}` }
  }
  if (!HASH_RE.test(String(capsule.evidence_sha256 || ''))) {
    return { ok: false, reason: 'missing or malformed evidence_sha256' }
  }

  const { evidence_sha256: claimed, ...body } = capsule
  const computed = sha256Canonical(body)
  if (computed !== claimed.toLowerCase()) {
    return { ok: false, reason: 'evidence_sha256 mismatch', claimed, computed }
  }

  return { ok: true, evidence_sha256: computed }
}
