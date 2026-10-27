"""Offline readiness evidence; never freezes data or invokes a model API."""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from dataset_validation import validate_curation_draft, validate_frozen_curation
from repair_experiment import _protocol_metadata, _prompt_hashes


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(output: Path) -> dict:
    # Refuse replacement of any prior research evidence.
    output.mkdir(parents=True, exist_ok=False)
    sources = [ROOT / 'data/research_dataset_draft_v0.1.0.json']
    sources += sorted((ROOT / 'data/curation_batches').glob('*/candidate_records.json'))
    records = [record for path in sources for record in json.loads(path.read_text())]
    report = validate_curation_draft(records)
    splits = {split: [r for r in records if r['curation']['split'] == split]
              for split in ('development', 'test')}
    hashes = {}
    for split, rows in splits.items():
        path = output / f'{split}_candidates.json'
        path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
        hashes[split] = digest(path)
    # Validate the actual draft manifest, retaining all expected rejection reasons.
    frozen = validate_frozen_curation(
        splits['test'], json.loads((ROOT / 'data/research_dataset_manifest_v0.1.0.json').read_text()),
        hashes['test'], development_value=splits['development'],
        development_dataset_sha256=hashes['development'])
    queue = []
    packet_dir = output / 'review_packets'
    packet_dir.mkdir()
    template = json.loads((ROOT / 'data/review_templates/research_candidate_review_template_v0.1.0.json').read_text())
    for record in records:
        single = validate_curation_draft([record])
        verification = record['curation'].get('theorem_verification') or {}
        packet = packet_dir / f"{record['id']}.json"
        review = copy.deepcopy(template)
        review['candidate_id'] = record['id']
        review['candidate_record'] = record
        review['candidate_record_sha256'] = hashlib.sha256(
            json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
        ).hexdigest()
        review['allowed_semantic_labels'] = ['faithful', 'not faithful', 'uncertain']
        review['reviewer_instructions'] = (
            'Compare English and Lean quantifiers, domains, assumptions, boundary cases, '
            'and conclusion. Inspect imports and definitions, category, difficulty, source '
            'rights, family, split and duplicates. Keep actual reviewer identity, date, '
            'decisions and evidence pending until independent human review.'
        )
        packet.write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
        queue.append({
            'id': record['id'], 'category': record['category'],
            'proposed_split': record['curation']['split'],
            'family': record['curation']['problem_family'],
            'statement_sha256': hashlib.sha256(record['expected_lean_statement'].encode()).hexdigest(),
            'review_packet': str(packet),
            'review_packet_sha256': digest(packet),
            'verification_scope': verification.get('verification_scope', 'legacy_unspecified'),
            'blockers': list(single.errors) + list(single.review_warnings),
        })
    result = {
        'status': 'BLOCKED', 'purpose': 'readiness_only_not_experiment_results',
        'candidate_count': len(records), 'curation_validation': asdict(report),
        'frozen_validation': asdict(frozen), 'protocol': _protocol_metadata(),
        'prompt_sha256': _prompt_hashes(),
        'input_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sources},
        'review_queue': queue,
        'api_calls': 0, 'dataset_frozen': False,
    }
    (output / 'readiness.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'candidate_count': len(records), 'eligible': report.eligible_split_counts,
                      'structural_errors': len(report.errors), 'warnings': len(report.review_warnings),
                      'freeze_errors': len(frozen.errors), 'output': str(output)}, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    prepare(parser.parse_args().output_dir)
