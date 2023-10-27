from langdetect import detect, detect_langs
from translate import Translator

def translate_text(text, target_language='en'):
    source_language = detect(text)
    if source_language == target_language:
        return text
    elif source_language != "es":
        print(f"[WARNING] NOT SPANISH ({source_language}): {text}")

    translator= Translator(to_lang=target_language, from_lang=source_language)
    translation = translator.translate(text)
    return translation


# Przykład użycia
input_text = "jajajaja"
translated_text = translate_text(input_text)
print(f"{input_text} -> {translated_text}")