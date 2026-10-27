"""Human-readable review packets and fail-closed imports of human decisions.

File hashes establish binding, not identity. A genuinely human-verified reviewer
registry and its evidence must be supplied externally; no such registry is made
by this program. Import never promotes unrelated dataset eligibility fields.
"""
from __future__ import annotations
import argparse
import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import re

LABELS = {'faithful', 'not faithful', 'uncertain'}


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',', ':')).encode()).hexdigest()


def binding(record: dict) -> str:
    return canonical_hash({'id':record['id'], 'english':record['nl_statement'],
                           'lean':record['expected_lean_statement'],
                           'imports':record.get('required_imports'),
                           'definitions':record.get('required_definitions'),
                           'assumptions':record.get('mathematical_assumptions')})


from candidate_inventory import load_candidates


def generated_review_subjects(records: list[dict], results_path: Path) -> list[dict]:
    """Prepare actual generated statements without treating them as references."""
    references={r['id']:r for r in records};subjects=[];seen=set()
    source_hash=hashlib.sha256(results_path.read_bytes()).hexdigest()
    for line in results_path.read_text().splitlines():
        if not line.strip(): continue
        result=json.loads(line);original=references.get(result.get('id'))
        if original is None or not isinstance(result.get('final_lean_statement'),str):
            raise ValueError('Generated result lacks a matching English source or Lean statement.')
        if not result['final_lean_statement'].strip(): continue
        run=result.get('run_id')
        if not isinstance(run,str) or not re.fullmatch(r'[A-Za-z0-9_-]+',run):
            raise ValueError('Generated review subject requires a safe actual run ID.')
        r=copy.deepcopy(original);r['id']=f"generated_{run}_{original['id']}"
        if r['id'] in seen: raise ValueError('Duplicate generated statement review subject.')
        seen.add(r['id']);r['subject_kind']='generated_statement'
        r['reference_lean_statement_for_comparison']=original['expected_lean_statement']
        r['expected_lean_statement']=result['final_lean_statement']
        r['generated_statement_provenance']={'results_path':str(results_path),'results_sha256':source_hash,
            'run_id':run,'source_problem_id':original['id'],'raw_result':result,
            'compiler_success_claim':result.get('solved'), 'semantic_success':False}
        c=r['curation'];c['semantic_fidelity']={'review_status':'pending','label':None,'reviewer_provenance':None,'evidence':None}
        c['review_records']=[];c['theorem_verification']=None
        for field in ('theorem_statement_review','assumption_mismatch_review','self_containment_review','category_difficulty_review'):
            if isinstance(c.get(field),dict):c[field]['status']='pending'
        c['family_review_status']='pending';c['split_status']='pending'
        subjects.append(r)
    return subjects


def prepare_packets(records: list[dict], output: Path) -> None:
    output.mkdir(parents=True,exist_ok=False)
    index=['# Independent Lean semantic review\n',
           'No decisions are supplied. Compilation is not semantic faithfulness.\n']
    for r in records:
        ident=r['id']
        if not re.fullmatch(r'[A-Za-z0-9_-]+',ident):
            raise ValueError('Unsafe candidate ID.')
        c=r['curation']; token=binding(r)
        decision={'schema_version':1,'candidate_id':ident,'binding_sha256':token,
                  'review_type':'semantic_fidelity','label':None,'reviewer_id':None,
                  'reviewer_kind':'independent_human_review','reviewed_on':None,
                  'independence_attestation':None,'evidence':None,'evidence_artifact':None}
        (output/f'{ident}.decision.json').write_text(json.dumps(decision,indent=2)+'\n')
        packet={'record':r,'binding_sha256':token,'decision_template':decision}
        (output/f'{ident}.json').write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
        # Fences prevent mathematical text or embedded markup becoming active HTML.
        chunks=[f'# {ident}: independent review\n', '## English statement\n',
                '```text\n'+r['nl_statement']+'\n```\n',('## Generated Lean statement (unreviewed)\n' if r.get('subject_kind')=='generated_statement' else '## Lean reference\n'),
                '```lean\n'+r['expected_lean_statement']+'\n```\n',
                '## Quantifiers, assumptions and definitions\n',
                'Read every explicit/implicit binder and typeclass in the theorem above. '
                'Compare its domains, existence/uniqueness, hypotheses and conclusion to English. '
                'The metadata below are author-assisted preparation, not reviewer findings.\n',
                '```json\n'+json.dumps({k:r.get(k) for k in ('mathematical_assumptions','required_imports','required_definitions','category','difficulty')},indent=2,ensure_ascii=False)+'\n```\n',
                '## Source and proof evidence\n','```json\n'+json.dumps({k:c.get(k) for k in ('source_citation','source_url','source_license','problem_family','split','theorem_verification')},indent=2,ensure_ascii=False)+'\n```\n',
                '## Reviewer instructions\n',
                'Check quantifiers, types, boundaries, notation, necessary and extra assumptions, '
                'self-containment, source adaptation, category/difficulty, family and split. '
                'Choose faithful / not faithful / uncertain. Record your actual identity, date, '
                'independence declaration, explanation, and a signed or otherwise verifiable '
                'decision artifact. Leave unreviewed items blank. Do not infer faithfulness '
                'from compilation or the supplied reference proof.\n',
                f'Binding SHA-256: `{token}`. Fill `{ident}.decision.json`; do not edit source fields.\n']
        (output/f'{ident}.md').write_text('\n'.join(chunks))
        index.append(f'- [{ident}]({ident}.md) — {r["category"]}; {c["split"]}; pending\n')
    (output/'README.md').write_text('\n'.join(index))


def check_artifact(spec: dict, base: Path) -> str:
    if not isinstance(spec,dict) or not isinstance(spec.get('path'),str):
        raise ValueError('An external evidence artifact and its SHA-256 are required.')
    path=(base/spec['path']).resolve()
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=spec.get('sha256'):
        raise ValueError('Evidence artifact is missing or its bytes changed.')
    return str(path)


def validate_decisions(records: list[dict], decisions: list[dict], registry: dict,
                       *, evidence_base: Path) -> list[dict]:
    if registry.get('status')!='human_verified' or not registry.get('verified_by'):
        raise ValueError('Reviewer identities must be genuinely verified by a human first.')
    check_artifact(registry.get('verification_artifact'),evidence_base)
    reviewers={r['id']:r for r in registry.get('reviewers',[])}
    by_id={r['id']:r for r in records};seen=set();validated=[]
    for d in decisions:
        ident=d.get('candidate_id'); reviewer=reviewers.get(d.get('reviewer_id'))
        if ident not in by_id or ident in seen:
            raise ValueError('Unknown or duplicate decision; disagreements require adjudication.')
        if d.get('schema_version')!=1 or d.get('review_type')!='semantic_fidelity':
            raise ValueError('Unsupported decision schema/type.')
        if d.get('binding_sha256')!=binding(by_id[ident]):
            raise ValueError('Review does not bind to the current English/Lean/imports/assumptions.')
        prior=by_id[ident]['curation'].get('semantic_fidelity',{})
        if prior.get('review_status')=='verified' and prior.get('label')!=d.get('label'):
            raise ValueError('Conflicting completed semantic review requires human adjudication.')
        if d.get('label') not in LABELS or not isinstance(d.get('evidence'),str) or not d['evidence'].strip():
            raise ValueError('An explicit label and substantive reviewer explanation are required.')
        if d.get('reviewer_kind')!='independent_human_review' or d.get('independence_attestation') is not True:
            raise ValueError('Independent human review attestation is required.')
        if not reviewer or reviewer.get('qualified_lean_reviewer') is not True:
            raise ValueError('Reviewer is not in the human-verified qualified Lean registry.')
        if reviewer['id'] in by_id[ident].get('author_ids',[]):
            raise ValueError('Author self-review cannot count as independent review.')
        try: reviewed=date.fromisoformat(d['reviewed_on'])
        except (ValueError,KeyError,TypeError) as error:
            raise ValueError('Reviewer date must be an ISO calendar date.') from error
        if reviewed>date.today():
            raise ValueError('Future review dates are invalid.')
        check_artifact(d.get('evidence_artifact'),evidence_base)
        seen.add(ident);validated.append(copy.deepcopy(d))
    return validated


def import_reviews(records: list[dict], decisions: list[dict], registry: dict,
                   output: Path, *, evidence_base: Path) -> None:
    validated=validate_decisions(records,decisions,registry,evidence_base=evidence_base)
    result=copy.deepcopy(records);by_id={r['id']:r for r in result}
    for d in validated:
        c=by_id[d['candidate_id']]['curation']
        c['semantic_fidelity']={'label':d['label'],'review_status':'verified',
                               'reviewer_provenance':d['reviewer_id'],'evidence':d['evidence']}
        c.setdefault('review_records',[]).append({'review_type':'semantic_fidelity',
            'reviewer_kind':'independent_human_review','reviewer_id':d['reviewer_id'],
            'reviewed_on':d['reviewed_on'],'evidence':d['evidence'],
            'decision_sha256':canonical_hash(d),'registry_sha256':canonical_hash(registry)})
    output.mkdir(parents=True,exist_ok=False)
    (output/'candidate_records.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    (output/'import_receipt.json').write_text(json.dumps({'status':'human_decisions_imported_not_dataset_frozen',
        'registry_sha256':canonical_hash(registry),'decisions':validated},indent=2)+'\n')


def semantic_success(compilation_success: bool, record: dict, decision: dict | None,
                     *, registry: dict | None = None, evidence_base: Path = Path('.')) -> bool:
    if not compilation_success or not decision or not registry:
        return False
    try:
        validated=validate_decisions([record],[decision],registry,evidence_base=evidence_base)
    except ValueError:
        return False
    return bool(validated and validated[0]['label']=='faithful')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--decisions',type=Path);p.add_argument('--reviewer-registry',type=Path);p.add_argument('--generated-results',type=Path);a=p.parse_args();records=load_candidates(a.root)
    if a.generated_results: records=generated_review_subjects(records,a.generated_results)
    if a.decisions:
        if not a.reviewer_registry: p.error('--reviewer-registry is required for import')
        import_reviews(records,json.loads(a.decisions.read_text()),json.loads(a.reviewer_registry.read_text()),a.output_dir,evidence_base=a.decisions.parent)
    else: prepare_packets(records,a.output_dir)

if __name__=='__main__': main()
