from googletrans import Translator

def translate(input_str,lang='fi'):
    translator = Translator()
    return translator.translate(input_str, dest='en', src=lang)