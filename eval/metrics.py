"""Compute pass@1, per-category breakdown, and repair-iteration stats from a
results JSONL file produced by src/pipeline.py.

Usage: python eval/metrics.py data/results/run1.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict


def load(path: str):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def main(path: str):
    results = load(path)
    total = len(results)
    solved = [r for r in results if r["solved"]]

    print(f"Overall pass@1: {len(solved)}/{total} = {len(solved) / total:.1%}\n")

    by_category = defaultdict(list)
    for r in results:
        by_category[r["category"]].append(r)

    print("By category:")
    for cat, rs in sorted(by_category.items()):
        s = sum(1 for r in rs if r["solved"])
        print(f"  {cat:22s} {s}/{len(rs)} = {s / len(rs):.1%}")

    by_difficulty = defaultdict(list)
    for r in results:
        by_difficulty[r["difficulty"]].append(r)

    print("\nBy difficulty:")
    for diff, rs in sorted(by_difficulty.items()):
        s = sum(1 for r in rs if r["solved"])
        print(f"  difficulty {diff}: {s}/{len(rs)} = {s / len(rs):.1%}")

    if solved:
        avg_repairs = sum(r["repair_attempts"] for r in solved) / len(solved)
        print(f"\nAvg repair attempts to success: {avg_repairs:.2f}")

        timed = [r for r in solved if r.get("wall_clock_seconds") is not None]
        if timed:
            avg_time = sum(r["wall_clock_seconds"] for r in timed) / len(timed)
            print(f"Avg wall-clock time per solved problem: {avg_time:.1f}s ({len(timed)}/{len(solved)} entries had timing data)")
        else:
            print("Avg wall-clock time: n/a (no entries have wall_clock_seconds -- "
                  "this run's proofs were hand-authored rather than API-timed, see RUN_REPORT.md)")

    failures = [r for r in results if not r["solved"]]
    if failures:
        by_stage = defaultdict(int)
        for r in failures:
            by_stage[r.get("failure_stage", "unknown")] += 1
        print("\nFailure breakdown by stage:")
        for stage, count in by_stage.items():
            print(f"  {stage}: {count}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python eval/metrics.py <results.jsonl>")
        sys.exit(1)
    main(sys.argv[1])
