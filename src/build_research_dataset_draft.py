"""Build the versioned, explicitly pending research-dataset curation draft."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from dataset_validation import validate_curation_draft


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "seed_problems.json"
VERSION = "nl2lean-repair-v0.1.0-draft"
OUTPUTS = {
    "dataset": ROOT / "data" / "research_dataset_draft_v0.1.0.json",
    "ledger": ROOT / "data" / "curation_ledger_v0.1.0.json",
    "manifest": ROOT / "data" / "research_dataset_manifest_v0.1.0.json",
}

FAMILY_PROPOSALS: dict[str, tuple[str, str, str]] = {
    "arith_001": (
        "nat_square_identities",
        "development",
        "Natural-number square identities; keep related algebraic variants together.",
    ),
    "arith_002": (
        "nat_square_identities",
        "development",
        "Natural-number square and difference-of-squares identity.",
    ),
    "arith_004": (
        "nat_square_identities",
        "development",
        "Natural-number square identity using truncated subtraction.",
    ),
    "div_001": (
        "nat_square_identities",
        "development",
        "Parity property of a natural-number square.",
    ),
    "div_005": (
        "nat_square_identities",
        "development",
        "Parity property of a natural-number square.",
    ),
    "div_006": (
        "nat_square_identities",
        "development",
        "Converse/equivalence variant of natural-number square parity.",
    ),
    "ineq_001": (
        "nat_square_identities",
        "development",
        "Natural-number lower bound involving a square.",
    ),
    "div_002": (
        "nat_parity_products",
        "test",
        "Parity result for product of consecutive natural numbers.",
    ),
    "div_004": (
        "nat_parity_products",
        "test",
        "Parity result for a sum of odd natural numbers.",
    ),
    "div_003": (
        "nat_divisibility_factorization",
        "test",
        "Single divisibility implication; singleton family proposal.",
    ),
    "mod_001": (
        "integer_congruence_translation",
        "test",
        "Congruence preserved by translation; singleton family proposal.",
    ),
    "mod_002": (
        "square_residue_classes",
        "test",
        "Square residue class theorem; related residue theorem grouped.",
    ),
    "mod_003": (
        "square_residue_classes",
        "test",
        "Square residue class theorem over naturals; grouped conservatively.",
    ),
    "ind_001": (
        "nat_finite_sum_identities",
        "development",
        "Finite sum identity over a natural-number range.",
    ),
    "ind_002": (
        "nat_finite_sum_identities",
        "development",
        "Finite sum identity over a natural-number range.",
    ),
    "ind_004": (
        "nat_finite_sum_identities",
        "development",
        "Geometric finite sum claim; definition/self-containment is unresolved.",
    ),
    "ind_003": (
        "nat_power_growth",
        "development",
        "Exponential growth comparison over natural numbers.",
    ),
    "ineq_003": (
        "nat_power_growth",
        "development",
        "Related exponential upper-bound theorem over natural numbers.",
    ),
    "arith_003": (
        "nat_distributivity",
        "development",
        "Natural-number distributivity statement.",
    ),
    "arith_003_mathlib": (
        "nat_distributivity",
        "development",
        "Exact English duplicate and propositionally identical distributivity candidate.",
    ),
    "ineq_002": (
        "nat_product_bound",
        "development",
        "Natural-number product lower/upper bound; singleton family proposal.",
    ),
}

AUDIT_NOTES: dict[str, tuple[str, str]] = {
    "arith_001": (
        "No record-specific discrepancy established from the pair alone; theorem meaning and reference provenance remain unreviewed.",
        "Have a Lean/math reviewer compare the universal natural-number identity with the English statement and record evidence.",
    ),
    "arith_002": (
        "The English condition 'a is at least b' corresponds to Lean hypothesis b ≤ a; natural subtraction semantics still require review.",
        "Confirm the hypothesis is sufficient and that the intended subtraction is natural-number truncated subtraction.",
    ),
    "div_001": (
        "English 'even' is represented by Lean's Even predicate; required import/context and semantic correspondence remain unreviewed.",
        "Review the Even definition/import context and theorem statement against the English claim.",
    ),
    "div_002": (
        "The English parity claim is represented using Even; no source or independent theorem review is recorded.",
        "Verify the intended product ordering and that the Lean Even predicate matches the wording.",
    ),
    "div_003": (
        "The conjunction in Lean corresponds to 'both'; source provenance and theorem review are absent.",
        "Verify divisibility conventions and the reference theorem, then record a source and review evidence.",
    ),
    "mod_001": (
        "English explicitly says m is positive, but the Lean statement has no positivity hypothesis. The congruence claim may be stronger; fidelity is unresolved.",
        "Decide whether positivity is essential to the intended English statement; amend only after human approval and record the decision.",
    ),
    "mod_002": (
        "Integer remainder convention for negative inputs is not stated in English; the Lean expression uses integer remainder modulo 4.",
        "Review the intended congruence/remainder convention, especially for negative integers, and confirm exact equivalence.",
    ),
    "ind_001": (
        "English says the sum equals a quotient, while Lean states a doubled-sum identity over range (n + 1); indexing and natural division are implicit.",
        "Review the range endpoints and algebraic equivalence, then rewrite the English wording or Lean statement if needed.",
    ),
    "ind_002": (
        "The English description 'first n odd numbers' depends on an indexing convention; Lean uses range n and terms 2*i+1.",
        "Confirm the zero-based enumeration and that the resulting sum is the intended one.",
    ),
    "ind_003": (
        "The Lean inequality n < 2^n corresponds to 'greater than n'; theorem assumptions and boundary case still need review.",
        "Check boundary cases and document theorem-statement and fidelity review.",
    ),
    "div_004": (
        "Oddness is encoded using witnesses a = 2*i+1 and b = 2*j+1 rather than the Even/Odd predicates.",
        "Confirm witness formulation, natural-number multiplication notation, and fidelity to ordinary oddness.",
    ),
    "ineq_001": (
        "The universal natural-number inequality has no explicit lower-bound assumption; its n = 0 boundary is relevant to human review.",
        "Check all boundary cases and compare the natural-number theorem with the English universal claim.",
    ),
    "arith_003": (
        "This record has an exact-English duplicate candidate, arith_003_mathlib, with a different theorem name.",
        "Adjudicate the duplicate group; do not count both as independent test examples.",
    ),
    "arith_003_mathlib": (
        "This record has an exact-English duplicate candidate, arith_003, with the same proposition under another theorem name.",
        "Adjudicate whether this is an environment variant or duplicate; retain family grouping and exclude duplicate count unless justified.",
    ),
    "arith_004": (
        "The English condition b ≤ a is present in Lean, but the equation uses natural subtraction and requires semantic review.",
        "Check truncated subtraction and verify the condition captures the intended algebraic identity.",
    ),
    "div_005": (
        "Oddness is encoded by an existential witness equation; the English uses the ordinary-language predicate.",
        "Review equivalence of the witness encoding and confirm imported arithmetic definitions.",
    ),
    "div_006": (
        "Both directions use existential evenness encodings; no explicit family or reference review is recorded.",
        "Verify the iff theorem, witness encodings, and natural-number boundary cases.",
    ),
    "ineq_002": (
        "The English phrase 'at most' maps to ≤; the expanded product and boundary cases have not been reviewed.",
        "Check the quantified statement and boundary cases, then record review provenance.",
    ),
    "ineq_003": (
        "English 'at least 1' maps to h : 1 ≤ n; confirm the bound and exponential claim at the smallest permitted n.",
        "Review the assumption and boundary case, then record theorem/fidelity decisions.",
    ),
    "ind_004": (
        "Lean statement references geomSum n, but no definition for geomSum is present in the dataset record; self-containment is unestablished.",
        "Locate and cite the intended definition or replace the statement with a self-contained Finset/closed-form expression after review.",
    ),
    "mod_003": (
        "English describes congruence modulo 3; Lean states a Nat remainder disjunction. The remainder convention and correspondence need review.",
        "Confirm the intended canonical remainder semantics and assess relation to mod_002 as a family, not as an assumed duplicate.",
    ),
}


def _review_object(note: str) -> dict[str, Any]:
    return {
        "status": "pending",
        "reviewer_provenance": None,
        "review_notes": note,
    }


def _curation_record(problem_id: str) -> dict[str, Any]:
    family, split, family_note = FAMILY_PROPOSALS[problem_id]
    note, action = AUDIT_NOTES[problem_id]
    duplicate_group = (
        "exact_english_duplicate_arith_003"
        if problem_id in {"arith_003", "arith_003_mathlib"}
        else None
    )
    duplicate_status = "needs_review" if duplicate_group else "pending"
    related_duplicate_ids = (
        ["arith_003_mathlib"]
        if problem_id == "arith_003"
        else ["arith_003"]
        if problem_id == "arith_003_mathlib"
        else []
    )
    return {
        "source_url": None,
        "source_citation": None,
        "source_status": "pending",
        "source_license": None,
        "source_license_verification_status": "pending",
        "problem_family": family,
        "family_review_status": "needs_review",
        "family_review_note": family_note,
        "split": split,
        "split_status": "pending",
        "semantic_fidelity": {
            "label": None,
            "review_status": "pending",
            "reviewer_provenance": None,
            "evidence": None,
        },
        "theorem_statement_review": _review_object(note),
        "assumption_mismatch_review": _review_object(note),
        "self_containment_review": _review_object(note),
        "duplicate_review": {
            "candidate_group": duplicate_group,
            "related_ids": related_duplicate_ids,
            "status": duplicate_status,
            "notes": note if duplicate_group else None,
        },
        "recommended_curator_action": action,
    }


def _eligible_counts(
    records: list[dict[str, Any]],
) -> tuple[int, dict[str, int]]:
    report = validate_curation_draft(records)
    eligible_ids = set(report.eligible_problem_ids)
    eligible_split_counts = Counter(
        record["curation"]["split"]
        for record in records
        if record.get("id") in eligible_ids
        and record.get("curation", {}).get("split") in {"development", "test"}
    )
    return len(report.eligible_problem_ids), {
        split: eligible_split_counts.get(split, 0)
        for split in ("development", "test")
    }


def build() -> None:
    existing_outputs = [path for path in OUTPUTS.values() if path.exists()]
    if existing_outputs:
        names = ", ".join(str(path.relative_to(ROOT)) for path in existing_outputs)
        raise FileExistsError(f"Refusing to overwrite existing draft artifacts: {names}")

    source_records = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(source_records, list):
        raise ValueError("Seed dataset must be a JSON array.")

    records: list[dict[str, Any]] = []
    ledger_records: list[dict[str, Any]] = []
    for source_record in source_records:
        record = dict(source_record)
        problem_id = record["id"]
        record["curation"] = _curation_record(problem_id)
        records.append(record)
        family, split, family_rationale = FAMILY_PROPOSALS[problem_id]
        audit_note, recommended_action = AUDIT_NOTES[problem_id]
        duplicate_group = record["curation"]["duplicate_review"]["candidate_group"]
        ledger_records.append(
            {
                "id": problem_id,
                "candidate_status": "review_pending",
                "source_and_license": {
                    "status": "pending",
                    "evidence": "No source or license evidence is recorded in the source seed record; none was added by this offline curation pass.",
                    "recommended_action": "Identify the original source or document verified hand-authored provenance, then verify applicable rights/license.",
                },
                "family_proposal": {
                    "id": family,
                    "status": "needs_review",
                    "rationale": family_rationale,
                },
                "split_proposal": {
                    "split": split,
                    "status": "pending",
                    "method": "Deterministic, explicit family map in src/build_research_dataset_draft.py; not a frozen assignment.",
                },
                "duplicate_candidate_group": duplicate_group,
                "audit_finding": audit_note,
                "recommended_curator_action": recommended_action,
                "human_review_status": "pending",
            }
        )

    dataset_bytes = (
        json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    dataset_hash = hashlib.sha256(dataset_bytes).hexdigest()
    categories = Counter(record["category"] for record in records)
    split_counts = Counter(record["curation"]["split"] for record in records)
    eligible_record_count, eligible_split_counts = _eligible_counts(records)
    review_completion_counts: dict[str, dict[str, int]] = {}
    for field in (
        "source_status",
        "source_license_verification_status",
        "family_review_status",
        "split_status",
    ):
        review_completion_counts[field] = dict(
            Counter(record["curation"][field] for record in records)
        )
    for field in (
        "semantic_fidelity",
        "theorem_statement_review",
        "assumption_mismatch_review",
        "self_containment_review",
        "duplicate_review",
    ):
        review_completion_counts[field] = dict(
            Counter(
                (
                    record["curation"][field]["review_status"]
                    if field == "semantic_fidelity"
                    else record["curation"][field]["status"]
                )
                for record in records
            )
        )

    manifest = {
        "dataset_version": VERSION,
        "status": "draft",
        "not_frozen": True,
        "record_count": len(records),
        "ordered_ids": [record["id"] for record in records],
        "dataset_sha256": dataset_hash,
        "proposed_split_counts": {
            split: split_counts.get(split, 0)
            for split in ("development", "test")
        },
        "eligible_record_count": eligible_record_count,
        "eligible_split_counts": eligible_split_counts,
        "category_counts": dict(sorted(categories.items())),
        "duplicate_review_status": "unresolved_candidate_requires_human_review",
        "duplicate_candidate_groups": [
            {
                "candidate_group": "exact_english_duplicate_arith_003",
                "ids": ["arith_003", "arith_003_mathlib"],
                "status": "needs_review",
                "independent_example_count": 1,
            }
        ],
        "review_completion_counts": review_completion_counts,
        "family_split_rule": "All records with the same proposed problem_family are assigned to the same proposed split; family assignments remain pending human review.",
        "source_dataset": "data/seed_problems.json",
        "source_dataset_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    }
    ledger = {
        "dataset_version": VERSION,
        "status": "draft",
        "policy": "No source, license, theorem review, semantic-fidelity label, or family decision is asserted without evidence. All original seed records and IDs are retained.",
        "record_audits": ledger_records,
        "family_proposals": [
            {
                "problem_family": family,
                "split": split,
                "member_ids": [
                    record["id"]
                    for record in records
                    if record["curation"]["problem_family"] == family
                ],
                "status": "needs_review",
                "rationale": rationale,
            }
            for family, split, rationale in sorted(
                {
                    (
                        record["curation"]["problem_family"],
                        record["curation"]["split"],
                        record["curation"]["family_review_note"],
                    )
                    for record in records
                }
            )
        ],
    }
    outputs = {
        "dataset": dataset_bytes,
        "ledger": (json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode(
            "utf-8"
        ),
        "manifest": (
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8"),
    }
    for name, path in OUTPUTS.items():
        with path.open("xb") as output:
            output.write(outputs[name])


if __name__ == "__main__":
    build()
