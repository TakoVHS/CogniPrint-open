#!/usr/bin/env node

import fs from 'node:fs/promises'
import process from 'node:process'

import { buildEvidenceCapsule, canonicalJson } from './capsule.mjs'

const [profilePath, contextPath, outputPath] = process.argv.slice(2)

if (!profilePath || !outputPath) {
  console.error('Usage: node src/build.mjs <cogniprint-profile.json> [context.json] <capsule.json>')
  console.error('Examples:')
  console.error('  node src/build.mjs profile.json capsule.json')
  console.error('  node src/build.mjs profile.json context.json capsule.json')
  process.exit(2)
}

let actualContextPath = contextPath
let actualOutputPath = outputPath
if (!outputPath) {
  actualOutputPath = contextPath
  actualContextPath = null
}

const profile = JSON.parse(await fs.readFile(profilePath, 'utf8'))
const context = actualContextPath
  ? JSON.parse(await fs.readFile(actualContextPath, 'utf8'))
  : {}

const capsule = buildEvidenceCapsule(profile, context)
await fs.writeFile(actualOutputPath, canonicalJson(capsule) + '\n', 'utf8')

console.log(JSON.stringify({
  output: actualOutputPath,
  schema: capsule.schema,
  publication_intent: capsule.publication_intent,
  evidence_sha256: capsule.evidence_sha256
}, null, 2))
