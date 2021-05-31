from translate import Translator


def translate(text, from_language, to_language):
    translator = Translator(from_lang=from_language, to_lang=to_language, email="<emailhere>")
    translation = translator.translate(text)
    return translation
