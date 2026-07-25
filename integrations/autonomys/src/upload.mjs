#!/usr/bin/env node

import fs from 'node:fs/promises'
import process from 'node:process'

import { createAutoDriveApi } from '@autonomys/auto-drive'
import { NetworkId } from '@autonomys/auto-utils'

import { canonicalJson, verifyEvidenceCapsule } from './capsule.mjs'

const capsulePath = process.argv[2]
const receiptPath = process.argv[3] || null

if (!capsulePath) {
  console.error('Usage: node src/upload.mjs <capsule.json> [receipt.json]')
  process.exit(2)
}

const apiKey = process.env.AUTO_DRIVE_API_KEY
if (!apiKey) {
  throw new Error('AUTO_DRIVE_API_KEY is required at runtime and must not be committed')
}

const capsule = JSON.parse(await fs.readFile(capsulePath, 'utf8'))
const verification = verifyEvidenceCapsule(capsule)
if (!verification.ok) {
  throw new Error(`Refusing upload: capsule verification failed: ${verification.reason}`)
}

const password = process.env.AUTO_DRIVE_ENCRYPTION_PASSWORD || null
if (capsule.publication_intent === 'encrypted' && !password) {
  throw new Error('Encrypted capsule requires AUTO_DRIVE_ENCRYPTION_PASSWORD at runtime')
}
if (capsule.publication_intent === 'public-audit' && password) {
  throw new Error('Refusing ambiguous mode: public-audit capsule must not use AUTO_DRIVE_ENCRYPTION_PASSWORD')
}

const api = createAutoDriveApi({
  apiKey,
  network: NetworkId.MAINNET
})

const payload = Buffer.from(canonicalJson(capsule) + '\n', 'utf8')
const fileName = `cogniprint-evidence-${capsule.evidence_sha256}.json`
const options = {
  compression: true,
  ...(password ? { password } : {})
}

const cid = await api.uploadFileFromBuffer(payload, fileName, options)
const receipt = {
  schema: 'cogniprint-auto-drive-receipt-v1',
  cid: String(cid),
  evidence_sha256: capsule.evidence_sha256,
  publication_intent: capsule.publication_intent,
  encrypted: Boolean(password),
  network: 'mainnet',
  sdk_package: '@autonomys/auto-drive',
  sdk_version: '1.6.14',
  public_url_created: false,
  note: 'Upload does not call publishObject(); no public download URL is created by this command.'
}

if (receiptPath) {
  await fs.writeFile(receiptPath, JSON.stringify(receipt, null, 2) + '\n', 'utf8')
}
console.log(JSON.stringify(receipt, null, 2))
