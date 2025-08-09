#!/usr/bin/env python3

import yaml
from rapidfuzz import process, fuzz

def find_best_fuzzy_match(text, choices, threshold=70):
    """
    Finds the best fuzzy match for a given text from a list of choices.

    :param text: The input text to match.
    :param choices: List of strings to compare against.
    :param threshold: Minimum similarity score to consider a valid match (0–100).
    :return: A tuple of (best_match, score) or (None, 0) if no match found.
    """
    best_match = process.extractOne(text, choices, scorer=fuzz.ratio)

    if best_match and best_match[1] >= threshold:
        # print(best_match)
        return best_match[0], best_match[1]  # (match, score)
    else:
        return None, 0

# Example usage
yml_data = yaml.load(open('./data/fuzzy-text-data.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)

search_list = yml_data.get('search-list', [])
text_list = yml_data.get('text-list', [])
confidence = yml_data.get('confidence', 70)

for i, input_text in enumerate(search_list):
    match, score = find_best_fuzzy_match(input_text, text_list, threshold=confidence)
    print(f"{i}. {match}, Score: {score}")
