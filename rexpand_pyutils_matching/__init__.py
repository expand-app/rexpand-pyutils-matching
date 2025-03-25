"""
rexpand-pyutils-matching - Python utilities for string matching and pattern recognition
"""

__version__ = "0.0.1"

from .matchers import (
    exact_match,
    fuzzy_match,
    SimilarityMeasure,
)
from .utils import normalize_string

__all__ = [
    "exact_match",
    "fuzzy_match",
    "SimilarityMeasure",
    "normalize_string",
]
