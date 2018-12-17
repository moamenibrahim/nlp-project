import gensim
import re
import string
import sys
import pickle
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

def preprocess_sentences(doc_complete):
	stop = set(stopwords.words('english'))
	exclude = set(string.punctuation)
	lemma = WordNetLemmatizer()
	norm = []
	stop_free = [i for i in doc_complete.lower().split() if i not in stop]
	punc_free = ' '.join(ch for ch in stop_free if ch not in exclude)
	normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
	norm.append(normalized.split())
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
	result = re.findall('[a-zA-Z]+',t)
	for i in result:
		if i not in mylist:
			mylist.append(i)
	return mylist
