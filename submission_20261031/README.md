# Submission candidate and public evidence audit — 31 October 2026

This directory is a proposed submission candidate, not an alteration of the frozen experiment or supervisor-approved release. The 761-line author-supplied LaTeX is the baseline of main.tex, with one verified October 2026 related-work addition. Eight original tables, four original figure environments, three RQs, two appendices and five authentic cases remain. There are 20 bibliography entries: the prior 19 plus Li and Li.

## Public aggregate consistency workflow

From repository root, run:

    python -B submission_20261031/public_audit.py
    python -m unittest discover -s submission_20261031/tests -v
    python -B publication/reanalyze.py

The new script is read-only. It reads redacted released results and checks the public totals, 60 distinct targets, A=0/60, B=1/60, C=1/58 observed, exactly two unknown C outcomes (lib_a_trig_unit and lib_i_bernoulli), one jointly solved B/C target (lib_a_exp_add), and zero discordant B/C outcomes. It checks 410 physical completed calls, total input/output tokens 362035/130401, each matched arm's 230 completed calls on 58 targets, mean input 1980.9 (B) and 4353.5 (C), exact repetition 90/178 and 70/172, the recorded compiler-error stage counts and the archival 38-check reconciliation statement. This verifies public aggregate consistency only, NOT independent exact-byte reconstruction, model sampling, tokenizer recomputation or Lean verification.

IMPORTANT: publication/results/results.redacted.json uses 60 as C's missing-as-failure *sensitivity* denominator, with incomplete=2. Do not report that field as the 58-outcome primary observed rate.

## 5.66 versus 5.56: algorithmic provenance, not a changed experiment

The historical publication/docs/FINAL_EXPERIMENT_RESULTS.md and publication/paper/generated/review_v2/paired.tex use +5.66 percentage points as the upper bound of the complete-pair C−A 95% family-cluster bootstrap. The older implementation in publication/post_hoc/eval/final_review_analysis.py samples whole families with Python random.Random(20271021).choices and sorted integer-order-statistic bounds. Reexecuting that archived function against the same 60 public case entries returns upper=0.05660377358490566 (+5.66 points).

The later post-hoc publication/post_hoc/outputs/post_hoc/reproduced_run1/post_hoc_calibrated_null.json reports upper=0.05555555555555555 (+5.56 points); its statistics.py implementation uses NumPy default_rng(20271021) multinomial family weights and 0.025/0.975 quantiles of per-resample ratio-of-sums. Both draw 10,000 bootstrap replicates, but their random streams and quantile conventions differ. Neither alters the primary results. Preserve both historical outputs unchanged. The new manuscript's +5.56 is explicitly associated with the later archived post-hoc implementation and must not be called a newly replicated model outcome.

## Scientific scope and disclosure

This is one 4-bit Qwen2.5-7B local model, one primary seed, bounded repair attempts, B before C without randomization, and unequal token costs. Semantic types were AI-assisted screened, with zero independent human gold labels. The 2 missing C outcomes are unknown, not observed failed proofs. Post-hoc repetition, edit distance, compiler-stage transitions and development placebo do not demonstrate diagnostic comprehension or a causal mechanism. Fixed-type synthesis is not end-to-end natural-language-to-Lean formalization. Full original M1–M7 requirements were not completed (M1/M2/M3 partial); existing submission NO-GO gate for the full specification is not contradicted.

Related work now explicitly cites Jack Li and Sophia Li (15 October 2026), Repair, Retry, and the Cost of Hindsight: Verifier Feedback in Formal Theorem Proving, arXiv:2610.22698. The study does not claim priority for paired retries, diagnostic feedback or matched diagnostic controls; this is a resource-constrained negative/inconclusive pilot, not a comparable performance benchmark against Li and Li, APRIL or Baldur.

## Public release inventory and figure blockers

The latest manuscript references four genuine author-supplied PDF-extracted figures as fig1.png–fig4.png. These exact files are absent from the repository ZIP. This PR keeps the references as explicit unresolved build dependencies rather than silently substituting other source graphics. A self-contained clean-checkout production PDF requires the four legitimate source graphics to be provided or their mapping explicitly approved.

The uploaded ZIP / live default branch has two extra paths relative to its historical PUBLIC_PAYLOAD_MANIFEST.json: publication/post_hoc/analysis/manuscript_update_numbers.py and publication/post_hoc/outputs/post_hoc/manuscript_update_numbers.csv. The existing publication/verify_payload.py therefore fails its strict inventory membership check on the unmodified snapshot. This PR deliberately adds no files inside publication/ and does not rewrite historical manifests.

The venue advertises 12–15 pages recommended, not a verified hard limit. An earlier local recovered-figure build of the author-supplied source was 19 pages. Final page count, figure legibility, anonymity policy, licensed asset inclusion and supervisor approval remain author-review items. No submission, publication approval or reproducible end-to-end inference is claimed.
