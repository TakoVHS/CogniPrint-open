from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cogniprint.benchmarks.raid import stable_selection_key


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / 'scripts' / 'prepare_raid_pilot.py'
MODELS = ('human', 'chatgpt', 'gpt4', 'llama-chat', 'mistral-chat')
DOMAINS = ('abstracts', 'news', 'reviews', 'wiki')
SEED = 20260725


def build_text(model: str, domain: str, idx: int, *, duplicate_label: str | None = None) -> str:
    base = duplicate_label or f'{model}-{domain}-{idx}'
    return (
        f'{base} benchmark passage for RAID Pilot A. '
        f'This sentence keeps deterministic token and character structure for {model} in {domain}. '
        'The passage is long enough to produce stable fingerprint coordinates for unit testing.'
    )


def make_row(model: str, domain: str, idx: int, *, prompt: str | None = None, text: str | None = None) -> dict[str, str]:
    is_human = model.lower() == 'human'
    return {
        'id': f'{model}-{domain}-{idx}',
        'adv_source_id': f'{model}-{domain}-{idx}',
        'source_id': f'source-{model}-{domain}-{idx}',
        'model': model,
        'decoding': '' if is_human else 'sampling',
        'repetition_penalty': '' if is_human else 'no',
        'attack': 'none',
        'domain': domain,
        'title': f'{model} {domain} {idx}',
        'prompt': prompt or f'Prompt for {model} {domain} {idx}',
        'generation': text or build_text(model, domain, idx),
    }


def write_csv(path: Path, rows: list[dict[str, str]], *, fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = ['id', 'adv_source_id', 'source_id', 'model', 'decoding', 'repetition_penalty', 'attack', 'domain', 'title', 'prompt', 'generation']
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_contract(path: Path, source_path: Path) -> str:
    source_sha = sha256_file(source_path)
    payload = {
        'schema': 'cogniprint-raid-source-contract-001',
        'status': 'PINNED',
        'source_name': 'test-source',
        'source_authority': 'https://github.com/liamdugan/raid',
        'landing_url': 'https://github.com/liamdugan/raid',
        'download_url': 'https://dataset.raid-bench.xyz/train_none.csv',
        'final_url': 'https://dataset.raid-bench.xyz/train_none.csv',
        'source_repository_revision': 'test-revision',
        'acquired_at_utc': '2026-07-29T00:00:00Z',
        'byte_size': source_path.stat().st_size,
        'sha256': source_sha,
        'license': 'MIT',
        'raw_source_committed': False,
        'raw_source_in_evidence_bundle': False,
        'intended_use': 'STAGE_A_DEVELOPMENT_ONLY',
        'scientific_claim_evidence': False,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return source_sha


def run_prepare(source_path: Path, contract_path: Path, output_dir: Path, *, models: tuple[str, ...] | None = None, domains: tuple[str, ...] | None = None, per_cell: int = 1, expected_sha: str | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(SCRIPT),
        '--input-file', str(source_path),
        '--expected-source-sha256', expected_sha or sha256_file(source_path),
        '--source-contract', str(contract_path),
        '--per-cell', str(per_cell),
        '--seed', str(SEED),
        '--output-dir', str(output_dir),
    ]
    if models is not None:
        cmd += ['--models', ','.join(models)]
    if domains is not None:
        cmd += ['--domains', ','.join(domains)]
    env = os.environ.copy()
    env['PYTHONPATH'] = f"{REPO_ROOT / 'src'}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)
    return subprocess.run(cmd, cwd=REPO_ROOT, env=env, text=True, capture_output=True)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


class RaidPilotSourceContractTests(unittest.TestCase):
    def test_source_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source_path = tmp / 'source.csv'
            write_csv(source_path, [make_row('human', 'abstracts', 1), make_row('gpt4', 'abstracts', 1)])
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            result = run_prepare(source_path, contract_path, tmp / 'out', models=('human', 'gpt4'), domains=('abstracts',), expected_sha='0' * 64)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('source SHA-256 mismatch', result.stderr + result.stdout)

    def test_missing_required_columns_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source_path = tmp / 'source.csv'
            write_csv(source_path, [make_row('human', 'abstracts', 1)], fieldnames=['id', 'model', 'generation'])
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            result = run_prepare(source_path, contract_path, tmp / 'out', models=('human',), domains=('abstracts',))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('missing required CSV columns', result.stderr + result.stdout)

    def test_malformed_csv_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source_path = tmp / 'source.csv'
            source_path.write_text(
                'id,adv_source_id,source_id,model,decoding,repetition_penalty,attack,domain,title,prompt,generation\n'
                '1,1,1,human,,,none,abstracts,title,"broken,generation\n',
                encoding='utf-8',
            )
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            result = run_prepare(source_path, contract_path, tmp / 'out', models=('human',), domains=('abstracts',))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('malformed CSV', result.stderr + result.stdout)

    def test_local_csv_source_mode_writes_metadata_only_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            rows = [
                make_row('human', 'abstracts', 1),
                make_row('human', 'wiki', 1),
                make_row('gpt4', 'abstracts', 1),
                make_row('gpt4', 'wiki', 1),
            ]
            source_path = tmp / 'source.csv'
            write_csv(source_path, rows)
            contract_path = tmp / 'contract.json'
            source_sha = write_contract(contract_path, source_path)
            output_dir = tmp / 'out'
            result = run_prepare(source_path, contract_path, output_dir, models=('human', 'gpt4'), domains=('abstracts', 'wiki'))
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            features = read_jsonl(output_dir / 'features.jsonl')
            summary = json.loads((output_dir / 'summary.json').read_text(encoding='utf-8'))
            self.assertEqual(len(features), 4)
            self.assertEqual(summary['record_count'], 4)
            self.assertEqual(summary['source_sha256'], source_sha)
            self.assertEqual(summary['source_contract_sha256'], sha256_file(contract_path))
            for record in features:
                self.assertNotIn('generation', record)
                self.assertNotIn('prompt', record)
                self.assertEqual(record['source_sha256'], source_sha)
                self.assertEqual(record['source_contract_sha256'], sha256_file(contract_path))

    def test_domain_and_model_mapping_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            rows = [
                make_row('human', 'wiki', 1),
                make_row('GPT-4', 'Wikipedia', 1),
            ]
            source_path = tmp / 'source.csv'
            write_csv(source_path, rows)
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            output_dir = tmp / 'out'
            result = run_prepare(source_path, contract_path, output_dir, models=('human', 'gpt4'), domains=('wiki',))
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            features = read_jsonl(output_dir / 'features.jsonl')
            labels = {(record['model_family'], record['domain']) for record in features}
            self.assertIn(('gpt4', 'wiki'), labels)

    def test_insufficient_cell_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            rows = [make_row('human', 'abstracts', 1)]
            source_path = tmp / 'source.csv'
            write_csv(source_path, rows)
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            result = run_prepare(source_path, contract_path, tmp / 'out', models=('human', 'gpt4'), domains=('abstracts',), per_cell=1)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('missing counts', result.stderr + result.stdout)

    def test_duplicate_replacement_keeps_unique_text_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            duplicate_text = build_text('duplicate', 'abstracts', 1, duplicate_label='same-text')
            human = make_row('human', 'abstracts', 1, text=duplicate_text)
            gpt_dup = make_row('gpt4', 'abstracts', 1, text=duplicate_text)
            gpt_unique = make_row('gpt4', 'abstracts', 2)
            while stable_selection_key(gpt_dup, SEED) > stable_selection_key(gpt_unique, SEED):
                gpt_dup = make_row('gpt4', 'abstracts', int(gpt_dup['id'].split('-')[-1]) + 10, text=duplicate_text)
            rows = [human, gpt_dup, gpt_unique]
            source_path = tmp / 'source.csv'
            write_csv(source_path, rows)
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            output_dir = tmp / 'out'
            result = run_prepare(source_path, contract_path, output_dir, models=('human', 'gpt4'), domains=('abstracts',), per_cell=1)
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            duplicate_audit = json.loads((output_dir / 'duplicate-lineage-audit.json').read_text(encoding='utf-8'))
            self.assertEqual(duplicate_audit['unique_text_hashes'], 2)
            self.assertEqual(duplicate_audit['replacement_count'], 1)

    def test_balanced_twenty_cell_quota_with_per_cell_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            rows = []
            for model in MODELS:
                for domain in DOMAINS:
                    rows.append(make_row(model, domain, 1))
            source_path = tmp / 'source.csv'
            write_csv(source_path, rows)
            contract_path = tmp / 'contract.json'
            write_contract(contract_path, source_path)
            output_dir = tmp / 'out'
            result = run_prepare(source_path, contract_path, output_dir, per_cell=1)
            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            summary = json.loads((output_dir / 'summary.json').read_text(encoding='utf-8'))
            self.assertEqual(summary['record_count'], 20)
            self.assertEqual(len(summary['cell_counts']), 20)
            self.assertTrue(all(count == 1 for count in summary['cell_counts'].values()))


if __name__ == '__main__':
    unittest.main()
