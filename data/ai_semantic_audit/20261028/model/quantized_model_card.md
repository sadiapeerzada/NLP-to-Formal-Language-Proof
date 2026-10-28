---
language:
- multilingual
library_name: transformers
license: mit
license_link: https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/LICENSE
pipeline_tag: text-generation
tags:
- nlp
- code
- mlx
widget:
- messages:
  - role: user
    content: Can you provide ways to eat combinations of bananas and dragonfruits?
---

# mlx-community/Phi-3.5-mini-instruct-4bit

The Model [mlx-community/Phi-3.5-mini-instruct-4bit](https://huggingface.co/mlx-community/Phi-3.5-mini-instruct-4bit) was converted to MLX format from [microsoft/Phi-3.5-mini-instruct](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) using mlx-lm version **0.17.0**.

## Use with mlx

```bash
pip install mlx-lm
```

```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Phi-3.5-mini-instruct-4bit")
response = generate(model, tokenizer, prompt="hello", verbose=True)
```
