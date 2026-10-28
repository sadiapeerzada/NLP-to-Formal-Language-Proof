"""Development-only synthetic judge controls, disjoint from the research pool."""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('ai_audit_runner', Path(__file__).with_name('ai_semantic_audit.py'))
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)

# Authored controls, not empirical research cases or human-adjudicated gold data.
# Expected labels follow literal finite arithmetic/domain changes; no dataset item
# or model response is used as a calibration prompt or demonstration.
CONTROLS = [
 ('syn_01','For every natural n, n plus zero equals n.', 'theorem control (n : ℕ) : n + 0 = n','faithful'),
 ('syn_02','For every natural n, n plus zero equals n.', 'theorem control (n : ℕ) : n + 1 = n + 1','not faithful'),
 ('syn_03','Every natural number is strictly greater than zero.', 'theorem control (n : ℕ) : 0 ≤ n','not faithful'),
 ('syn_04','For every natural n at least one, n minus one plus one equals n.', 'theorem control (n : ℕ) (h : 1 ≤ n) : n - 1 + 1 = n','faithful'),
 ('syn_05','For every natural n, n minus one plus one equals n.', 'theorem control (n : ℕ) (h : 1 ≤ n) : n - 1 + 1 = n','not faithful'),
 ('syn_06','For every integer x, there exists an integer y with y greater than x.', 'theorem control (x : ℤ) : ∃ y : ℤ, x < y','faithful'),
 ('syn_07','There exists a natural number greater than every natural number.', 'theorem control : ∀ n : ℕ, ∃ m : ℕ, n < m','not faithful'),
 ('syn_08','For every integer x, x squared is nonnegative.', 'theorem control (x : ℤ) : 0 ≤ x ^ 2','faithful'),
 ('syn_09','For natural a and b, if a divides b and b divides a, then a equals b.', 'theorem control (a b : ℕ) (h : a ∣ b) (g : b ∣ a) : a = b','faithful'),
 ('syn_10','For natural n, the sum of the numbers from zero through n equals n(n+1)/2.', 'theorem control (n : ℕ) : 2 * (∑ i ∈ Finset.range (n + 1), i) = n * (n + 1)','faithful'),
 ('syn_11','For every natural n, n is divisible by four if and only if n is divisible by two.', 'theorem control (n : ℕ) : 4 ∣ n → 2 ∣ n','not faithful'),
 ('syn_12','For every positive integer m, zero is congruent to zero modulo m.', 'theorem control (m : ℤ) : Int.ModEq m 0 0','not faithful')
]

def probes():
    return [{'id':i,'nl_statement':n,'expected_lean_statement':s,'required_imports':['Mathlib'],
             'required_definitions':None} for i,n,s,_ in CONTROLS]

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run']);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    runner.MODEL=runner.ROOT/'data/ai_semantic_audit/20261028/model_phi4'
    runner.TEMPLATE=runner.ROOT/'prompts/ai_semantic_audit_v2.txt'
    if a.action=='prepare':
        runner.load_candidates=lambda root:probes()
        runner.prepare(a.output)
        path=a.output/'manifest.json';m=json.loads(path.read_text())
        m['kind']='development_only_synthetic_judge_calibration_not_study'
        m['source_sha256']['scripts/ai_audit_calibration.py']=runner.sha(Path(__file__))
        m['limitations']=['Synthetic coding-AI-authored controls; not human-adjudicated gold. No statistical accuracy or generalization claim.',
            'Controls include strength mismatches even when both propositions are true. Literal quantifier preservation is the declared audit criterion.']
        path.write_text(json.dumps(m,indent=2)+'\n')
        (a.output/'expected_labels.json').write_text(json.dumps({i:l for i,_,_,l in CONTROLS},indent=2)+'\n')
    else:runner.run(a.output)
