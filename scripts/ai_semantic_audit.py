"""Prepare/run a separate local reviewer. Never invokes the study runner/gates."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ai_semantic_audit import digest, subject, parse_judgment
from candidate_inventory import load_candidates
from local_llm_client import LocalMLXClient

TEMPLATE = ROOT / 'prompts/ai_semantic_audit_v1.txt'
MODEL = ROOT / 'data/ai_semantic_audit/20261028/model'


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()


def append(path, value):
    with path.open('a') as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + '\n')
        stream.flush(); os.fsync(stream.fileno())


def prepare(output):
    output.mkdir(parents=True, exist_ok=False)
    rows = load_candidates(ROOT)
    (output / 'subjects.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    prompts = output / 'prompts'; prompts.mkdir()
    for r in rows:
        text = TEMPLATE.read_text().replace('{{subject_json}}', json.dumps(subject(r), ensure_ascii=False, indent=2))
        (prompts / (r['id'] + '.txt')).write_text(text)
    selection = json.loads((MODEL / 'selection.json').read_text())
    manifest = {'kind': 'ai_semantic_audit_not_experiment', 'prepared_at': now(),
        'reviewer_kind': 'ai_only_not_independent_human', 'candidate_count': len(rows),
        'selection': selection, 'subjects_sha256': sha(output / 'subjects.json'),
        'subject_bindings': {r['id']: digest(subject(r)) for r in rows},
        'prompt_sha256': {r['id']: sha(prompts / (r['id'] + '.txt')) for r in rows},
        'inventory_sha256': sha(MODEL / 'inventory.json'),
        'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in [Path(__file__).resolve(), ROOT / 'src/ai_semantic_audit.py', ROOT / 'src/local_llm_client.py', TEMPLATE]},
        'settings': {'seed': 284729, 'temperature': 0.0, 'top_p': 1.0,
                     'max_completion_tokens': 900, 'max_context_tokens': 8192},
        'execution_order': 'stored dataset order; one independent conversation per candidate',
        'visibility': 'English, theorem type, imports and explicit custom definitions only; no reference proofs, previous labels or split assignments',
        'paid_inference_requests': 0, 'study_gate_changes': False,
        'limitations': ['Different model family does not establish statistically independent errors.',
            'Single deterministic pass; model output is fallible and not ground truth.',
            'All 96 candidate texts accessed for authorized curation, not repair/prompt tuning. Future split approval must disclose this exposure.',
            'No human review or local-study substitution approval is inferred.']}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared', len(rows), 'AI-only subjects; existing curation remains unchanged.')


def run(output):
    m = json.loads((output / 'manifest.json').read_text())
    for name, expected in m['source_sha256'].items():
        if sha(ROOT / name) != expected: raise ValueError('Audit implementation changed: ' + name)
    if sha(output / 'subjects.json') != m['subjects_sha256'] or sha(MODEL / 'inventory.json') != m['inventory_sha256']:
        raise ValueError('Audit inputs changed')
    rows = json.loads((output / 'subjects.json').read_text())
    journal = output / 'journal.jsonl'
    events = [json.loads(s) for s in journal.read_text().splitlines()] if journal.exists() else []
    # Every prior intent consumes its context, including crashes/interruption.
    consumed = {e['candidate_id'] for e in events if e['event'] == 'intent'}
    snapshot = Path((MODEL / 'local_snapshot_path.txt').read_text().strip())
    client = LocalMLXClient(snapshot, json.loads((MODEL / 'inventory.json').read_text()),
        model_id=m['selection']['review_model'], seed=m['settings']['seed'], max_context_tokens=8192)
    traces = output / 'streams'; traces.mkdir(exist_ok=True); client.trace_directory = traces
    responses = output / 'responses'; responses.mkdir(exist_ok=True)
    for i, r in enumerate(rows, 1):
        ident = r['id']
        if ident in consumed: continue
        prompt_path = output / 'prompts' / (ident + '.txt')
        if sha(prompt_path) != m['prompt_sha256'][ident]: raise ValueError('Prompt changed')
        target = responses / (ident + '.json')
        if target.exists(): raise ValueError('Unjournaled existing response')
        context = 'ai-audit-v1/' + ident
        append(journal, {'event': 'intent', 'at': now(), 'candidate_id': ident,
                         'context': context, 'prompt_sha256': sha(prompt_path)})
        started = time.monotonic()
        try:
            result = client(prompt_path.read_text(), max_tokens=900, temperature=0.0,
                            generation_context=context)
            row = {'candidate_id': ident, 'reviewer_kind': 'ai_only_not_independent_human',
                   'subject_sha256': m['subject_bindings'][ident], 'at': now(),
                   'raw_response': result.content, 'metadata': result.metadata,
                   'judgment': None, 'parse_error': None}
            try: row['judgment'] = parse_judgment(result.content)
            except (ValueError, TypeError) as e: row['parse_error'] = str(e)
            with target.open('x') as stream:
                json.dump(row, stream, ensure_ascii=False, indent=2); stream.write('\n')
                stream.flush(); os.fsync(stream.fileno())
            append(journal, {'event': 'completed', 'at': now(), 'candidate_id': ident,
                             'response_sha256': sha(target), 'parsed': row['judgment'] is not None})
            label = row['judgment']['label'] if row['judgment'] else 'unparseable'
            print(f'{i}/{len(rows)} {ident}: {label}; {time.monotonic()-started:.1f}s', flush=True)
        except BaseException as e:
            append(journal, {'event': 'interrupted', 'at': now(), 'candidate_id': ident, 'error_type': type(e).__name__})
            raise


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'run']); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); (prepare if a.action == 'prepare' else run)(a.output)
