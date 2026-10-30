"""Read-only post-hoc manuscript statistics from stored repair-level CSVs.

Run from publication/post_hoc: python -m analysis.manuscript_update_numbers
No model calls, experiment reruns, or modification of existing outputs.
"""
import csv
from pathlib import Path
from .statistics import bootstrap_difference

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/post_hoc'
TEST='outputs/post_hoc/post_hoc_repair_metrics.csv'
DEV='outputs/post_hoc/post_hoc_dev_repair_metrics.csv'
CODE='analysis/manuscript_update_numbers.py'

def load(path):
    with (ROOT/path).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def count(rows,arm,steps=None,field='identical'):
    eligible=[r for r in rows if r['condition']==arm
       and (steps is None or int(r['repair_index']) in steps)
       and r.get(field) not in ('',None)]
    return (sum(int(r[field]) for r in eligible),len(eligible))

def main():
    test,dev=load(TEST),load(DEV)
    assert count(test,'B')==(90,178) and count(test,'C')==(70,172)
    assert count(dev,'C')==(23,45) and count(dev,'C_placebo')==(32,45)
    first=[dict(r,identical=int(r['identical'])) for r in test
           if int(r['repair_index'])==1]
    boot=bootstrap_difference(first,'identical',unit='family',
        conditions=('B','C'),resamples=10000,seed=20271021)
    assert boot['estimable'] and boot['valid_resamples']==10000
    rows=[]
    def entry(name,arm,source,steps=None,field='identical',note=''):
        k,n=count(test if source==TEST else dev,arm,steps,field)
        if not n:raise ValueError('Empty denominator: '+name+'/'+arm)
        rows.append(dict(metric=name,condition=arm,numerator=k,denominator=n,
            percent=f'{k/n*100:.5f}',contrast_c_minus_b_pp='',
            family_bootstrap_low_pp='',family_bootstrap_high_pp='',
            code_path=CODE,source_path=source,notes=note))
    for arm in ('B','C'):
        entry('test_first_repair_identical',arm,TEST,{1},
              note='Completed repairs only; two unavailable C first repairs excluded')
        entry('test_repairs_2_3_identical',arm,TEST,{2,3},
              note='Different branch predecessor candidates after step 1')
    for arm in ('B','C','C_placebo'):
        entry('dev_identical',arm,DEV,note='15 development problems; five families; one seed')
        entry('dev_unknown_name_removal',arm,DEV,field='any_unknown_removed',
              note='Analyst-only; B never saw diagnostics' if arm=='B'
                   else 'Syntactic disappearance, not certified proof repair')
    b,nb=count(test,'B',{1});c,nc=count(test,'C',{1})
    difference=100*(c/nc-b/nb)
    assert abs(difference-100*boot['difference'])<1e-10
    rows.append(dict(metric='test_first_repair_C_minus_B',condition='C-B',
       numerator='',denominator=f'B:{nb};C:{nc}',percent='',
       contrast_c_minus_b_pp=f'{difference:.5f}',
       family_bootstrap_low_pp=f'{100*boot["interval"][0]:.5f}',
       family_bootstrap_high_pp=f'{100*boot["interval"][1]:.5f}',
       code_path=CODE,source_path=TEST,
       notes='10,000 multinomial whole-family resamples; seed 20271021; post-hoc unadjusted CI'))
    b,nb=count(test,'B',{2,3});c,nc=count(test,'C',{2,3})
    rows.append(dict(metric='test_repairs_2_3_C_minus_B',condition='C-B',
       numerator='',denominator=f'B:{nb};C:{nc}',percent='',
       contrast_c_minus_b_pp=f'{100*(c/nc-b/nb):.5f}',
       family_bootstrap_low_pp='',family_bootstrap_high_pp='',
       code_path=CODE,source_path=TEST,
       notes='Descriptive; different predecessor candidates'))
    target=OUT/'manuscript_update_numbers.csv'
    if target.exists():raise FileExistsError('Refusing to overwrite existing output')
    with target.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(target)

if __name__=='__main__':main()
