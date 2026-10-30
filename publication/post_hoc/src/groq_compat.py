"""Optional legacy Groq dependency; local execution never constructs a client."""
from types import SimpleNamespace
try:
    import groq as groq
except ImportError:
    class GroqNotInstalledError(RuntimeError):
        pass
    groq = SimpleNamespace(APIError=GroqNotInstalledError,
        APIStatusError=GroqNotInstalledError, RateLimitError=GroqNotInstalledError, Groq=None)
