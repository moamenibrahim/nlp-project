from finnish_toolkit import co_occurence, helper, named_entities, part_of_speech, sentiment, firebase_key
from english_toolkit import lda_topic, stanford_ner, translator
from nltk.corpus import stopwords as englishStopwords
from os import listdir,remove
import ijson,json
import operator
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
import pyrebase

files = listdir("./textdumps")  # Folder for dataset
righttopics = ["Terveys"]    # topics to be matched 

# Keeping tracck of number of threads and comments fetched
data = {"threads" : 0,
        "comments" : 0}

#### Dictionaries initializations 
named_entities_data={}  # Task 1 
named_entities_stanford={}  # Task 1
overall_sentiment_data={}   # Task 6 
paser_positive_data={}  # Task 7
paser_negative_data={}  # Task 8


with open('./data/sentences_dump.txt', 'r') as sentencesFile:
    sentences = sentencesFile.readlines()
    sentences = [x.strip() for x in sentences]

def translationFunc():
    translated_sent=[]
    for sent in sentences:
        translated=translator.translate(sent)
        if translated:
            translated_sent.append(translated)
    writeToFileTxt(data=translated_sent,filename='translated_sentences.txt',parameter='w+')
    return 

def translateDivided():  
    for fileN in listdir("./post_process/time"):
        if fileN.endswith(".txt"):
            filename="./post_process/time/{}".format(fileN)
        else:
            continue

        with open(filename) as f:
            print(filename)
            sentencespre = f.read().split('\n')
            f.close()

        translated_sent=[]
        for sent in sentencespre:
            translated=translator.translate(sent)
            if translated:
                translated_sent.append(translated)
        writeToFileTxt(data=translated_sent,filename='post_process/time/translated/'+fileN,parameter='w+')
    return

def analyzeFiles():
    '''
    Analyze files and dump outputs to post process to improve processing times
    '''

    # All sentences of the discussions: expected output is big and will be matched by 30 most frequent ner
    sentencesList=[]    
    for fileN in files:
        if fileN.endswith(".json"):
            filename="./textdumps/{}".format(fileN)
        else:
            continue
        with open(filename) as f:
            print(filename)

            try:
                items = ijson.items(f,"item")
                for o in items:
                    ### Checking topics and whether thread is deleted or not 
                    if co_occurence.checkTopic(o["topics"],righttopics) or o["deleted"] is True:
                        continue

                    data["threads"]+=1

                    body = o["body"]

                    ### check sentences and remove unidentified chars
                    body = co_occurence.checkSentence(body) 
                    sentencesList.extend(body) 
                    ### remove stopwords while keeping sentencesList with stopwords for parsers 
                    noStopWords = co_occurence.removeStopWords(body)    

                    timestamp = co_occurence.getDateString(o["created_at"]) 
                    # anonnick = co_occurence.getValueIntoList(o["anonnick"])   # not used
                    writeToFileTxt(body,filename='time/'+timestamp[0]+'.txt',parameter="a+")

                    for sentence in noStopWords:
                        named_entity=named_entities.polyglotNER(sentence)
                        if(named_entity):
                            addToDictNER(named_entity,named_entities_data)
                        stanford_named=stanford_ner.getNamedEntites(translator.translate(sentence))
                        if(stanford_named):
                            addToDictNER(stanford_named,named_entities_stanford)

                    for c in o["comments"]:
                        if c["deleted"] is True:
                            continue
                        
                        data["comments"]+=1

                        body = c["body"]
                        body = co_occurence.checkSentence(body)
                        sentencesList.extend(body)
                        noStopWords = co_occurence.removeStopWords(body)

                        timestamp = co_occurence.getDateString(c["created_at"]) 
                        # anonnick = co_occurence.getValueIntoList(c["anonnick"])   # not used 
                        writeToFileTxt(body,filename='time/'+timestamp[0]+'.txt',parameter="a+")

                        for sentence in noStopWords:
                            named_entity=named_entities.polyglotNER(translator.translate(sentence))
                            if(named_entity):
                                addToDictNER(named_entity,named_entities_data)
                            stanford_named=stanford_ner.getNamedEntites(translator.translate(sentence))
                            if(stanford_named):
                                addToDictNER(stanford_named,named_entities_stanford)

            except ValueError:
                print("ValueError")
                continue
            except KeyError:
                print("KeyError")
                continue
            except ijson.common.IncompleteJSONError:
                print("IncompleteJSONError")
                continue

    writeToFileTxt(data=sentencesList,filename='sentences.txt')
    writeToFile(data=named_entities_data,filename='named_entities.json')
    writeToFile(data=named_entities_stanford,filename='stanford_named_entities.json')
    print("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
    return

# add element to dictionary
def addToDict(elements, dictionary):
    '''
    helper function to add elements to dictionaries and keep track of repetitions 
    '''
    if (elements != ''):
        if (elements in dictionary):
            ## increment that elements
            dictionary[elements] += 1
        else:
            ## add elements to list
            dictionary[elements] = 1 
    return

# add element to dictionary for named entities
def addToDictNER(elements, dictionary):
    '''
    helper special function for named entities specifically polyglot
    '''
    item=elements.__str__()
    if (item != ''):
        if (item in dictionary):
            ## increment that item
            dictionary[item] += 1
        else:
            ## add item to list
            dictionary[item] = 1 
    return

# writing out to log-file the current contents of wordcount
def writeToFile(data,filename,parameter="w+"):
    '''
    write outputs to json files: for dictionaries 
    '''
    with open("post_process/"+filename,parameter) as f:
        json.dump(data,fp=f)
    return

# writing out to log-file the current contents of wordcount
def writeToFileTxt(data,filename,parameter="w+"):
    '''
    write outputs to text files: for strings 
    '''
    with open(filename,parameter) as f:
        for items in data:
            f.write(items+'\n')
    return

# visualizing results
def visualizePlotly(data_to_visualize, x_title, y_title, plotly_filename):
    '''
    Visualize Results to plolty
    '''
    x_axis=[]
    y_axis=[]
    for element in data_to_visualize:
        x_axis.append(element[0])
        y_axis.append(element[1])
    data = [go.Bar(
        x=x_axis,
        y=y_axis
    )]
    layout = go.Layout(
        title='suomi24',
        xaxis=dict(
            title=x_title,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title=y_title,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=plotly_filename)
    return

def visualize(data_to_visualize, x_title, y_title, graphname):
    
    x_axis=[]
    y_axis=[]
    for element in data_to_visualize:
        x_axis.append(element[0])
        y_axis.append(element[1])
    y_pos = np.arange(len(y_axis))
    x_pos = x_axis
    plt.bar(y_pos, x_pos, align='center', alpha=0.5)
    plt.xticks(y_pos, y_axis)
    plt.ylabel(y_title)
    plt.title(graphname)
    plt.show()


'''
Task 2 Frequency of Named entities
'''
def freqNER(named_entities_data):
    '''
    return most frequent ner
    '''
    named_entities_data = sorted(named_entities_data.items(),
                        key=operator.itemgetter(1), reverse=True)
    return named_entities_data[0:30]


'''
Task 2 Histogram for NER
'''
def histogramNER():
    '''
    construct a histogram of most repeated ner 
    '''
    with open("post_process/named_entities.json","r") as f:
        mydata=json.load(fp=f)
        common=freqNER(mydata)
        visualize(common, x_title='named entities', y_title='frequency', graphname='named-entities')
        return common


'''
Task 3 Parser tree on 30 most frequent NER
'''

def extract_sentences_of_most_frequent_named_entities():
    with open("data/five_diseases_dump.txt", "r") as f:
        words_to_check = f.readlines()
        words_to_check = [x.strip() for x in words_to_check]

    sentences_containing_words = []
    for sentence in sentences:
        for word in words_to_check:
            if sentence.lower().find(word) != -1:
                sentences_containing_words.append(sentence)
                break

    with open('data/five_diseases_sentences_dump.txt', 'w+') as f:
        f.writelines("%s\n" % line for line in sentences_containing_words)

def parse_most_frequent_named_entity_sentences():
    with open('data/five_diseases_sentences_dump.txt', 'r') as f:
        sentences = f.readlines()
        sentences = [x.strip() for x in sentences]

    from finnish_toolkit import parser

    mp = parser.Parser()

    parsed_sentences = []
    for i in range(30):
        sentence = sentences[i]
        parsed_sentence = mp.parse(sentence)
        parsed_sentences.append(parsed_sentence)
    
    import os
    dump_folder = './data/visualizations/five_diseases'
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    for i, parsed_sentence in enumerate(parsed_sentences):
        parser.visualize(
            parsed_sentence, '{}/{}.html'.format(dump_folder, i))


'''
Task 4 Most co-occuring pairs 
'''
firebase = pyrebase.initialize_app(firebase_key.pyrebase_config)
auth=firebase.auth()
db=firebase.database()
np_new_res=np.array([])

def mostCooccuring():
    mylist=fetchHigh(np_new_res,db)
    sorted_x=sorted(mylist, key=operator.itemgetter(1), reverse=True)
    no_stop=[]
    no_stop=removeStopFromList(sorted_x,co_occurence.stopwords,no_stop)
    most_common=no_stop
    most_common=most_common[0:30]
    return most_common

def fetchHigh(np_new_res,db):
    '''
    fetching high co-occurrence from firebase 
    '''
    occurrence=db.child('co-occurrences-new').get()
    values=occurrence.val()
    np_new_res=np.array([[value,values[value]['Total'],values[value]] for value in values])
    return np_new_res

def removeStopFromList(most_common,stopwords,no_stop):
    '''
    clear stopwords from lists 
    '''
    for string in most_common:
        item=string[0].split('-')
        if (u"%s"%str(item[0]) or u"%s"%str(item[1])) in stopwords:
            continue
        elif (u"%s"%str(item[0]) or u"%s"%str(item[1])) in set(englishStopwords.words('english')):
            continue
        else:
            no_stop.append(string)
    print("no stopwords list done")
    return no_stop 


'''
Task 5 Overall sentiment analysis 
'''
def overallSentiment(text):
    '''
    evaluate overall sentiment using afinn
    '''
    return sentiment.afinnCorpus(text)

def getSent():
    sentencesFile = open("post_process/sentences.txt","r")
    sentencespre = sentencesFile.read()
    sentences = sentencespre.replace('\n','\n ').split('\n')
    sentencesFile.close()
    return [overallSentiment(sentence) for sentence in sentences]


'''
Task 6 Parser tree on positive sentiment
'''
def parserPositiveAdj():
    with open("data/postive_adjectives_dump.txt", "r") as f:
        words_to_check = f.readlines()
        words_to_check = [x.strip() for x in words_to_check]

    sentences_containing_words = []
    for sentence in sentences:
        for word in words_to_check:
            if sentence.lower().find(word) != -1:
                sentences_containing_words.append(sentence)
                break

    with open('data/postive_adjectives_sentences_dump.txt', 'w+') as f:
        f.writelines("%s\n" % line for line in sentences_containing_words)

    with open('data/postive_adjectives_sentences_dump.txt', 'r') as f:
        sentences = f.readlines()
        sentences = [x.strip() for x in sentences]

    from finnish_toolkit import parser
    mp = parser.Parser()
    parsed_sentences = []
    for i in range(30):
        sentence = sentences[i]
        parsed_sentence = mp.parse(sentence)
        parsed_sentences.append(parsed_sentence)
    
    import os
    dump_folder = './data/visualizations/postive_adjectives'
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    for i, parsed_sentence in enumerate(parsed_sentences):
        parser.visualize(
            parsed_sentence, '{}/{}.html'.format(dump_folder, i))
    

def parserPositiveVerb():
    with open("data/postive_verbs_dump.txt", "r") as f:
        words_to_check = f.readlines()
        words_to_check = [x.strip() for x in words_to_check]

    sentences_containing_words = []
    for sentence in sentences:
        for word in words_to_check:
            if sentence.lower().find(word) != -1:
                sentences_containing_words.append(sentence)
                break

    with open('data/postive_verbs_sentences_dump.txt', 'w+') as f:
        f.writelines("%s\n" % line for line in sentences_containing_words)

    with open('data/postive_verbs_sentences_dump.txt', 'r') as f:
        sentences = f.readlines()
        sentences = [x.strip() for x in sentences]

    from finnish_toolkit import parser
    mp = parser.Parser()
    parsed_sentences = []
    for i in range(30):
        sentence = sentences[i]
        parsed_sentence = mp.parse(sentence)
        parsed_sentences.append(parsed_sentence)
    
    import os
    dump_folder = './data/visualizations/postive_verbs'
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    for i, parsed_sentence in enumerate(parsed_sentences):
        parser.visualize(
            parsed_sentence, '{}/{}.html'.format(dump_folder, i))

'''
Task 7 Parser tree on negative sentiment 
'''
def parserNegativeAdj():
    with open("data/negative_adjectives_dump.txt", "r") as f:
        words_to_check = f.readlines()
        words_to_check = [x.strip() for x in words_to_check]

    sentences_containing_words = []
    for sentence in sentences:
        for word in words_to_check:
            if sentence.lower().find(word) != -1:
                sentences_containing_words.append(sentence)
                break

    with open('data/negative_adjectives_sentences_dump.txt', 'w+') as f:
        f.writelines("%s\n" % line for line in sentences_containing_words)

    with open('data/negative_adjectives_sentences_dump.txt', 'r') as f:
        sentences = f.readlines()
        sentences = [x.strip() for x in sentences]

    from finnish_toolkit import parser
    mp = parser.Parser()
    parsed_sentences = []
    for i in range(30):
        sentence = sentences[i]
        parsed_sentence = mp.parse(sentence)
        parsed_sentences.append(parsed_sentence)
    
    import os
    dump_folder = './data/visualizations/negative_adjectives'
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    for i, parsed_sentence in enumerate(parsed_sentences):
        parser.visualize(
            parsed_sentence, '{}/{}.html'.format(dump_folder, i))

def parserNegativeVerb():
    with open("data/negative_verbs_dump.txt", "r") as f:
        words_to_check = f.readlines()
        words_to_check = [x.strip() for x in words_to_check]

    sentences_containing_words = []
    for sentence in sentences:
        for word in words_to_check:
            if sentence.lower().find(word) != -1:
                sentences_containing_words.append(sentence)
                break

    with open('data/negative_verbs_sentences_dump.txt', 'w+') as f:
        f.writelines("%s\n" % line for line in sentences_containing_words)

    with open('data/negative_verbs_sentences_dump.txt', 'r') as f:
        sentences = f.readlines()
        sentences = [x.strip() for x in sentences]

    from finnish_toolkit import parser
    mp = parser.Parser()
    parsed_sentences = []
    for i in range(30):
        sentence = sentences[i]
        parsed_sentence = mp.parse(sentence)
        parsed_sentences.append(parsed_sentence)
    
    import os
    dump_folder = './data/visualizations/negative_verbs'
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    for i, parsed_sentence in enumerate(parsed_sentences):
        parser.visualize(
            parsed_sentence, '{}/{}.html'.format(dump_folder, i))


'''
Task 8 LDA and sentiment variation per year
'''
def getSentVariation():

'''
Topic 9 detection functions 
'''
def overallTopic(text):
    return lda_topic.generate_topic(text)    

def getTopicVariation():

    topics=[]
    for fileN in listdir("./post_process/time_lemmatized"):
        if fileN.endswith(".txt"):
            filename="./post_process/time_lemmatized/{}".format(fileN)
        else:
            continue

        with open(filename) as f:
            print(filename)
            sentencespre = f.read()
            f.close()
        
        topic=overallTopic(sentencespre)
        print(topic)
        topics.append(topic)

    return topics
    

    sentiment=[]
    for fileN in listdir("./post_process/time"):
        if fileN.endswith(".txt"):
            filename="./post_process/time/{}".format(fileN)
        else:
            continue

        with open(filename) as f:
            print(filename)
            sentencespre = f.read()
            f.close()

        sentiment_item=overallSentiment(sentencespre)
        print(sentiment_item)
        sentiment.append(sentiment_item)

    return sentiment


    with open('data/five_diseases_sentences_dump.txt', 'r') as f:
        sentences = f.readlines()
        sentences = [x.strip() for x in sentences]

    from finnish_toolkit import parser

    mp = parser.Parser()

    parsed_sentences = []
    for i in range(30):
        sentence = sentences[i]
        parsed_sentence = mp.parse(sentence)
        parsed_sentences.append(parsed_sentence)
    
    import os
    dump_folder = './data/visualizations/five_diseases'
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    for i, parsed_sentence in enumerate(parsed_sentences):
        parser.visualize(
            parsed_sentence, '{}/{}.html'.format(dump_folder, i))


# sent = overallSentiment(sentencespre)
# overall_sent = [overallSentiment(sentence) for sentence in sentences]
# sentences=fetchSentences()
# histogramNER()
# commoncooccurred = mostCooccuring()
# print(overallTopic(". ".join(sent) for sent in sentences))
# analyzeFiles()
# translationFunc()
# getTopicVariation()
# getSentVariation()
# translateDivided()
# extract_sentences_of_most_frequent_named_entities()
# parse_most_frequent_named_entity_sentences()