from .redact_per_pdf import redact_pdf

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("masquerade")
except ImportError:
    __version__ = "unknown"

__all__ = ["redact_pdf"]
