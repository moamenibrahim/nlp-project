from afinn.afinn import Afinn
from polyglot.text import Text
from nltk import sent_tokenize
from statistics import mean 


def afinnSent(text, lang='fi'):
    afinn = Afinn(language=lang)
    return afinn.score(text)

def afinnCorpus(text, lang='fi'):
    afinn = Afinn(language=lang)
    sentences = sent_tokenize(text)
#     scored_sentences = ((afinn.score(sent), sent) for sent in sentences)
    scored_sentences = [afinn.score(sent) for sent in sentences]
    average_score = mean(scored_sentences)
    return average_score

def polyglotSent(text, lang='fi'):
    sentence=[]
    text=Text(text, hint_language_code=lang)
    # print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
    for w in text.words:
        if(w.polarity!=0):
            sentence.append([w, w.polarity])
    return w.polarity