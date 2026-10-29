"""Validation gates for the proposed local replacement; never approve on behalf of a supervisor."""
from __future__ import annotations
import hashlib
from datetime import date
import importlib.metadata
import json
import subprocess
from pathlib import Path
from dataset_validation import validate_curation_draft, validate_frozen_curation
from semantic_review import check_artifact

ROOT=Path(__file__).resolve().parents[1]

def file_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_local_protocol(path: Path) -> dict:
    p=json.loads(path.read_text());m=p['model'];d=p['decoding']
    if m.get('provider')!='mlx_local' or m.get('fallback_model') is not None:
        raise ValueError('Local protocol requires MLX and no provider/model fallback.')
    if d!={**d,'temperature':0.2,'max_completion_tokens':2000,'reasoning_effort':None,'top_p':1.0,'max_context_tokens':8192}:
        raise ValueError('Local decoding settings differ from the reviewed implementation.')
    if p['conditions']['B']['maximum_repair_calls']!=3 or p['conditions']['C']['maximum_repair_calls']!=3:
        raise ValueError('Both repair conditions require three calls.')
    if p.get('condition_execution_order')!=['B','C']:
        raise ValueError('Condition execution order is not implemented as specified.')
    if p['repetition'].get('local_base_seeds')!=[d.get('generation_seed')]:
        raise ValueError('Implementation requires exactly one declared base seed.')
    if p.get('compute_policy',{}).get('paid_inference_allowed') is not False:
        raise ValueError('Paid inference is prohibited.')
    for spec in p['prompt_templates'].values():
        if file_hash(ROOT/spec['path'])!=spec['sha256']: raise ValueError('Prompt hash mismatch.')
    env=p['lean_environment']
    for key,name in [('lean_toolchain_sha256','lean-toolchain'),('lake_manifest_sha256','lake-manifest.json'),('lakefile_sha256','lakefile.toml')]:
        if file_hash(ROOT/'lean_project'/name)!=env[key]: raise ValueError('Pinned Lean environment mismatch.')
    for module in env.get('candidate_definition_modules',[]):
        if file_hash(ROOT/module['path'])!=module['sha256']:
            raise ValueError('Candidate definition module changed.')
    for implementation in p.get('implementation_files',[]):
        if file_hash(ROOT/implementation['path'])!=implementation['sha256']:
            raise ValueError('Local implementation source changed after protocol preparation.')
    inventory_path=ROOT/m['model_inventory_file']
    if file_hash(inventory_path)!=m['model_inventory_sha256']: raise ValueError('Model inventory hash mismatch.')
    inventory=json.loads(inventory_path.read_text())
    if inventory['snapshot_revision']!=m['immutable_revision'] or inventory['chat_template_sha256']!=m['chat_template_sha256'] or inventory['quantization']!=m['quantization']:
        raise ValueError('Model protocol and inventory disagree.')
    return p


def live_lean_environment(protocol: dict) -> dict:
    """Verify the actual executables/checkout, not only the lockfile bytes."""
    project=ROOT/'lean_project';package=project/'.lake/packages/mathlib'
    commands=[['lake','env','lean','--version'],['git','-C',str(package),'rev-parse','HEAD'],['git','-C',str(package),'status','--porcelain']]
    outputs=[]
    for command in commands:
        result=subprocess.run(command,cwd=project,capture_output=True,text=True,timeout=30)
        if result.returncode:raise ValueError('Cannot inspect actual Lean/Mathlib environment.')
        outputs.append(result.stdout.strip())
    if not outputs[0].startswith('Lean (version 4.32.0,') or outputs[1]!=protocol['lean_environment']['mathlib_revision'] or outputs[2]:
        raise ValueError('Actual Lean version or clean Mathlib checkout differs from the pinned environment.')
    return {'lean_version':outputs[0],'mathlib_actual_revision':outputs[1],'mathlib_source_clean':True}


def execution_context(protocol_path: Path, approval_path: Path | None, dataset_path: Path | None,
                      problem_id: str, theorem: str, client, *, phase: str,
                      development_path: Path | None = None, freeze_path: Path | None = None) -> dict:
    p=validate_local_protocol(protocol_path)
    if p.get('local_execution_enabled') is not True or p['protocol_status'] not in {'approved_for_development_pilot','approved_and_preregistered','frozen_and_preregistered'}:
        raise ValueError('Local study execution is blocked pending genuine supervisor approval.')
    if phase not in {'development_pilot','heldout'}: raise ValueError('Unknown execution phase.')
    if approval_path is None or dataset_path is None: raise ValueError('Approval and exact eligible dataset artifacts are required.')
    a=json.loads(approval_path.read_text());records=json.loads(dataset_path.read_text());h=file_hash(protocol_path)
    if a.get('status')!='approved' or a.get('reviewer_kind')!='independent_human_review' or not a.get('reviewer_id') or not a.get('reviewed_on'):
        raise ValueError('Supervisor approval provenance is missing.')
    try:
        reviewed=date.fromisoformat(a['reviewed_on'])
    except (ValueError,TypeError,KeyError) as error:
        raise ValueError('Supervisor approval date must be an ISO date.') from error
    if reviewed>date.today(): raise ValueError('Future supervisor approvals are invalid.')
    approval_evidence=check_artifact(a.get('evidence_artifact'),approval_path.parent)
    if a.get('local_substitution_approved') is not True or a.get('protocol_sha256')!=h or a.get('dataset_sha256')!=file_hash(dataset_path) or problem_id not in a.get('approved_problem_ids',[]) or a.get('phase')!=phase:
        raise ValueError('Approval does not bind this exact local execution package.')
    if a.get('maximum_logical_generations_per_problem')!=7 or a.get('paid_inference_allowed') is not False:
        raise ValueError('Approval must enforce seven local generations and prohibit paid inference.')
    report=validate_curation_draft(records)
    if not report.is_valid or problem_id not in report.eligible_problem_ids:
        raise ValueError('Problem does not have eligible independent review/source/proof evidence.')
    record=next(r for r in records if r['id']==problem_id)
    if record['expected_lean_statement']!=theorem: raise ValueError('Theorem differs from reviewed dataset bytes.')
    if phase=='development_pilot' and record['curation']['split']!='development': raise ValueError('Pilot must use development examples only.')
    if phase=='heldout':
        if p['protocol_status'] not in {'approved_and_preregistered','frozen_and_preregistered'} or development_path is None or freeze_path is None:
            raise ValueError('Held-out execution requires approved preregistration and frozen splits.')
        frozen=validate_frozen_curation(records,json.loads(freeze_path.read_text()),file_hash(dataset_path),development_value=json.loads(development_path.read_text()),development_dataset_sha256=file_hash(development_path))
        if not frozen.is_valid: raise ValueError('Frozen dataset validation failed: '+'; '.join(frozen.errors))
        pilot=check_artifact(a.get('audited_pilot_artifact'),approval_path.parent)
        pilot_record=json.loads(Path(pilot).read_text())
        if pilot_record.get('phase')!='development_pilot' or pilot_record.get('status')!='completed' or pilot_record.get('local_generation_confirmed') is not True:
            raise ValueError('A completed genuine local development pilot is required.')
    m=p['model']
    frozen_inventory=json.loads((ROOT/m['model_inventory_file']).read_text())
    if client.inventory!=frozen_inventory:
        raise ValueError('Client weight/tokenizer hashes differ from approved inventory.')
    if client.model_id!=m['requested_model_id'] or client.inventory['snapshot_revision']!=m['immutable_revision'] or client.seed!=p['decoding']['generation_seed'] or client.max_context_tokens!=p['decoding']['max_context_tokens']:
        raise ValueError('Local client does not match frozen model/decoding.')
    for package,key in [('mlx','mlx_version'),('mlx-lm','backend_version')]:
        if importlib.metadata.version(package)!=m[key]: raise ValueError('Installed backend version differs from protocol.')
    actual_environment=live_lean_environment(p)
    return {'actual_lean_environment':actual_environment,'protocol':{'version':p['protocol_version'],'status':p['protocol_status'],'path':str(protocol_path.resolve().relative_to(ROOT)),'sha256':h},
            'provider':'mlx_local','prompt_templates':p['prompt_templates'],'model':m,'decoding':p['decoding'],'phase':phase,
            'approval_sha256':file_hash(approval_path),'approval_record_path':str(approval_path.resolve()),
            'approval_record':a,'approval_evidence_path':approval_evidence,
            'implementation_files':p.get('implementation_files',[]),
            'input_natural_language':record['nl_statement']}
