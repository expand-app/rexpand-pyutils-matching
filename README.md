# rexpand-pyutils-matching

A Python library providing various string matching utilities including exact matching, fuzzy matching with multiple similarity measures, and string normalization.

## Installation

```bash
pip install rexpand-pyutils-matching
```

## Features

- Exact string matching
- Fuzzy string matching with multiple similarity measures:
  - Levenshtein distance
  - Longest common subsequence
  - Common prefix
  - Starts with
- String normalization utilities
- Configurable similarity thresholds
- Optional string normalization

## Usage

```python
from rexpand_pyutils_matching import (
    exact_match,
    fuzzy_match,
    SimilarityMeasure,
    normalize_string,
)

# Exact matching
exact_match("hello", "hello")  # True
exact_match("hello", "world")  # False

# Fuzzy matching with different similarity measures
fuzzy_match("hello", "helo", threshold=0.8)  # Using Levenshtein (default)
fuzzy_match("hello", "helo", threshold=0.8, similarity_measure=SimilarityMeasure.LONGEST_COMMON_SEQUENCE)
fuzzy_match("hello world", "hello", threshold=0.8, similarity_measure=SimilarityMeasure.COMMON_PREFIX)
fuzzy_match("hello world", "hello", threshold=0.8, similarity_measure=SimilarityMeasure.STARTS_WITH)

# Without string normalization
fuzzy_match("Hello", "hello", threshold=0.8, normalize=False)

# String normalization
normalize_string("Hello, World!")  # "hello world"
```

## Similarity Measures

The package provides several similarity measures for fuzzy matching:

1. **Levenshtein** (default)

   - Measures the minimum number of single-character edits required to change one string into another
   - Good for general-purpose string similarity

2. **Longest Common Subsequence**

   - Finds the longest sequence of characters that appear in both strings in the same order
   - Useful when character order matters but characters don't need to be consecutive

3. **Common Prefix**

   - Calculates similarity based on common prefixes between words
   - Good for matching words that share the same beginning

4. **Starts With**
   - Checks if one string starts with another
   - Useful for prefix-based matching

## Requirements

- Python >= 3.11
- NumPy >= 1.21.0

## Development

The project includes a Makefile with common development commands. First, set up your development environment:

```bash
# Create virtual environment
make venv

# Activate virtual environment (you need to do this every time you start a new shell)
source .venv/bin/activate

# Install development dependencies (this will also create venv if it doesn't exist)
make install
```

Other available commands:

```bash
# Run tests
make test

# Run linting checks
make lint

# Format code
make format

# Clean build artifacts
make clean

# Clean everything including virtual environment
make clean-all

# Build package
make build

# Upload to PyPI
make publish

# Run all checks before commit
make pre-commit
```

To deactivate the virtual environment when you're done:

```bash
deactivate
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
