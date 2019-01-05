import gensim
import re
import string
import sys
import pickle
from gensim import corpora
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

stopwords_file = open("./finnish_toolkit/finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()

def preprocess_sentences(doc_complete):
	exclude = set(string.punctuation)
	lemma = WordNetLemmatizer()
	norm = []
	stop_free = [i for i in doc_complete.lower().split() if i not in stopwords]
	punc_free = ' '.join(ch for ch in stop_free if ch not in exclude)
	norm.append(punc_free.split())
	return norm

def generate_topic(input):
	mylist=[]
	texts = preprocess_sentences(input)
	dictionary = corpora.Dictionary(texts)
	doc_term_matrix = [dictionary.doc2bow(text) for text in texts]
	Lda = gensim.models.ldamodel.LdaModel
	ldamodel = Lda(doc_term_matrix, num_topics=20, id2word = dictionary, passes=400)
	str = ldamodel.print_topics(num_topics=20, num_words=20)
	s = tuple(str)
	t = "\n".join(item[1] for item in s)
	result = re.findall('[a-zA-ZåäöÅÄÖ]+',t)
	for i in result:
		if i not in mylist:
			mylist.append(i)
	return mylist
