"""Second, disclosed reviewer/model/prompt revision; first pass is preserved."""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('ai_audit_runner', Path(__file__).with_name('ai_semantic_audit.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    runner.MODEL = runner.ROOT / 'data/ai_semantic_audit/20261028/model_phi4'
    runner.TEMPLATE = runner.ROOT / 'prompts/ai_semantic_audit_v2.txt'
    if args.action == 'prepare':
        runner.prepare(args.output)
        path = args.output / 'manifest.json'
        m = json.loads(path.read_text())
        m['source_sha256']['scripts/ai_semantic_audit_phi4.py'] = runner.sha(Path(__file__))
        m['revision_disclosure'] = ('Phi-4 mini and a shorter, balanced JSON prompt were added after observing '
            'Phi-3.5 format failures and unsupported semantic objections. All 96 subjects are reviewed again; '
            'no prior responses, static assessments, proofs or split assignments are shown to Phi-4. '
            'No first-pass outcome is erased. This is curation workflow development, not study prompt tuning.')
        path.write_text(json.dumps(m, indent=2) + '\n')
    else:
        runner.run(args.output)
