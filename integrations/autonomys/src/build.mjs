#!/usr/bin/env node

import fs from 'node:fs/promises'
import process from 'node:process'

import { buildEvidenceCapsule, canonicalJson } from './capsule.mjs'

const args = process.argv.slice(2)
if (args.length !== 2 && args.length !== 3) {
  console.error('Usage: node src/build.mjs <cogniprint-profile.json> [context.json] <capsule.json>')
  console.error('Examples:')
  console.error('  node src/build.mjs profile.json capsule.json')
  console.error('  node src/build.mjs profile.json context.json capsule.json')
  process.exit(2)
}

const profilePath = args[0]
const contextPath = args.length === 3 ? args[1] : null
const outputPath = args.length === 3 ? args[2] : args[1]

const profile = JSON.parse(await fs.readFile(profilePath, 'utf8'))
const context = contextPath
  ? JSON.parse(await fs.readFile(contextPath, 'utf8'))
  : {}

const capsule = buildEvidenceCapsule(profile, context)
await fs.writeFile(outputPath, canonicalJson(capsule) + '\n', 'utf8')

console.log(JSON.stringify({
  output: outputPath,
  schema: capsule.schema,
  publication_intent: capsule.publication_intent,
  evidence_sha256: capsule.evidence_sha256
}, null, 2))
