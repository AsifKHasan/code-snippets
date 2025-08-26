# pip install ai4bharat-transliteration
# pip install indic-transliteration
# pip install pygoogletranslation

# pip install pip==24.0
# pip install --upgrade pip


# -----------------------------------------------------------------------------------
from ai4bharat.transliteration import XlitEngine

engine = XlitEngine("bn")
engine = XlitEngine("hi", beam_width=10, rescore=True)

# --- Example 1: Transliterating a single sentence ---
english_sentence = "Amar sonar Bangla, ami tomay bhalobashi."
transliterated_output = engine.translit_sentence(english_sentence)

# The output is a dictionary. The key is the language code, and the value is the transliterated string.
bangla_sentence = transliterated_output['bn']

print(f"English: {english_sentence}")
print(f"Bangla (Transliterated): {bangla_sentence}")

# --- Example 2: Transliterating a single word with multiple suggestions ---
english_word = "namaskar"
transliterated_word_suggestions = engine.translit_word(english_word)

# The output for a word is also a dictionary, with a list of top suggestions.
print(f"\nEnglish Word: {english_word}")
print(f"Bangla Suggestions: {transliterated_word_suggestions['bn']}")


# -----------------------------------------------------------------------------------
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

# Define the scheme map from ITRANS (a phonetic English representation) to Bengali
# The library supports various schemes, but ITRANS is commonly used for phonetic transliteration.
# You can also use other schemes like VELTHUIS or a custom map.
scheme_map = SchemeMap(SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.BENGALI])

# The input English sentence
english_sentence = "Amar naam Rohan."
bangla_sentence = transliterate(english_sentence, scheme_map=scheme_map)
print(bangla_sentence)
