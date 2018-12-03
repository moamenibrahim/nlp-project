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

def train_lda():
	with open('newsgroups', 'rb') as f:
		newsgroup_data = pickle.load(f)

	vect = CountVectorizer(min_df=20, max_df=0.2, stop_words='english',
		token_pattern='(?u)\\b\\w\\w\\w+\\b')
	
	X = vect.fit_transform(newsgroup_data)
	corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)
	id_map = dict((v, k) for k, v in vect.vocabulary_.items())
	ldamodel = gensim.models.ldamodel.LdaModel(
		corpus, num_topics=10, iterations=100, id2word=id_map, passes=25, random_state=34)
	output = ldamodel.print_topics(10)
	# print (output)
	return

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
	ldamodel = Lda(doc_term_matrix, num_topics=2, id2word = dictionary, passes=300)
	str = ldamodel.print_topics(num_topics=2, num_words=3)
	s = tuple(str)
	t = "\n".join(item[1] for item in s)
	result = re.findall('[a-zA-Z]+',t)
	for i in result:
		if i not in mylist:
			mylist.append(i)
	return mylist
