from nltk.tag import StanfordNERTagger

stanford_dir = './stanford/stanford-nertagger-2018-10-16/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.muc.7class.distsim.crf.ser.gz'
st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)
        
def getNamedEntites(self, text):
    return st.tag(text.split())