"""AI-only semantic review artifacts. This module never grants eligibility."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re

DIMENSIONS = ('quantifiers', 'domains', 'assumptions', 'equivalence', 'strength',
              'boundary_cases', 'counterexample_search')
LABELS = ('faithful', 'not faithful', 'uncertain')


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def subject(record: dict) -> dict:
    # No reference proof, expected label, split or earlier verdict: reduce anchoring.
    return {k: record.get(k) for k in ('id', 'nl_statement', 'expected_lean_statement',
                                      'required_imports', 'required_definitions')}


def parse_judgment(text: str) -> dict:
    """Reject malformed/truncated/ambiguous judgments; never infer a pass."""
    cleaned = text.strip()
    if cleaned.startswith('```'):
        match = re.fullmatch(r'```(?:json)?\s*(.*?)\s*```', cleaned, re.S)
        if not match:
            raise ValueError('Unclosed JSON fence')
        cleaned = match[1]
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError('Duplicate judgment key')
            result[k] = v
        return result
    result = json.loads(cleaned, object_pairs_hook=unique)
    if not isinstance(result, dict) or result.get('label') not in LABELS:
        raise ValueError('Missing/invalid semantic label')
    for field in (*DIMENSIONS, 'explanation'):
        if not isinstance(result.get(field), str) or not result[field].strip():
            raise ValueError('Missing substantive field: ' + field)
    if not isinstance(result.get('issues'), list) or any(not isinstance(x, str) for x in result['issues']):
        raise ValueError('issues must be a string list')
    return result


def proposed_record(record: dict, audit: dict) -> dict:
    """Preserve curation bytes/decisions and attach AI findings outside curation."""
    if audit['candidate_id'] != record['id'] or audit['subject_sha256'] != digest(subject(record)):
        raise ValueError('Audit is bound to a different subject')
    result = copy.deepcopy(record)
    result['ai_semantic_audit'] = copy.deepcopy(audit)
    result['ai_semantic_audit']['reviewer_kind'] = 'ai_only_not_independent_human'
    result['ai_semantic_audit']['grants_eligibility'] = False
    return result


def assert_unchanged_curation(original: list[dict], proposed: list[dict]) -> None:
    if len(original) != len(proposed) or len({r['id'] for r in proposed}) != len(original):
        raise ValueError('Candidate inventory changed')
    originals = {r['id']: r for r in original}
    for row in proposed:
        if row['id'] not in originals:
            raise ValueError('Unknown candidate')
        recovered = copy.deepcopy(row)
        recovered.pop('ai_semantic_audit', None)
        if recovered != originals[row['id']]:
            raise ValueError('AI audit modified existing fields')
