"""Report actual synthetic judge diagnostics, not study/generalization accuracy."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from ai_audit_quality import quality_flags


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True);a=p.parse_args()
    spec=importlib.util.spec_from_file_location('synthetic_audit_controls',ROOT/'scripts/ai_audit_calibration.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    expected={i:label for i,_,_,label in module.CONTROLS}
    if json.loads((a.directory/'expected_labels.json').read_text())!=expected:raise ValueError('Control labels changed')
    rows=[]
    for ident,label in expected.items():
        path=a.directory/'responses'/(ident+'.json');r=json.loads(path.read_text())
        flags=quality_flags(r['judgment'])
        actual=r['judgment']['label'] if r['judgment'] else None
        rows.append({'control_id':ident,'expected_label':label,'actual_schema_valid_label':actual,
            'quality_flags':flags,'usable_for_control_comparison':not flags,
            'matches_authored_expectation':actual==label if not flags else None,
            'response_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    report={'kind':'development_only_synthetic_semantic_judge_diagnostics','controls':len(rows),
        'expected_label_provenance':'Coding-AI-authored controls, not human-adjudicated gold.',
        'usable_responses':sum(r['usable_for_control_comparison'] for r in rows),
        'matches':sum(r['matches_authored_expectation'] is True for r in rows),
        'mismatches':sum(r['matches_authored_expectation'] is False for r in rows),
        'unusable':sum(not r['usable_for_control_comparison'] for r in rows),
        'generalization_accuracy_claim':False,'study_experiment':False,'results':rows}
    with (a.directory/'diagnostics.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))


if __name__=='__main__':main()
