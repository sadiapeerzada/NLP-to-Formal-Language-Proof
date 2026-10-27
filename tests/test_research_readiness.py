"""Ensure offline preparation cannot promote the real unreviewed candidate pool."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('research_readiness', ROOT / 'scripts/research_readiness.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_real_pool_remains_blocked_and_review_packets_bind_exact_candidates():
    with TemporaryDirectory() as temporary:
        output = Path(temporary) / 'prepared'
        report = module.prepare(output)
        assert report['dataset_frozen'] is False
        assert report['api_calls'] == 0
        assert report['curation_validation']['eligible_problem_ids'] == ()
        assert report['frozen_validation']['errors']
        assert len(report['review_queue']) == report['candidate_count']
        for row in report['review_queue']:
            packet = Path(row['review_packet'])
            assert module.digest(packet) == row['review_packet_sha256']
            review = json.loads(packet.read_text())
            assert review['candidate_record']['id'] == row['id']
            assert review['semantic_fidelity_review']['status'] == 'pending'
            assert review['semantic_fidelity_review']['reviewer_id'] is None
        with pytest.raises(FileExistsError):
            module.prepare(output)
