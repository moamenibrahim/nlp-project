from afinn import Afinn
from polyglot.text import Text


def afinnSent(text, lang='fi'):
    afinn = Afinn(language=lang)
    return afinn.score(text)


def polyglotSent(text):
    text=Text(text)
    print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
    for w in text.words:
        print("{:<16}{:>2}".format(w, w.polarity))
    return