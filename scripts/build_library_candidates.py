"""Prepare attributed, unreviewed library-derived candidates from actual Lean evidence.

Never labels human review, source compatibility or split eligibility approved.
The verification JSON and exact reference-source hash must already pass.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from verify import _diagnostics, _axioms_from_diagnostics, DEFAULT_POLICY, _find_prohibited_source

REV='81a5d257c8e410db227a6665ed08f64fea08e997'
LEAN_REV='8c9756b28d64dab099da31a4c09229a9e6a2ef35'
MATH=ROOT/'lean_project/.lake/packages/mathlib'
LEAN=Path.home()/'.elan/toolchains/leanprover--lean4---v4.32.0/src/lean'

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# Resolve overloaded formal names to the mathematical domains used by each record.
OVERRIDES={
'q_rational_density':('Mathlib/Algebra/Order/Archimedean/Basic.lean',372),
'q_rearrangement':('Mathlib/Algebra/Order/Ring/Unbundled/Basic.lean',294),
'q_pigeonhole':('Mathlib/Data/Finset/Card.lean',451),
'd_prime_factor_exists':('Mathlib/Data/Nat/Prime/Defs.lean',407),
'd_euclidean_gcd':('Init/Data/Nat/Gcd.lean',74),
'i_stirling':('Mathlib/Combinatorics/Enumerative/Stirling.lean',144),
'i_catalan':('Mathlib/Combinatorics/Enumerative/Catalan/Basic.lean',61),
'a_power_add':('Mathlib/Algebra/Group/Defs.lean',733),
'a_euclidean':('Init/Data/Int/DivMod/Bootstrap.lean',100),
'a_abs_product':('Mathlib/Algebra/Order/Ring/Abs.lean',49),
'a_sqrt_square':('Mathlib/Analysis/Real/Sqrt.lean',178),
'a_truncated_sub':('Init/Data/Nat/Basic.lean',991),
'a_inverse_difference':('Mathlib/Algebra/Field/Basic.lean',187),
'a_gcd_lcm':('Init/Data/Nat/Lcm.lean',38),
'd_euclid':('Mathlib/Data/Nat/Prime/Defs.lean',422),
'd_bezout':('Mathlib/Data/Int/GCD.lean',172),
'd_prime_factorial':('Mathlib/Data/Nat/Prime/Factorial.lean',23),
'd_dvd_antisymmetry':('Init/Data/Nat/Dvd.lean',76),
'i_fibonacci':('Mathlib/Data/Nat/Fib/Basic.lean',75),
'i_vandermonde':('Mathlib/Data/Nat/Choose/Vandermonde.lean',31),
'q_triangle':('Mathlib/Algebra/Order/Group/Unbundled/Abs.lean',125),
'q_sqrt_monotone':('Mathlib/Analysis/Real/Sqrt.lean',209),
'q_quotient':('Init/Data/Nat/Div/Basic.lean',71),
'm_cancel':('Mathlib/Data/Nat/ModEq.lean',378),
'm_power':('Mathlib/Data/Int/ModEq.lean',0),
'm_gcd_obstruction':('Mathlib/Data/Int/ModEq.lean',109),
'm_residue_product':('Init/Data/Nat/Lemmas.lean',810),
'a_log_product':('Mathlib/Analysis/SpecialFunctions/Log/Basic.lean',132),
'a_exp_add':('Mathlib/Analysis/Complex/Exponential.lean',209),
'a_min_max':('Mathlib/Algebra/Order/Monoid/Unbundled/MinMax.lean',38),
'd_factorization':('Mathlib/Data/Nat/Factorization/Defs.lean',155),
'i_telescope':('Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean',896),
'q_finite_inclusion':('Mathlib/Data/Finset/Card.lean',66),
'm_euler':('Mathlib/FieldTheory/Finite/Basic.lean',564),
}
ALIASES={'q_triangle':'Additive counterpart abs_add_le generated from mabs_mul_le by to_additive.',
'a_min_max':'Additive counterpart min_add_max generated from min_mul_max by to_additive.',
'i_telescope':'Additive counterpart Finset.sum_range_sub generated from prod_range_div by to_additive.'}

def build(batch: Path):
    specs=json.loads((batch/'specifications.json').read_text())
    result=json.loads((batch/'verification_expanded.json').read_text());source=batch/'references_expanded.lean'
    if result['exit_code']!=0 or result['source_sha256']!=digest(source):raise ValueError('Reference batch did not verify or changed.')
    messages,malformed=_diagnostics(result['stdout'])
    if malformed or any(m['severity']=='error' for m in messages): raise ValueError('Compiler evidence is malformed or contains errors.')
    if _find_prohibited_source(source.read_text(),False,DEFAULT_POLICY):raise ValueError('Reference source contains a forbidden shortcut.')
    locator={}
    pattern=re.compile(r'\b(?:theorem|lemma|def)\s+([^\s(:]+)')
    wanted={r[6].split('.')[-1] for r in specs}
    for root in [MATH/'Mathlib',LEAN/'Init']:
        for p in root.rglob('*.lean'):
            for line,text in enumerate(p.read_text().splitlines(),1):
                m=pattern.search(text)
                if m and m[1].split('.')[-1] in wanted:locator.setdefault(m[1].split('.')[-1],[]).append((p,line,m[1]))
    archive=batch/'source_archive';archive.mkdir(exist_ok=False)
    for filename,original in [('MATHLIB_LICENSE',MATH/'LICENSE'),('LEAN_LICENSE',LEAN.parents[1]/'LICENSE')]:
        (archive/filename).write_bytes(original.read_bytes())
    template=json.loads((ROOT/'data/curation_batches/v0.1.8/candidate_records.json').read_text())[0]
    records=[];source_entries=[]
    for ident,category,family,english,signature,proof,hint in specs:
        if ident in OVERRIDES:
            relative,line=OVERRIDES[ident];p=(MATH if relative.startswith('Mathlib/') else LEAN)/relative
            if line==0:
                lines=p.read_text().splitlines();line=next(i for i,s in enumerate(lines,1) if re.search(r'(theorem|lemma).*\bpow\b',s))
        else:
            options=locator.get(hint.split('.')[-1],[])
            if not options:raise ValueError(f'No exact source declaration found for {ident}: {hint}')
            if ident=='a_trig_unit':options=[v for v in options if 'Trigonometric' in str(v[0])]
            p,line,_=options[0]
            relative=str(p.relative_to(MATH if p.is_relative_to(MATH) else LEAN))
        blob=p.read_bytes();sha=hashlib.sha256(blob).hexdigest();archived=archive/(sha[:12]+'_'+p.name)
        if not archived.exists():archived.write_bytes(blob)
        is_math=p.is_relative_to(MATH);rev=REV if is_math else LEAN_REV;repository='leanprover-community/mathlib4' if is_math else 'leanprover/lean4';prefix='' if is_math else 'src/lean/'
        url=f'https://github.com/{repository}/blob/{rev}/{prefix}{relative}#L{line}'
        if f'theorem study_{ident} {signature} := by\n  {proof}' not in source.read_text():
            raise ValueError('Candidate specification differs from actually compiled source.')
        statement='open scoped BigOperators\ntheorem study_'+ident+' '+signature
        reference='import Mathlib\n'+statement+' := by\n  '+proof+'\n'
        axioms=_axioms_from_diagnostics(messages,'study_'+ident)
        if axioms is None or set(axioms)-set(DEFAULT_POLICY.allowed_axioms):raise ValueError(f'Unapproved/missing axiom evidence for {ident}.')
        r=copy.deepcopy(template);r.update(id='lib_'+ident,nl_statement=english,expected_lean_statement=statement,category=category,difficulty=2 if len(signature)<160 else 3,difficulty_rationale='Provisional library-derived rating; reference reuse is not generated-model difficulty evidence.',source_item_id=hint,source_location=f'{relative}:{line}',required_imports=['Mathlib'],mathematical_assumptions='Exact binders/hypotheses: '+signature.split(' : ',1)[0],reference_lean_code=reference)
        c=r['curation'];c.update(source_url=url,source_citation=f'{repository} at {rev}, {relative}:{line}, formal item {hint}. English is a new author-assisted paraphrase/adaptation, not a source quotation.',source_status='verified',source_license='Apache-2.0',source_license_verification_status='needs_review',problem_family=family,family_review_status='needs_review',family_review_note='Provisional mathematical family; independent cross-pool review must check generalizations and source overlap before counting independence.',split='test',split_status='pending')
        c['source_license_evidence']={'status':'needs_review','evidence_reference':str(archive/('MATHLIB_LICENSE' if is_math else 'LEAN_LICENSE')),'observed_on':'2026-10-27','reviewed_on':None,'statement_sha256':hashlib.sha256(statement.encode()).hexdigest(),'rights_note':'Repository license and original copyright headers archived. Independent item-scope, redistribution and model-input review pending.'}
        c['source_metadata']={'source_author':'The mathlib community / Lean contributors; see archived file copyright header','source_title':repository,'source_item_id':hint,'source_location':r['source_location'],'revision':rev,'source_page_archive':str(archived),'source_page_sha256':sha,'source_page_sha256_status':'captured_pinned_source_bytes','source_statement_transcription':None,'original_english_statement':None,'english_provenance':'Codex-authored mathematical paraphrase of formal source; independent semantic review pending.','changes_made':ALIASES.get(ident,'Specialized source statement or derived consequence to the displayed domains. See explicit reference proof and exact source declaration; English was authored for review.'),'required_attribution':f'{repository}, revision {rev}; Apache-2.0; original authors/copyright in archived source.','retrieved_on':'2026-10-27'}
        c['reference_lean_statement_provenance']='Prepared from cited pinned formal source; exact displayed proposition verified in the complete reference batch.'
        c['proposed_split_rationale']='New candidate only, provisionally reserved for test curation; not evaluated with an LLM or used for model/prompt selection. Review and freeze required.'
        c['theorem_verification']={'status':'verified','success':True,'verification_scope':'strict_proof','lean_toolchain':'leanprover/lean4:v4.32.0','mathlib_revision':REV,'command':result['command'],'theorem_sha256':hashlib.sha256(statement.encode()).hexdigest(),'reference_code_sha256':hashlib.sha256(reference.encode()).hexdigest(),'verification_source_sha256':result['source_sha256'],'axiom_dependencies':axioms,'evidence':str(batch/'verification_expanded.json')+'; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs.'}
        records.append(r);source_entries.append({'candidate_id':r['id'],'source_url':url,'source_archive':str(archived),'sha256':sha,'item':hint,'line':line})
    path=batch/'candidate_records.json'
    with path.open('x') as stream:stream.write(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    (batch/'batch_manifest.json').write_text(json.dumps({'status':'unreviewed_candidates_not_frozen','candidate_count':len(records),'strict_proof_verified_count':len(records),'eligible_count':0,'candidate_file_sha256':digest(path),'reference_source_sha256':digest(source),'verification_sha256':digest(batch/'verification_expanded.json'),'sources':source_entries,'independence_status':'proposed_families_require_review_not_established','inference_calls_on_candidates':0},indent=2)+'\n')
    print(f'Prepared {len(records)} attributed, proof-verified, unreviewed candidates; no eligibility promotion.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',type=Path,required=True);build(p.parse_args().batch)
