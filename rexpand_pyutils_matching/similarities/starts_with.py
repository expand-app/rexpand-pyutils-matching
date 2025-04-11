from typing import Callable
from rexpand_pyutils_matching.utils.string import IGNORED_CHARS, normalize_string


def _get_partial_similarity(
    s1_substrings: list[str],
    s2_substrings: list[str],
    s1_weight_dict: dict[str, float] | None = None,
    s1_total_weight: float | None = None,
) -> float:
    # Initialize s1_weight_dict and s1_total_weight if they are not provided
    if s1_weight_dict is None:
        s1_weight_dict = {part: 1 for part in s1_substrings}

    if s1_total_weight is None:
        s1_total_weight = sum(s1_weight_dict.values())

    score_a = 0
    set_b = set(s2_substrings)
    for a in s1_substrings:
        if a in set_b:
            current_score_a = 1
        else:
            current_score_a = 0
            for b in set_b:
                if b.startswith(a):
                    current_score_a = max(current_score_a, len(a) / len(b))

        score_a += current_score_a * s1_weight_dict[a]

    return score_a / s1_total_weight


def get_starts_with_similarity(
    s1: str,
    s2: str,
    get_part_weights: Callable[[str], dict[str, float]] | None = None,
    weight_by_length: bool = True,
    normalize: bool = True,
    ignored_chars: list[str] | None = IGNORED_CHARS,
    separator: str = " ",
) -> float:
    """
    Calculate similarity score based on whether one string starts with another.
    Score is normalized between 0 (no common prefix) and 1 (identical).

    Args:
        s1: First string
        s2: Second string
        get_part_weights: Function to get the weight of each part of the string
        weight_by_length: Whether to weight the parts by their length
        normalize: Whether to normalize the strings before comparison
        ignored_chars: Characters to ignore when normalizing strings
        separator: Separator to split the strings into parts

    Returns:
        float: Similarity score between 0 and 1
    """
    if normalize:
        s1 = normalize_string(s1, ignored_chars)
        s2 = normalize_string(s2, ignored_chars)

    if s1 == s2:
        return 1
    else:
        s1_substrings = [part.strip() for part in s1.split(separator)]
        s2_substrings = [part.strip() for part in s2.split(separator)]

        # Initialize s1_weight_dict, s1_total_weight, s2_weight_dict, s2_total_weight
        if get_part_weights is not None:
            s1_weight_dict = get_part_weights(s1)
            s1_total_weight = sum(s1_weight_dict.values())

            s2_weight_dict = get_part_weights(s2)
            s2_total_weight = sum(s2_weight_dict.values())
        elif weight_by_length:
            s1_weight_dict = {}
            s1_total_weight = 0
            for part in s1_substrings:
                length = len(part)
                s1_weight_dict[part] = length
                s1_total_weight += length

            s2_weight_dict = {}
            s2_total_weight = 0
            for part in s2_substrings:
                length = len(part)
                s2_weight_dict[part] = length
                s2_total_weight += length
        else:
            s1_weight_dict = {part: 1 for part in s1_substrings}
            s1_total_weight = len(s1_substrings)

            s2_weight_dict = {part: 1 for part in s2_substrings}
            s2_total_weight = len(s2_substrings)

        score_a = _get_partial_similarity(
            s1_substrings,
            s2_substrings,
            s1_weight_dict=s1_weight_dict,
            s1_total_weight=s1_total_weight,
        )
        score_b = _get_partial_similarity(
            s2_substrings,
            s1_substrings,
            s1_weight_dict=s2_weight_dict,
            s1_total_weight=s2_total_weight,
        )

        weighted_partial_score_a = score_a * len(s1) / (len(s1) + len(s2))
        weighted_partial_score_b = score_b * len(s2) / (len(s2) + len(s1))

        return weighted_partial_score_a + weighted_partial_score_b
