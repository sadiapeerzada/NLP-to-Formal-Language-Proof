"""Assemble actual audit evidence; preserve every original curation field."""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from ai_semantic_audit import digest, subject, proposed_record, assert_unchanged_curation
from ai_audit_quality import quality_flags, exact_duplicate_groups
from candidate_inventory import load_candidates
from dataset_validation import validate_curation_draft


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())


def fenced(text, language='text'):
    fence='`'*max(3,1+max((len(s) for s in re.findall(r'`+',text)),default=0))
    return fence+language+'\n'+text+'\n'+fence+'\n'


def checked_pass(path, records, *, require_complete=True):
    manifest=read(path/'manifest.json')
    if sha(path/'subjects.json')!=manifest['subjects_sha256']:raise ValueError('Stale subject snapshot')
    saved=read(path/'subjects.json')
    if saved!=records:raise ValueError('Original inventory changed since review')
    for name, expected in manifest['source_sha256'].items():
        if sha(ROOT/name)!=expected:raise ValueError('Implementation/prompt changed: '+name)
    events=[json.loads(line) for line in (path/'journal.jsonl').read_text().splitlines()]
    intents=[e['candidate_id'] for e in events if e['event']=='intent']
    completions=[e for e in events if e['event']=='completed']
    record_ids={r['id'] for r in records};completion_ids=[e['candidate_id'] for e in completions]
    if len(set(intents))!=len(intents) or not set(intents)<=record_ids:raise ValueError('Unknown or replayed review context')
    if len(set(completion_ids))!=len(completion_ids) or not set(completion_ids)<=set(intents):raise ValueError('Invalid completion journal')
    if require_complete:
        if set(intents)!=record_ids or set(completion_ids)!=record_ids or any(e['event']=='interrupted' for e in events):raise ValueError('Incomplete reviewer execution')
    else:
        retirement=read(path/'retirement.json')
        if retirement['status']!='exploratory_reviewer_retired_not_a_complete_pass' or retirement['journal_sha256']!=sha(path/'journal.jsonl'):
            raise ValueError('Missing/changed explicit exploratory retirement')
        if retirement['completed_ids']!=completion_ids or set(retirement['unattempted_ids'])!=record_ids-set(intents):raise ValueError('Retirement counts changed')
        if retirement['interrupted_ids']!=[e['candidate_id'] for e in events if e['event']=='interrupted']:raise ValueError('Interrupted contexts changed')
    by_id={}
    for event in completions:
        ident=event['candidate_id'];p=path/'responses'/(ident+'.json');r=read(p)
        if sha(p)!=event['response_sha256']:raise ValueError('Response changed')
        if sha(path/'prompts'/(ident+'.txt'))!=manifest['prompt_sha256'][ident]:raise ValueError('Prompt changed')
        if r['subject_sha256']!=manifest['subject_bindings'][ident] or r['metadata']['snapshot_revision']!=manifest['selection']['review_revision']:
            raise ValueError('Wrong response binding/model')
        if r['metadata']['prompt_sha256']!=manifest['prompt_sha256'][ident]:raise ValueError('Wrong model input')
        if r['metadata']['api_attempts']!=0:raise ValueError('Not a local-only call')
        by_id[ident]=r
    return by_id


def assemble(base, output):
    rows=load_candidates(ROOT)
    retired=(base/'phi_pass1/retirement.json').exists()
    first=checked_pass(base/'phi_pass1',rows,require_complete=not retired);second=checked_pass(base/'phi4_pass2',rows)
    retirement=read(base/'phi_pass1/retirement.json') if retired else {'interrupted_ids':[],'unattempted_ids':[]}
    static=read(base/'coding_assistant_assessments.json');seal=read(base/'coding_assistant_assessment_manifest.json')
    if sha(base/'coding_assistant_assessments.json')!=seal['sha256']:raise ValueError('Static review changed')
    math=read(base/'math_checks/results.json')
    if math['source_sha256']!=sha(ROOT/'scripts/ai_audit_math_checks.py'):raise ValueError('Math checker changed')
    math_by_id={r['candidate_id']:r for r in math['results']}
    lean=read(base/'lean_reference_check/verification.json')
    if lean['source_sha256']!=sha(base/'lean_reference_check/all_references.lean') or lean['exit_code']!=0 or lean['verified_count']!=len(rows):raise ValueError('Lean check incomplete/changed')
    lean_by_id={r['candidate_id']:r for r in lean['comparisons']}
    output.mkdir(parents=True,exist_ok=False);packets=output/'records';packets.mkdir()
    proposed=[];disagreements=[];actions=[]
    duplicate_aliases={group[i]:group[0] for group in static['duplicate_groups'] for i in range(1,len(group))}
    automatic_duplicates=exact_duplicate_groups(rows)
    if automatic_duplicates!=static['duplicate_groups']:raise ValueError('Static and exact duplicate findings disagree')
    for r in rows:
        ident=r['id'];two=second[ident]
        exploratory_status='completed' if ident in first else ('interrupted' if ident in retirement['interrupted_ids'] else 'unattempted_reviewer_retired')
        one=first.get(ident,{'judgment':None,'parse_error':'No completed exploratory judgment: '+exploratory_status,
                             'raw_response':'No completed response. Consult the preserved retirement/journal/stream evidence.'})
        if math_by_id[ident]['subject_sha256']!=digest(subject(r)):raise ValueError('Math subject changed')
        assessment={'label':static['overrides'].get(ident,{}).get('label',static['default_label']),
                    'note':static['notes'][ident],**static['overrides'].get(ident,{})}
        labels=[one['judgment']['label'] if one['judgment'] else ('invalid_format' if ident in first else exploratory_status),
                two['judgment']['label'] if two['judgment'] else 'invalid_format']
        reasons=[]
        quality=[quality_flags(one['judgment']) if ident in first else ['Exploratory model did not complete a review; no verdict exists.'],
                 quality_flags(two['judgment'])]
        for name,flags in zip(['Phi-3.5','Phi-4'],quality):
            if flags:reasons.append(name+' response quality: '+' '.join(flags))
        if len(set([assessment['label'],*labels]))>1:reasons.append('Coding-AI/model labels or parse status differ.')
        if 'invalid_format' in labels:reasons.append('At least one model response failed the frozen strict JSON schema; its label is NOT counted.')
        if any(v in ('not faithful','uncertain') for v in labels):reasons.append('At least one model raises a semantic concern; raw explanation requires adjudication.')
        if assessment['label']!='faithful':reasons.append(assessment['issue'])
        if ident in duplicate_aliases:reasons.append('Exact duplicate of '+duplicate_aliases[ident]+'.')
        if math_by_id[ident]['failures']:reasons.append('Bounded mathematical probe failure.')
        if not lean_by_id[ident]['strict_verified']:raise ValueError('Reference not strictly verified')
        status='concordant_ai_only_pending_supervisor_policy' if not reasons else 'unresolved_ai_audit_requires_adjudication'
        if ident in duplicate_aliases:action='propose_exclude_duplicate'
        elif assessment['label']=='not faithful':action='propose_revision'
        elif assessment['label']=='uncertain':action='propose_clarification'
        elif two['judgment'] and not quality[1] and two['judgment']['label']=='faithful':action='tentatively_retain_subject_to_resolving_all_disagreements'
        else:action='retain_in_review_queue_no_acceptance'
        audit={'candidate_id':ident,'subject_sha256':digest(subject(r)),
            'reviewer_kind':'ai_only_not_independent_human','grants_eligibility':False,
            'status':status,'coding_assistant_assessment':assessment,
            'phi_3_5':{'judgment':one['judgment'],'parse_error':one['parse_error'],'response':str((base/'phi_pass1/responses'/(ident+'.json')).relative_to(ROOT)),
                       'status':exploratory_status,
                       'response_sha256':sha(base/'phi_pass1/responses'/(ident+'.json')) if ident in first else None},
            'phi_4':{'judgment':two['judgment'],'parse_error':two['parse_error'],'response':str((base/'phi4_pass2/responses'/(ident+'.json')).relative_to(ROOT)),
                     'response_sha256':sha(base/'phi4_pass2/responses'/(ident+'.json'))},
            'lean_reference_check':lean_by_id[ident], 'mathematical_probe':math_by_id[ident],
            'disagreement_reasons':reasons,'proposed_action':action,
            'posthoc_quality_flags':{'phi_3_5':quality[0],'phi_4':quality[1]},
            'human_review_status':'unchanged_pending','policy_change_approved':False}
        if ident not in first:audit['phi_3_5']['response']=None
        proposed.append(proposed_record(r,audit));actions.append({'candidate_id':ident,'action':action,'coding_ai_label':assessment['label'],'phi_labels':labels})
        if reasons:disagreements.append({'candidate_id':ident,'coding_ai_label':assessment['label'],'phi_labels':labels,'reasons':reasons,
            'resolution_status':'unresolved_no_automatic_majority_vote'})
        (packets/(ident+'.json')).write_text(json.dumps({'subject':subject(r),'audit':audit},indent=2,ensure_ascii=False)+'\n')
        text=[f'# {ident}: AI-only audit\n','No human review or approval. Existing curation and eligibility are unchanged.\n',
              '## English\n',fenced(r['nl_statement']),'## Lean type\n',fenced(r['expected_lean_statement'],'lean'),
              '## Coding-assistant static assessment\n',fenced(json.dumps(assessment,ensure_ascii=False,indent=2),'json'),
              '\n## Fresh Lean check\n',fenced(json.dumps(lean_by_id[ident],ensure_ascii=False,indent=2),'json'),
              '\n## Bounded mathematical probe\n',fenced(json.dumps(math_by_id[ident],ensure_ascii=False,indent=2),'json')]
        for title,response in [('Phi-3.5',one),('Phi-4-mini',two)]:
            text += ['\n## '+title+' actual judgment\n',fenced(json.dumps(response['judgment'],indent=2,ensure_ascii=False),'json'),
                     'Schema error: '+str(response['parse_error'])+'\n','Raw model response (untrusted, including any unsupported claims):\n',
                     fenced(response['raw_response'])]
        text += ['\n## Disagreements and proposed action\n',fenced(json.dumps({'status':status,'reasons':reasons,'action':action},ensure_ascii=False,indent=2),'json')]
        (packets/(ident+'.md')).write_text('\n'.join(text)+'\n')
    assert_unchanged_curation(rows,proposed)
    (output/'proposed_ai_audited_dataset.json').write_text(json.dumps(proposed,indent=2,ensure_ascii=False)+'\n')
    (output/'disagreements.json').write_text(json.dumps(disagreements,indent=2,ensure_ascii=False)+'\n')
    (output/'proposed_actions.json').write_text(json.dumps(actions,indent=2)+'\n')
    (output/'proposed_unique_candidate_ids.json').write_text(json.dumps({
        'status':'proposal_only_not_frozen_or_eligible',
        'note':'Exact duplicate exclusion only; family independence/source/review/split requirements remain unresolved.',
        'candidate_ids':[r['id'] for r in rows if r['id'] not in duplicate_aliases],
        'excluded_exact_duplicates':duplicate_aliases},indent=2)+'\n')
    report=validate_curation_draft(proposed)
    summary={'kind':'ai_only_audit_not_empirical_repair_results','candidate_count':len(rows),
        'phi_3_5_completed':len(first),'phi_4_completed':len(second),
        'phi_3_5_interrupted':len(retirement['interrupted_ids']),
        'phi_3_5_unattempted':len(retirement['unattempted_ids']),
        'ai_review_attempts':len(first)+len(retirement['interrupted_ids'])+len(second),
        'ai_review_completed_generations':len(first)+len(second),
        'phi_3_5_labels':dict(Counter(r['judgment']['label'] if r['judgment'] else 'invalid_format' for r in first.values())),
        'phi_4_labels':dict(Counter(r['judgment']['label'] if r['judgment'] else 'invalid_format' for r in second.values())),
        'coding_ai_labels':dict(Counter(r['ai_semantic_audit']['coding_assistant_assessment']['label'] for r in proposed)),
        'phi_3_5_without_detected_quality_flags':sum(not quality_flags(r['judgment']) for r in first.values()),
        'phi_4_without_detected_quality_flags':sum(not quality_flags(r['judgment']) for r in second.values()),
        'fresh_lean_verified':lean['verified_count'],'bounded_checks':math['checked_assignments'],
        'exact_duplicate_groups':automatic_duplicates,
        'proposed_candidate_count_after_exact_duplicate_exclusion':len(rows)-len(duplicate_aliases),
        'bounded_probe_failures':sum(bool(r['failures']) for r in math['results']),
        'unresolved_records':len(disagreements),'actions':dict(Counter(r['action'] for r in actions)),
        'independent_human_reviews':0,'eligible_split_counts':report.eligible_split_counts,
        'structural_errors':list(report.errors),'paid_inference_requests':0,
        'study_gate_changes':False,'study_pilots':0,'heldout_repair_runs':0,
        'curation_fields_identical':True,'dataset_sha256':sha(output/'proposed_ai_audited_dataset.json')}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    index=['# AI-only semantic audit of 96 candidates\n','AI-only evidence; no eligibility, freeze, human review or supervisor approval.\n',
           'See `summary.json`, `disagreements.json`, `proposed_actions.json` and `proposed_ai_audited_dataset.json`. All model outputs, including invalid ones, are preserved.\n']
    index += [f'- [{r["id"]}](records/{r["id"]}.md): {r["ai_semantic_audit"]["status"]}; {r["ai_semantic_audit"]["proposed_action"]}' for r in proposed]
    (output/'README.md').write_text('\n'.join(index)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assemble(a.base.resolve(),a.output.resolve())
