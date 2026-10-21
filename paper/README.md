# TAIMMA 2027 paper draft

`main.tex` is a Springer LNCS-format pre-results manuscript. There was no
manuscript or bibliography in the repository before this draft was added.
Author and affiliation metadata remain unfilled. Tables generated from the
candidate inventory are not eligible-dataset results. A/B/C results and the
success-by-budget figure are deliberately unavailable until a frozen dataset
and validated paired API run artifacts exist.

## Build

Obtain the official Springer LNCS LaTeX proceedings template and place the
matching `llncs.cls` and `splncs04.bst` in the TeX search path. They are not
vendored here. Generate the data-derived inventory and manually authored
historical trace illustrations, then run LaTeX and BibTeX:

```sh
python paper/scripts/generate_inventory_tables.py
cd paper
pdflatex -halt-on-error main.tex
bibtex main
pdflatex -halt-on-error main.tex
pdflatex -halt-on-error main.tex
```

The candidate table and semantic-review inventory are generated from the
versioned candidate records. The qualitative trace snippets are extracted
from `data/results/attempts/*.jsonl` and are explicitly labeled as manual
historical diagnostics, not API outputs. Do not turn them into model results.

For a real results build, first freeze and validate the dataset, then run
`eval/paired_analysis.py` into a new output directory as documented in
`docs/experiment_protocol.md`; review its hashes and outputs before replacing
the manuscript's unavailable result sections. The analysis must never read
the held-out test set during model or prompt selection.

## Evidence status

See [`claims_to_evidence.md`](claims_to_evidence.md). Current status is not
submission-ready: there are zero eligible dataset records, no frozen split,
no independently approved/preregistered protocol, no qualifying paired API
runs, and no complete qualitative repair examples with authenticated API
provenance. Do not claim otherwise based on successful LaTeX formatting or
Lean compilation.
