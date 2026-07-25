#!/usr/bin/env node

import fs from 'node:fs/promises'
import process from 'node:process'

import { verifyEvidenceCapsule } from './capsule.mjs'

const capsulePath = process.argv[2]
if (!capsulePath) {
  console.error('Usage: node src/verify.mjs <capsule.json>')
  process.exit(2)
}

const capsule = JSON.parse(await fs.readFile(capsulePath, 'utf8'))
const result = verifyEvidenceCapsule(capsule)
console.log(JSON.stringify(result, null, 2))
process.exit(result.ok ? 0 : 1)
