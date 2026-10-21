"""Generate paper inventory tables and historical trace illustrations.

These outputs are dataset-construction/audit material, not A/B/C results.
"""
from __future__ import annotations

import json
import difflib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / "generated"


def tex_escape(value: str) -> str:
    substitutions = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(substitutions.get(char, char) for char in value)


def code_excerpt(value: str) -> str:
    lines = value.splitlines() or [""]
    return "\n".join(tex_escape(line[:108] + ("..." if len(line) > 108 else "")) + r"\\" for line in lines[:8])


def read_candidates() -> list[dict]:
    records = json.loads((ROOT / "data/research_dataset_draft_v0.1.0.json").read_text())
    for path in sorted((ROOT / "data/curation_batches").glob("*/candidate_records.json")):
        records.extend(json.loads(path.read_text()))
    ids = [record.get("id") for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Candidate IDs are not unique across the current inventory.")
    return records


def candidate_table(records: list[dict]) -> str:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        curation = record.get("curation", {})
        split = curation.get("split", "unassigned") if isinstance(curation, dict) else "unassigned"
        grouped[(str(split), str(record.get("category", "unknown")))].append(record)
    rows = []
    for (split, category), group in sorted(grouped.items()):
        difficulty = Counter(str(r.get("difficulty", "?")) for r in group)
        source_cited = sum(bool(r.get("curation", {}).get("source_citation") or r.get("curation", {}).get("source_url") or r.get("curation", {}).get("source_metadata")) for r in group)
        rows.append(
            f"{tex_escape(split)} & {tex_escape(category)} & {len(group)} & "
            f"{difficulty.get('1', 0)}/{difficulty.get('2', 0)}/{difficulty.get('3', 0)}/{difficulty.get('4', 0)} & "
            f"{source_cited} & {len(group) - source_cited} & 0 \\\\"
        )
    total = len(records)
    cited_total = sum(bool(r.get("curation", {}).get("source_citation") or r.get("curation", {}).get("source_url") or r.get("curation", {}).get("source_metadata")) for r in records)
    dev = sum(str(r.get("curation", {}).get("split")) == "development" for r in records)
    test = sum(str(r.get("curation", {}).get("split")) == "test" for r in records)
    rows.append(r"\midrule")
    rows.append(f"Total & All categories & {total} & -- & {cited_total} & {total - cited_total} & 0 \\\\")
    rows.append(r"\multicolumn{7}{l}{Proposed split totals: development=" + str(dev) + ", test=" + str(test) + r"; eligible total=0.} \\")
    return "\n".join([
        r"\begin{tabular}{llrrrrr}", r"\toprule",
        r"Proposed split & Category & Candidates & Difficulty 1/2/3/4 & Cited & No item citation & Eligible\\",
        r"\midrule", *rows, r"\bottomrule", r"\end{tabular}",
    ])


def semantic_table(records: list[dict]) -> str:
    counts = Counter()
    for record in records:
        curation = record.get("curation", {})
        value = curation.get("semantic_fidelity", {}) if isinstance(curation, dict) else {}
        label = value.get("label") if isinstance(value, dict) else None
        status = value.get("review_status") if isinstance(value, dict) else None
        if status == "verified" and label in {"faithful", "not faithful", "uncertain"}:
            counts[label] += 1
        else:
            counts["pending/unreviewed"] += 1
    rows = [r"\begin{tabular}{lr}", r"\toprule", r"Review state & Candidate count\\", r"\midrule"]
    for label in ("faithful", "not faithful", "uncertain", "pending/unreviewed"):
        rows.append(f"{label} & {counts[label]} \\\\")
    rows.extend([r"\midrule", "Eligible frozen test records & 0 " + r"\\", r"\bottomrule", r"\end{tabular}"])
    return "\n".join(rows)


def historical_examples() -> str:
    selected = ("arith_001", "arith_004", "arith_003", "ineq_001", "mod_002")
    blocks = [r"\noindent\textbf{Evidence note.} These are manual historical trace slices; `success` below means only the saved attempt record's compiler-verification outcome. No API provenance is claimed."]
    for problem_id in selected:
        path = ROOT / "data/results/attempts" / f"{problem_id}.jsonl"
        attempts = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        attempts.sort(key=lambda row: int(row.get("attempt_number", 0)))
        first = next((row for row in attempts if row.get("attempt_number") == 1), None)
        second = next((row for row in attempts if row.get("attempt_number") == 2), None)
        if not first or not second:
            raise ValueError(f"Required historical trace pair missing for {problem_id}.")
        initial_lines = str(first.get("proof_text", "")).splitlines()
        next_lines = str(second.get("proof_text", "")).splitlines()
        initial = "\n".join(initial_lines[:5])
        diff_lines = list(difflib.unified_diff(
            initial_lines, next_lines, fromfile="attempt_1", tofile="attempt_2", lineterm=""
        ))
        if not diff_lines:
            raise ValueError(f"No candidate change is recorded for {problem_id} attempts 1 and 2.")
        changed = "\n".join(diff_lines[:10])
        raw_errors = first.get("compiler_errors", [])
        diagnostic = "\n".join(str(raw_errors[0]).splitlines()[:6]) if raw_errors else "No diagnostic recorded."
        if first.get("success") is not False or second.get("success") is not False:
            raise ValueError(f"Expected two recorded failures for selected example {problem_id}.")
        blocks.extend([
            r"\paragraph{" + problem_id.replace("_", r"\_") + r" (manual trace; attempts 1 and 2 both rejected).}",
            r"\begin{quote}\small",
            r"\textbf{Initial candidate excerpt:}\par\ttfamily",
            code_excerpt(initial),
            r"\par\textbf{Compiler message excerpt:}\par\ttfamily",
            code_excerpt(diagnostic),
            r"\par\textbf{Attempt 1 to attempt 2 candidate diff:}\par\ttfamily",
            code_excerpt(changed),
            r"\par\textbf{Saved verifier outcomes:} attempt 1 success=false; attempt 2 success=false. Exit codes are not recorded in this legacy trace.",
            r"\end{quote}",
        ])
    return "\n".join(blocks)


def main() -> None:
    records = read_candidates()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "table1_candidate_inventory.tex").write_text(candidate_table(records) + "\n")
    (OUT / "table4_semantic_review_inventory.tex").write_text(semantic_table(records) + "\n")
    (OUT / "manual_compiler_examples.tex").write_text(historical_examples() + "\n")
    print(f"Generated inventory artifacts for {len(records)} candidates; no experiment metrics generated.")


if __name__ == "__main__":
    main()
