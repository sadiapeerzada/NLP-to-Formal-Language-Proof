from pathlib import Path
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model_client import CompletionResult
from verify import VerificationResult
from formalize import formalize
from proof_sketch import sketch_with_metadata
from synthesize import synthesize_and_verify


def test_all_stages_accept_the_common_local_completion_interface(tmp_path):
    class SyntheticClient:
        model_id='synthetic-local-fixture'
        def __init__(self):self.calls=[]
        def __call__(self,prompt,**kwargs):
            self.calls.append(kwargs)
            return CompletionResult('theorem target : True := by trivial',{'provider':'synthetic-test-only','model':self.model_id})
    client=SyntheticClient()
    with patch('formalize.check_lean_file_detailed',return_value=VerificationResult(True)):
        ok,statement,trace=formalize('Synthetic test statement.',tmp_path,'test',completion_fn=client)
    assert ok and trace[0]['provider']=='synthetic-test-only'
    assert sketch_with_metadata('Synthetic.',statement,completion_fn=client).metadata['model']==client.model_id
    with patch('synthesize.check_lean_file_detailed',return_value=VerificationResult(True)):
        result,attempts=synthesize_and_verify('Synthetic.',statement,'Synthetic.',tmp_path,'test',max_repair=0,completion_fn=client)
    assert result['solved'] and all(call['model']==client.model_id for call in client.calls)
