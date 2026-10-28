"""Fresh strict reference checks plus explicit type comparisons, without placeholders."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from candidate_inventory import load_candidates
from verify import _run_compiler, _diagnostics, _axioms_from_diagnostics, _find_prohibited_source, DEFAULT_POLICY


def build(output):
    output.mkdir(parents=True, exist_ok=False)
    records = load_candidates(ROOT)
    sources = [ROOT / 'data/reference_verification/v0.1.0/references.lean',
               ROOT / 'data/reference_verification/v0.2.0/references_module.lean']
    sources += [p for p in sorted((ROOT / 'data/curation_batches').glob('v0.1*/*.lean'))
                if p.name != 'statement_check.lean']
    sources += [ROOT / f'data/curation_batches/{v}/references_expanded.lean' for v in ['v0.2.0', 'v0.2.1']]
    chunks = ['import Mathlib\nimport Nl2Lean.CandidateDefinitions\nopen scoped BigOperators\n']
    declarations = {}
    for i, path in enumerate(sources):
        code = path.read_text()
        if _find_prohibited_source(code, False, DEFAULT_POLICY): raise ValueError('Unsafe reference source')
        names = re.findall(r'(?m)^theorem\s+(\S+)', code)
        prefix = f'AuditReference{i}.' + ('AdditionalReferences.' if 'namespace AdditionalReferences' in code else '')
        if any(name in declarations for name in names): raise ValueError('Duplicate theorem name')
        for name in names: declarations[name] = (prefix + name, str(path.relative_to(ROOT)))
        code = re.sub(r'(?m)^import [^\n]+\n?', '', code)
        chunks.append(f'namespace AuditReference{i}\n{code}\nend AuditReference{i}\n')
    comparisons = []
    for r in records:
        statement = r['expected_lean_statement'].split('theorem ', 1)[1]
        name, signature = statement.split(None, 1)
        fullname, origin = declarations[name]
        # Locate the result colon at binder depth zero, not a binder type colon.
        depth = 0; split = None
        for i, c in enumerate(signature):
            if c in '([{': depth += 1
            elif c in ')]}': depth -= 1
            elif c == ':' and depth == 0: split = i; break
        if split is None: raise ValueError('No result type')
        binders, conclusion = signature[:split].strip(), signature[split+1:].strip()
        expected = ('∀ ' + binders + ', ' if binders else '') + conclusion
        chunks.append(f'-- Exact type comparison: {r["id"]}\nexample : {expected} := @{fullname}\n#print axioms {fullname}\n')
        comparisons.append({'candidate_id': r['id'], 'theorem': fullname, 'source': origin,
                            'expected_type': expected})
    source = output / 'all_references.lean'
    source.write_text('\n'.join(chunks))
    cmd = ['lake', 'env', 'lean', '--json', str(source.resolve())]
    started = time.monotonic()
    result = _run_compiler(cmd, cwd=str(ROOT/'lean_project'), capture_output=True, text=True, timeout=600)
    messages, malformed = _diagnostics(result.stdout)
    for row in comparisons:
        row['axioms'] = _axioms_from_diagnostics(messages, row['theorem'])
        row['strict_verified'] = (result.returncode == 0 and not malformed
            and row['axioms'] is not None and not set(row['axioms']) - set(DEFAULT_POLICY.allowed_axioms)
            and not any(d['severity'] == 'error' for d in messages))
    record = {'command': cmd, 'exit_code': result.returncode, 'stdout': result.stdout,
              'stderr': result.stderr, 'elapsed_seconds': time.monotonic()-started,
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              'comparisons': comparisons, 'verified_count': sum(r['strict_verified'] for r in comparisons),
              'scope': 'Reference proposition truth and exact theorem types, NOT English equivalence'}
    (output/'verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    print('Lean exit', result.returncode, 'strict exact-type checks', record['verified_count'], '/', len(records))
    if result.returncode: print(result.stdout[-6000:]); raise SystemExit(1)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--output', type=Path, required=True)
    build(p.parse_args().output)
