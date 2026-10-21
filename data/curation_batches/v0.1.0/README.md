# Curation batch v0.1.0

## Scope and source

This is the first candidate batch, kept separate from the existing 21-record
research draft. It contains three statements from Oscar Levin, *Discrete
Mathematics: An Open Introduction*, 3rd edition, 5th printing (2021), under
CC BY-SA 4.0. The source PDF identifies its edition, printing, license, and
undergraduate audience in its front matter. The official edition page confirms
the license and permits modification and redistribution with attribution.
The adapted candidate wording, Lean statements, and associated batch data are
released under CC BY-SA 4.0 to meet the source's share-alike condition.

Source URL: https://discrete.openmathbooks.org/pdfs/dmoi3-tablet.pdf
Edition/license page: https://discrete.openmathbooks.org/dmoi3.html
Retrieved and checked: 2026-10-21

## Candidate list

- `div_007`: section 3.2 exposition, printed page 218, claim that the sum of
two even integers is even.
- `div_008`: exercise 3.2.5, printed page 223, equivalence between evenness
of an integer and of three times that integer.
- `div_009`: example 3.2.11, printed page 222, evenness of `n^3 - n`.

All three use a provisional `development` split field and the conservative
family `integer_parity`; neither is approved. Existing draft candidates
`div_001`, `div_004`, and `div_006` are related-family leads, and their proposed
splits currently fall on both sides. Keep every split decision pending until
independent family review resolves the overlap; do not use these proposals as
a test set. These records are not eligible.

## Evidence status

The source edition and its CC BY-SA 4.0 terms were checked against the cited
PDF and official edition page. Candidate source-statement hashes and exact
Lean-statement hashes are in the JSON batch. All three Lean files compiled under
the pinned repository toolchain/Mathlib revision using the commands recorded
in each candidate's `curation.theorem_verification` field. This compilation
establishes only that Lean accepts these formal statements; it is not a
semantic-fidelity review.

No independent reviewer is recorded. Semantic fidelity, theorem-statement,
assumption-mismatch, self-containment, family, split, and duplicate reviews
remain pending. These three records contribute zero eligible examples.

## Actual implementation sequence

1. Preserve the existing draft, manifest, and experiment artifacts.
2. Pin an edition and inspect its item-level statements and license terms.
3. Add sourced candidates and separate Lean files in this batch directory.
4. Compile each Lean file and store command/output and hashes.
5. Run the curation-draft validator and focused dataset-validation tests.
6. Leave review-dependent statuses pending and keep the batch separate until
   independent review and family/split decisions exist.
