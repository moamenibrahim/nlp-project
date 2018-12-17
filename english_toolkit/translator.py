from googletrans import Translator
import json,time

def translate(input_str,lang='fi'):
    time.sleep(1)
    translate_urls = ["translate.google.com", "translate.google.co.kr",
                      "translate.google.at", "translate.google.de",
                      "translate.google.ru", "translate.google.ch",
                      "translate.google.fr", "translate.google.es"]
    translator = Translator(service_urls=translate_urls)
    try:
        translated = translator.translate(str(input_str), dest='en', src=lang)
        return translated.text
    except Exception as e:
        print(str(e))
        return False
