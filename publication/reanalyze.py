"""Offline reanalysis of disclosed outcomes and redacted pairing evidence.

This is not exact original-byte inference replay or a new Lean verification.
Only Python's standard library is required. Run: python3 reanalyze.py
"""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def read(path):return json.loads(path.read_text())
def digest(data):return hashlib.sha256(data).hexdigest()


def wilson(k,n):
    z=1.959963984540054;p=k/n;d=1+z*z/n
    center=(p+z*z/(2*n))/d;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,center-half),min(1,center+half)]


def main():
    cases=read(ROOT/'results/cases.json');assert len(cases)==60
    assert len({r['problem_id'] for r in cases})==60
    complete=[r for r in cases if all(v is not None for v in r['outcomes'].values())]
    assert len(complete)==58
    counts={c:{'success':sum(r['outcomes'][c] is True for r in cases),
               'known_failure':sum(r['outcomes'][c] is False for r in cases),
               'unavailable':sum(r['outcomes'][c] is None for r in cases)} for c in ['A','B','C']}
    assert counts=={'A':{'success':0,'known_failure':60,'unavailable':0},
                   'B':{'success':1,'known_failure':59,'unavailable':0},
                   'C':{'success':1,'known_failure':57,'unavailable':2}}
    altered_prompt_hashes=0;calls=0;candidate_hashes_checked=0
    for row in cases:
        folder=ROOT/'evidence/redacted_runs/heldout/2027'/row['problem_id']
        m=read(folder/'manifest.json');assert m['problem_id']==row['problem_id']
        assert {c:m['conditions'][c]['success'] for c in ['A','B','C']}==row['outcomes']
        initial=m['initial']
        assert initial['candidate_sha256']==row['initial_candidate_sha256']
        for c in ['A','B','C']:
            assert m['conditions'][c]['initial_candidate_sha256']==initial['candidate_sha256']
            assert len(m['conditions'][c]['attempts'])<=3
        steps=[initial]+[a for c in ['B','C'] for a in m['conditions'][c]['attempts']]
        for step in steps:
            key=step['key'];completion=read(folder/key/'completion.json')
            verification=read(folder/key/'verification.json');assert verification==step['verification']
            calls+=1
            if digest(completion['prompt'].encode())!=completion['prompt_sha256']:
                altered_prompt_hashes+=1
            md=completion['metadata']
            seed=int.from_bytes(hashlib.sha256(f"{md['base_seed']}:{md['generation_context']}:{md['prompt_sha256']}".encode()).digest()[:4],'big')
            assert seed==md['generation_seed']
            assert md['model']=='mlx-community/Qwen2.5-7B-Instruct-4bit'
            assert md['snapshot_revision']=='c26a38f6a37d0a51b4e9a1eb3026530fa35d9fed'
            candidate=read(folder/key/'candidate.lean.json')
            assert candidate['candidate_view']==step['candidate']
            if digest(candidate['candidate_view'].encode())==step['candidate_sha256']:
                candidate_hashes_checked+=1
            assert candidate['original_sha256']==step['candidate_sha256']
            if verification['success']:
                assert verification['exit_code']==0
                assert set(verification['axiom_dependencies']) <= {'propext','Classical.choice','Quot.sound'}
        for c in ['B','C']:
            prior=initial
            for step in m['conditions'][c]['attempts']:
                if c=='B':assert step['feedback_payload']=='No compiler diagnostics are provided in the blind-retry condition.'
                else:
                    expected=[d for d in prior['verification']['diagnostics'] if d.get('kind')!='hasSorry']
                    assert json.loads(step['feedback_payload'])=={'diagnostic_state':'available','diagnostics':expected}
                    assert step['feedback_source_candidate_sha256']==prior['candidate_sha256']
                prior=step
    assert calls==410
    b_only=sum(r['outcomes']['B'] and not r['outcomes']['C'] for r in complete)
    c_only=sum(r['outcomes']['C'] and not r['outcomes']['B'] for r in complete)
    assert b_only==c_only==0
    result={'cases':60,'complete_pairs':58,'counts':counts,
            'missing_as_failure_rates':{c:counts[c]['success']/60 for c in counts},
            'missing_as_failure_wilson_95':{c:wilson(counts[c]['success'],60) for c in counts},
            'complete_pair_B_and_C_rate':1/58,'discordant_pairs':0,
            'mcnemar_conventional_p':1.0,'mcnemar_note':'The original analysis stores null for zero discordance; conventionally p=1. Neither convention supplies evidence of equivalence.',
            'missingness_C_minus_B_bounds_pp':[0,100*2/60],
            'heldout_completed_calls_checked':calls,'unchanged_candidate_hashes_checked':candidate_hashes_checked,
            'prompts_with_changed_public_bytes':altered_prompt_hashes,
            'scope':'Redacted-view consistency and aggregate reanalysis, not proof of authenticity of withheld originals or exact prompt replay.'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
