"""Plan or execute the approved local A/B/C protocol without a paid API."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from local_protocol import validate_local_protocol, file_hash

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--protocol',type=Path,default=ROOT/'configs/repair_experiment_local_v0.3.0.json')
    p.add_argument('--plan-only',action='store_true');p.add_argument('--snapshot',type=Path)
    p.add_argument('--approval',type=Path);p.add_argument('--dataset',type=Path)
    p.add_argument('--problem-id');p.add_argument('--phase',choices=['development_pilot','heldout'],default='development_pilot')
    p.add_argument('--development-dataset',type=Path);p.add_argument('--freeze-manifest',type=Path)
    p.add_argument('--output-root',type=Path);a=p.parse_args();protocol=validate_local_protocol(a.protocol)
    if a.plan_only:
        print(json.dumps({'status':protocol['protocol_status'],'protocol_sha256':file_hash(a.protocol),'execution_enabled':protocol['local_execution_enabled'],
            'model':protocol['model'],'decoding':protocol['decoding'],'paid_inference_allowed':False,
            'maximum_logical_generations_per_problem':7,'model_calls_made':0,
            'required_approvals':protocol['execution_gate']},indent=2));return
    if not all([a.snapshot,a.dataset,a.problem_id,a.output_root,a.approval]):
        p.error('Execution requires snapshot, dataset, problem ID, fresh output root and genuine approval.')
    if not protocol['local_execution_enabled']:
        p.error('Local protocol is proposed and disabled; no model was loaded or called.')
    from local_llm_client import LocalMLXClient
    from repair_experiment import run_experiment
    inventory=json.loads((ROOT/protocol['model']['model_inventory_file']).read_text())
    client=LocalMLXClient(a.snapshot,inventory,model_id=protocol['model']['requested_model_id'],seed=protocol['decoding']['generation_seed'],max_context_tokens=protocol['decoding']['max_context_tokens'])
    records=json.loads(a.dataset.read_text());record=next((r for r in records if r['id']==a.problem_id),None)
    if record is None: p.error('Unknown problem ID.')
    path=run_experiment(a.problem_id,record['expected_lean_statement'],ROOT/'lean_project',a.output_root,
        model=client.model_id,execution_mode='local',completion_fn=client,dataset_path=a.dataset,
        local_protocol_path=a.protocol,local_approval_path=a.approval,local_phase=a.phase,
        development_path=a.development_dataset,freeze_path=a.freeze_manifest)
    print(path)
if __name__=='__main__': main()
