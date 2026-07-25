#!/usr/bin/env node

import fs from 'node:fs/promises'
import process from 'node:process'
import {
  QWEN3_600M_INST_Q4,
  completion,
  loadModel,
  unloadModel
} from '@qvac/sdk'

import { buildBoundedEvidencePrompt, sanitizeCogniPrintProfile } from './evidence.mjs'

const profilePath = process.argv[2]
const outputPath = process.argv[3]

if (!profilePath) {
  console.error('Usage: node src/explain.mjs <cogniprint-profile.json> [output.md]')
  process.exit(2)
}

const raw = await fs.readFile(profilePath, 'utf8')
const profile = JSON.parse(raw)
const evidence = sanitizeCogniPrintProfile(profile)
const prompt = buildBoundedEvidencePrompt(evidence)

let modelId
try {
  modelId = await loadModel({
    modelSrc: QWEN3_600M_INST_Q4,
    modelConfig: { ctx_size: 4096 }
  })

  const result = completion({
    modelId,
    history: [{ role: 'user', content: prompt }],
    stream: true
  })

  let explanation = ''
  for await (const token of result.tokenStream) {
    explanation += token
    if (!outputPath) process.stdout.write(token)
  }
  if (!outputPath) process.stdout.write('\n')

  if (outputPath) {
    await fs.writeFile(outputPath, explanation.trimEnd() + '\n', 'utf8')
    console.error(`Local QVAC explanation written: ${outputPath}`)
  }
} finally {
  if (modelId) await unloadModel({ modelId })
}
