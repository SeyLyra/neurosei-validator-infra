"""
NeuroSei Python SDK
AI-powered validator tooling for SEI Network
"""

from .ai import AI
from .validator import Validator
from .zk_proofs import ZKProofGenerator

__version__ = "0.1.0"
__all__ = ["AI", "Validator", "ZKProofGenerator"]

# Convenience import
def from_neurosei_import_ai():
    """Example usage: from neurosei import AI"""
    return AI 