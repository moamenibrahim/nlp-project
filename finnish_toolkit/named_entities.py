from polyglot.text import Text

def polyglotNER(inputText, lang='fi'):
        try:
                text = Text(inputText, hint_language_code=lang)
                for sent in text.sentences:
                        for entity in sent.entities:
                                print(entity.tag, entity)
                                return text.entities
        except UnboundLocalError:
                print("UnboundLocalError")
                return False
