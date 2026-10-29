"""Offline review-v2 regeneration from released redacted raw records; no inference."""
from collections import defaultdict
import datetime as dt
import json
import math
from pathlib import Path
import random
import statistics

ROOT=Path(__file__).resolve().parent
def read(path):return json.loads(path.read_text())


def main():
    expected=read(ROOT/'results/review_v2/analysis_verified/results.json')
    case_index=read(ROOT/'results/cases.json');cases=[];calls=[]
    for index in case_index:
        folder=ROOT/'evidence/redacted_runs/heldout/2027'/index['problem_id'];m=read(folder/'manifest.json')
        case={'problem_id':index['problem_id'],'family':index['family'],'outcomes':{c:m['conditions'][c]['success'] for c in ['A','B','C']},'milestones':{c:m['conditions'][c]['milestones'] for c in ['A','B','C']}}
        steps=[m['initial']]+[a for c in ['B','C'] for a in m['conditions'][c]['attempts']]
        for step in steps:
            f=folder/step['key'];raw=read(f/'completion.json');intent=read(f/'intent.json');md=raw['metadata']
            calls.append({'id':case['problem_id'],'key':step['key'],'prompt_tokens':md['prompt_tokens'],'completion_tokens':md['completion_tokens'],
                          'generation_seconds':md['latency_seconds'],'call_wall_seconds':(dt.datetime.fromisoformat(raw['finished_at'])-dt.datetime.fromisoformat(intent['started_at'])).total_seconds(),
                          'compiler_seconds':step['verification']['elapsed_seconds']})
        cases.append(case)
    assert len(cases)==60 and len(calls)==410
    for c in ['A','B','C']:
        observed=[r for r in cases if r['outcomes'][c] is not None];k=sum(r['outcomes'][c] for r in observed);target=expected['conditions'][c]
        assert target['observed_denominator']==len(observed) and target['successes']==k
        assert math.isclose(target['observed_rate'],k/len(observed))
        n=len(observed);z=1.959963984540054;p=k/n;scale=1+z*z/n
        center=(p+z*z/(2*n))/scale;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/scale
        for a,b in zip([max(0,center-half),min(1,center+half)],target['wilson_95_observed']):assert math.isclose(a,b,abs_tol=1e-12)
        selected=[a for a in calls if a['key']=='initial' or a['key'].startswith(c)]
        for key in ['prompt_tokens','completion_tokens','generation_seconds','call_wall_seconds','compiler_seconds']:
            values=[a[key] for a in selected];d=target['resources'][key]
            assert math.isclose(sum(values),d['sum'],abs_tol=1e-6)
            assert math.isclose(statistics.mean(values),d['mean'],abs_tol=1e-6)
            assert math.isclose(statistics.median(values),d['median'],abs_tol=1e-6)
    pairs=[]
    for first,second in [('C','B'),('C','A'),('B','A')]:
        group=[r for r in cases if all(r['outcomes'][c] is not None for c in [first,second])]
        diffs=[int(r['outcomes'][first])-int(r['outcomes'][second]) for r in group]
        target=next(v for v in expected['comparisons'] if v['comparison']==first+'_vs_'+second)
        assert len(group)==target['complete_pairs'] and statistics.mean(diffs)==target['risk_difference_complete_case']
        b=sum(d==1 for d in diffs);c=sum(d==-1 for d in diffs);n=b+c
        exact=None if n==0 else min(1,2*sum(math.comb(n,k) for k in range(min(b,c)+1))/(2**n))
        assert exact==target['exact_mcnemar_p']
        rng=random.Random(20271021);boot=sorted(statistics.mean(rng.choices(diffs,k=len(diffs))) for _ in range(10000))
        assert [boot[249],boot[9749]]==target['problem_bootstrap_95_complete_case']
        families=defaultdict(list)
        for r,d in zip(group,diffs):families[r['family']].append(d)
        rng=random.Random(20271021);cluster=[];names=list(families)
        for _ in range(10000):
            vals=[d for name in rng.choices(names,k=len(names)) for d in families[name]];cluster.append(statistics.mean(vals))
        cluster.sort();assert [cluster[249],cluster[9749]]==target['family_bootstrap_95_complete_case']
        pairs.append({'contrast':target['comparison'],'matched_cases':len(group),'risk_difference':statistics.mean(diffs),
                      'problem_interval':[boot[249],boot[9749]],'family_interval':[cluster[249],cluster[9749]]})
    complete=[r for r in cases if all(v is not None for v in r['outcomes'].values())]
    for c in ['A','B','C']:
        curve=[sum(any(v is True for k,v in r['milestones'][c].items() if int(k)<=budget) for r in complete)/len(complete) for budget in range(4)]
        assert curve==expected['paired_success_curves']['curves'][c]
    print(json.dumps({'valid':True,'cases':60,'completed_calls':410,'observed_rates':{c:expected['conditions'][c]['observed_rate'] for c in ['A','B','C']},
                     'paired_comparisons':pairs,'all_resource_sums_means_medians_match':True,
                     'missingness_bounds_C_minus_B':expected['comparisons'][0]['missingness_identification_bounds'],
                     'scope':'Public raw-view reanalysis of original outcomes/resources; exact private prompt replay is not claimed.'},indent=2))


if __name__=='__main__':main()
