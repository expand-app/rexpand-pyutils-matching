from typing import Callable
from ..utils.string import normalize_string


def _get_partial_similarity(
    s1_substrings: list[str],
    s2_substrings: list[str],
    s1_weight_dict: dict[str, float] | None = None,
) -> float:
    set_b = set(s2_substrings)
    if s1_weight_dict is None:
        s1_weight_dict = {part: 1 / len(s1_substrings) for part in s1_substrings}

    score_a = 0
    for a in s1_substrings:
        if a in set_b:
            current_score_a = 1
        else:
            current_score_a = 0
            for b in set_b:
                if b.startswith(a):
                    current_score_a = max(current_score_a, len(a) / len(b))

        score_a += current_score_a * s1_weight_dict[a]

    return score_a


def get_starts_with_similarity(
    s1: str,
    s2: str,
    get_part_weights: Callable[[str], dict[str, float]] | None = None,
    normalize: bool = True,
) -> float:
    """
    Calculate similarity score based on whether one string starts with another.
    Score is normalized between 0 (no common prefix) and 1 (identical).

    Args:
        s1: First string
        s2: Second string
        get_part_weights: Function to get the weight of each part of the string
        normalize: Whether to normalize the strings before comparison

    Returns:
        float: Similarity score between 0 and 1
    """
    if normalize:
        s1 = normalize_string(s1)
        s2 = normalize_string(s2)

    if s1 == s2:
        return 1
    else:
        s1_substrings = s1.split()
        s2_substrings = s2.split()

        if get_part_weights is not None:
            s1_weight_dict = get_part_weights(s1)
            s2_weight_dict = get_part_weights(s2)
        else:
            s1_weight_dict = None
            s2_weight_dict = None

        score_a = _get_partial_similarity(s1_substrings, s2_substrings, s1_weight_dict)
        score_b = _get_partial_similarity(s2_substrings, s1_substrings, s2_weight_dict)

        weighted_partial_score_a = score_a * len(s1) / (len(s1) + len(s2))
        weighted_partial_score_b = score_b * len(s2) / (len(s2) + len(s1))

        return weighted_partial_score_a + weighted_partial_score_b
