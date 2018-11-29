from afinn import Afinn

'''
Class currently gets sentiment analysis for Finnish text 
'''

class afinnSentiment(object):
    def __init__(self):
        self.afinn = Afinn(language='fi')

    def getSentiment(self, text):
        return self.afinn.score(text)