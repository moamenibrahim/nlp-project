from polyglot.text import Text

def polyglotNER(inputText):
    text = Text(inputText)
    for sent in text.sentences:
        for entity in sent.entities:
            print(entity.tag, entity)
    return text.entities
