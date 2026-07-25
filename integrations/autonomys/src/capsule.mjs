import { createHash } from 'node:crypto'

const HASH_RE = /^[0-9a-f]{64}$/i
const CAPSULE_SCHEMA = 'cogniprint-evidence-capsule-v1'
const ALLOWED_ASSERTION_KINDS = new Set([
  'c2pa',
  'tool-log',
  'revision-history',
  'publication-record',
  'operator-declared',
  'other-authenticated-record'
])
const ALLOWED_ASSERTION_STATES = new Set(['verified', 'declared', 'missing', 'conflict'])

function cloneJson(value) {
  return JSON.parse(JSON.stringify(value))
}

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

function cleanString(value, label, { maxLength = 256, required = false } = {}) {
  const normalized = value === undefined || value === null ? '' : String(value).trim()
  if (required && !normalized) throw new TypeError(`${label} is required`)
  if (normalized.length > maxLength) throw new TypeError(`${label} exceeds ${maxLength} characters`)
  return normalized || null
}

function sanitizeAssertions(assertions) {
  if (assertions === undefined || assertions === null) return []
  if (!Array.isArray(assertions)) throw new TypeError('provenance_assertions must be an array')

  return assertions.map((assertion, index) => {
    if (!assertion || typeof assertion !== 'object' || Array.isArray(assertion)) {
      throw new TypeError(`provenance_assertions[${index}] must be an object`)
    }
    const kind = cleanString(assertion.kind, `provenance_assertions[${index}].kind`, { required: true })
    const state = cleanString(assertion.state, `provenance_assertions[${index}].state`, { required: true })
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
  if (!profile.metrics || typeof profile.metrics !== 'object' || Array.isArray(profile.metrics)) {
    throw new TypeError('CogniPrint profile is missing metrics')
  }
  if (!profile.fingerprint || typeof profile.fingerprint !== 'object' || Array.isArray(profile.fingerprint)) {
    throw new TypeError('CogniPrint profile is missing fingerprint')
  }
  if (!Array.isArray(profile.fingerprint_vector)) {
    throw new TypeError('CogniPrint profile is missing fingerprint_vector')
  }

  const publicationIntent = cleanString(context.publication_intent, 'publication_intent') || 'public-audit'
  if (!['public-audit', 'encrypted'].includes(publicationIntent)) {
    throw new TypeError('publication_intent must be public-audit or encrypted')
  }

  const body = {
    schema: CAPSULE_SCHEMA,
    publication_intent: publicationIntent,
    source_content_sha256: requireSha256(profile.content_hash, 'content_hash'),
    fingerprint_version: cleanString(profile.fingerprint_version, 'fingerprint_version', { required: true }),
    metrics: cloneJson(profile.metrics),
    fingerprint: cloneJson(profile.fingerprint),
    fingerprint_vector: profile.fingerprint_vector.map(Number),
    normalization: profile.normalization && typeof profile.normalization === 'object'
      ? cloneJson(profile.normalization)
      : null,
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
      cogniprint_commit_sha: optionalSha256(context.cogniprint_commit_sha, 'cogniprint_commit_sha'),
      experiment_id: cleanString(context.experiment_id, 'experiment_id'),
      dataset_id: cleanString(context.dataset_id, 'dataset_id'),
      dataset_revision: cleanString(context.dataset_revision, 'dataset_revision'),
      configuration_sha256: optionalSha256(context.configuration_sha256, 'configuration_sha256'),
      calibration_context_sha256: optionalSha256(
        context.calibration_context_sha256,
        'calibration_context_sha256'
      )
    },
    provenance_assertions: sanitizeAssertions(context.provenance_assertions),
    disclaimer: cleanString(
      profile.disclaimer,
      'disclaimer',
      { maxLength: 1024 }
    ) || 'CogniPrint outputs are descriptive research measurements, not identity, source, model, legal, or forensic conclusions.'
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
