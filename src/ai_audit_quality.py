"""Post-hoc response quality checks, distinct from the frozen schema parser.

These checks were added after observing template echoes. They do not change
stored parser outcomes or recover a verdict from malformed text.
"""
from ai_semantic_audit import DIMENSIONS
import re

TEMPLATE_VALUES = {
    'specific scope comparison', 'specific type comparison',
    'specific hypothesis comparison', 'conclusion comparison',
    'same, stronger, weaker, or ambiguous with reason',
    'specific zero/endpoint/sign check',
    'specific candidate example or no found counterexample',
    'brief overall reason',
}


def quality_flags(judgment):
    if judgment is None:
        return ['Frozen schema parse failed; no accepted judgment.']
    flags=['Prompt placeholder copied into '+k+'.' for k in (*DIMENSIONS,'explanation')
           if judgment[k].strip().lower() in TEMPLATE_VALUES]
    if judgment['label']=='faithful' and judgment['issues']:
        flags.append('Faithful label accompanies nonempty issues; consistency requires adjudication.')
    return flags


def exact_duplicate_groups(records):
    """Conservative exact duplicates, not a proof of family independence."""
    signatures={};groups=[]
    for record in records:
        match=re.search(r'\btheorem\s+\S+\s+(.*)',record['expected_lean_statement'],re.S)
        if match is None:raise ValueError('Missing theorem declaration')
        key=(' '.join(record['nl_statement'].lower().split()),' '.join(match[1].split()))
        signatures.setdefault(key,[]).append(record['id'])
    return [ids for ids in signatures.values() if len(ids)>1]
