from afinn import Afinn

'''
Class currently gets sentiment analysis for Finnish text 
'''

def getSentiment(self, text, lang='fi'):
    afinn = Afinn(language=lang)
    return afinn.score(text)