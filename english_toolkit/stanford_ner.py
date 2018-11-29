from nltk.tag import StanfordNERTagger


class StanfordNer(object):
    def __init__(self):
        stanford_dir = '/stanford/stanford-nertagger-2018-10-16/'
        jarfile = stanford_dir + 'stanford-ner.jar'
        modelfile = stanford_dir + 'classifiers/english.muc.7class.distsim.crf.ser.gz'
        self.st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)
        
    def getNamedEntites(self, text):
        return self.st.tag(text.split())