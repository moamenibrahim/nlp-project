from googletrans import Translator

def translate(input_str,lang='fi'):
    try:
        translator = Translator()
        translated = translator.translate(input_str, dest='en', src=lang)
        return translated.text
    except AttributeError:
        return input_str
