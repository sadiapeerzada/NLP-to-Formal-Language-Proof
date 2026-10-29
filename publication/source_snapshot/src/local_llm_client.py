"""Offline MLX completions from an exact, hash-verified local snapshot.

Importing this module neither imports Groq nor loads weights. No network/model
fallback, transport retry or remote-code execution is permitted.
"""
from __future__ import annotations
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import threading
import time
from model_client import CompletionResult


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def snapshot_inventory(path: Path) -> dict:
    path = path.resolve()
    if not path.is_dir() or len(path.name) != 40 or any(c not in '0123456789abcdef' for c in path.name):
        raise ValueError('An existing immutable 40-hex snapshot directory is required.')
    config = json.loads((path / 'config.json').read_text())
    tokenizer = json.loads((path / 'tokenizer_config.json').read_text())
    if not tokenizer.get('chat_template'):
        raise ValueError('Snapshot must provide its own instruction chat template.')
    files = {p.name: {'sha256': sha256(p), 'bytes': p.stat().st_size}
             for p in sorted(path.iterdir()) if p.is_file()}
    if not any(n.endswith('.safetensors') for n in files):
        raise ValueError('Local model weights are missing.')
    if any(n.endswith('.py') for n in files):
        raise ValueError('Remote/custom Python model code is not accepted.')
    template = tokenizer['chat_template']
    return {'snapshot_revision': path.name, 'files': files,
            'quantization': config.get('quantization'), 'model_type': config.get('model_type'),
            'chat_template': template,
            'chat_template_sha256': hashlib.sha256(json.dumps(template, sort_keys=True).encode()).hexdigest(),
            'tokenizer_revision': path.name, 'max_position_embeddings': config['max_position_embeddings'],
            'weight_bytes': sum(v['bytes'] for n,v in files.items() if n.endswith('.safetensors'))}


class LocalMLXClient:
    provider = 'mlx_local'

    def __init__(self, snapshot: Path, inventory: dict, *, model_id: str, seed: int,
                 max_context_tokens: int = 8192):
        actual = snapshot_inventory(snapshot)
        if actual != inventory:
            raise ValueError('Snapshot bytes do not match the frozen model inventory.')
        if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed < 2**32:
            raise ValueError('Seed must be a uint32 integer.')
        if isinstance(max_context_tokens, bool) or not isinstance(max_context_tokens, int) or not 1 <= max_context_tokens <= actual['max_position_embeddings']:
            raise ValueError('Context limit exceeds the model configuration.')
        self.snapshot, self.inventory = snapshot.resolve(), actual
        self.model_id, self.seed, self.max_context_tokens = model_id, seed, max_context_tokens
        self._model = self._tokenizer = None
        self._lock = threading.Lock()
        self.trace_directory = None
        self._ordinal = 0
        self._used_contexts = set()

    def _load(self):
        if snapshot_inventory(self.snapshot) != self.inventory:
            raise RuntimeError('Model files changed between preflight and loading.')
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        try:
            from mlx_lm import load
            self._model, self._tokenizer = load(str(self.snapshot), tokenizer_config={'trust_remote_code': False})
        except ImportError as error:
            raise RuntimeError('Local MLX backend is unavailable; verify the optional packages and Metal/GPU access.') from error

    def __call__(self, prompt: str, *, max_tokens: int = 2000, temperature: float = 0.2,
                 model: str | None = None, retries: int = 1,
                 reasoning_effort: str | None = None, generation_context: str | None = None, **kwargs) -> CompletionResult:
        if kwargs or retries != 1 or reasoning_effort is not None:
            raise ValueError('Local inference accepts one generation and no provider-specific options.')
        if model is not None and model != self.model_id:
            raise ValueError('Requested model differs from the frozen local model.')
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError('A nonempty prompt is required.')
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or not 1 <= max_tokens <= 2000:
            raise ValueError('Completion cap must be between 1 and 2000 tokens.')
        if isinstance(temperature, bool) or not isinstance(temperature, (int,float)) or not 0 <= temperature <= 2:
            raise ValueError('Temperature must be in [0, 2].')
        # Explicit call contexts make B stopping independent of C and keep
        # repeated unchanged prompts from reusing the same random stream.
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        with self._lock:
            context = generation_context or f'standalone/{self._ordinal}'
            if context in self._used_contexts:
                raise RuntimeError('Logical generation context was already attempted; automatic replay is forbidden.')
            self._used_contexts.add(context)
            self._ordinal += 1
            seed = int.from_bytes(hashlib.sha256(f'{self.seed}:{context}:{prompt_hash}'.encode()).digest()[:4], 'big')
            if self._model is None:
                self._load()
            import mlx.core as mx
            from mlx_lm import stream_generate
            from mlx_lm.sample_utils import make_sampler
            rendered = self._tokenizer.apply_chat_template(
                [{'role':'user','content':prompt}], tokenize=False, add_generation_prompt=True)
            token_ids = self._tokenizer.encode(rendered, add_special_tokens=False)
            if len(token_ids) + max_tokens > self.max_context_tokens:
                raise RuntimeError('Rendered input plus output cap exceeds the frozen context budget.')
            mx.random.seed(seed)
            started = time.monotonic(); chunks=[]; final=None
            trace = None
            if self.trace_directory is not None:
                trace_path = Path(self.trace_directory) / (hashlib.sha256(context.encode()).hexdigest()+'.jsonl')
                trace = trace_path.open('x', encoding='utf-8')
            try:
                if trace:
                    trace.write(json.dumps({'context':context,'prompt_sha256':prompt_hash,'generation_seed':seed})+'\n'); trace.flush(); os.fsync(trace.fileno())
                for response in stream_generate(self._model, self._tokenizer, prompt=token_ids,
                        max_tokens=max_tokens, sampler=make_sampler(temp=temperature, top_p=1.0)):
                    chunks.append(response.text); final=response
                    if trace:
                        trace.write(json.dumps({'token':response.token,'text':response.text,'generation_tokens':response.generation_tokens})+'\n');trace.flush();os.fsync(trace.fileno())
                if trace:
                    trace.write(json.dumps({'status':'generation_finished','completion_tokens':getattr(final,'generation_tokens',None)})+'\n');trace.flush();os.fsync(trace.fileno())
            except BaseException as error:
                if trace:
                    trace.write(json.dumps({'status':'interrupted','error_type':type(error).__name__,'completion_tokens':getattr(final,'generation_tokens',0)})+'\n');trace.flush();os.fsync(trace.fileno())
                raise
            finally:
                if trace: trace.close()
            if final is None:
                raise RuntimeError('MLX returned no generation telemetry.')
            content=''.join(chunks)
            return CompletionResult(content, {
                'provider': self.provider, 'model': self.model_id, 'response_model': self.model_id,
                'snapshot_revision': self.inventory['snapshot_revision'], 'base_seed':self.seed,
                'generation_seed':seed, 'generation_context':context,
                'seed_policy':'sha256(base_seed:context:prompt_sha256)_first_uint32',
                'prompt_sha256':prompt_hash, 'rendered_chat_text':rendered,
                'rendered_chat_sha256':hashlib.sha256(rendered.encode()).hexdigest(),
                'chat_template_sha256':self.inventory['chat_template_sha256'],
                'prompt_tokens':len(token_ids), 'completion_tokens':final.generation_tokens,
                'total_tokens':len(token_ids)+final.generation_tokens,
                'finish_reason':getattr(final,'finish_reason', None),
                'max_completion_tokens':max_tokens,'temperature':temperature,'top_p':1.0,
                'latency_seconds':time.monotonic()-started,'api_attempts':0,
                'logical_generations':1, 'retry_events':[], 'content_empty':not content.strip(),
                'mlx_version':importlib.metadata.version('mlx'),
                'mlx_lm_version':importlib.metadata.version('mlx-lm'),
                'platform':platform.platform(), 'peak_memory_gb':getattr(final,'peak_memory',None),
            })
