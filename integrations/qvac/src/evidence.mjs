const HASH_RE = /^[0-9a-f]{64}$/i

export function sanitizeCogniPrintProfile(payload) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    throw new TypeError('CogniPrint profile must be a JSON object')
  }

  const contentHash = String(payload.content_hash || '')
  if (!HASH_RE.test(contentHash)) {
    throw new TypeError('CogniPrint profile is missing a valid SHA-256 content_hash')
  }
  if (!payload.metrics || typeof payload.metrics !== 'object' || Array.isArray(payload.metrics)) {
    throw new TypeError('CogniPrint profile is missing metrics')
  }
  if (!payload.fingerprint || typeof payload.fingerprint !== 'object' || Array.isArray(payload.fingerprint)) {
    throw new TypeError('CogniPrint profile is missing normalized fingerprint coordinates')
  }
  if (!Array.isArray(payload.fingerprint_vector)) {
    throw new TypeError('CogniPrint profile is missing fingerprint_vector')
  }

  return {
    schema: 'cogniprint-local-evidence-v1',
    content_hash: contentHash.toLowerCase(),
    fingerprint_version: String(payload.fingerprint_version || 'unknown'),
    metrics: structuredClone(payload.metrics),
    fingerprint: structuredClone(payload.fingerprint),
    fingerprint_vector: payload.fingerprint_vector.map(Number),
    normalization: payload.normalization && typeof payload.normalization === 'object'
      ? structuredClone(payload.normalization)
      : null,
    disclaimer: String(
      payload.disclaimer ||
        'CogniPrint outputs are descriptive research signals, not authorship, source, model, legal, or forensic conclusions.'
    ),
    claim_boundary: {
      exact_model_attribution: false,
      authorship_identification: false,
      ai_origin_proof: false,
      actor_or_commissioner_identification: false,
      legal_or_forensic_provenance: false
    }
  }
}

export function buildBoundedEvidencePrompt(evidence) {
  const compact = JSON.stringify(evidence)
  return [
    'You are the local-only explanation layer for CogniPrint research evidence.',
    'Use only the supplied evidence JSON. Do not invent provenance or infer facts that are not represented.',
    'Never identify an author, exact neural model, AI origin, commissioning actor, intent, legal status, or forensic provenance.',
    'Explain the measured statistical profile in plain language, mention the content hash and fingerprint version, and state uncertainty explicitly.',
    'If the evidence cannot support a conclusion, say that directly.',
    'Return four short sections: Measured evidence; What it may help compare; What it does not establish; Reproducibility identifiers.',
    '',
    `Evidence JSON: ${compact}`
  ].join('\n')
}
