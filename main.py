from finnish_toolkit import co_occurence, helper, named_entities, part_of_speech, sentiment, firebase_key
from english_toolkit import lda_topic, stanford_ner, translator
from nltk.corpus import stopwords as englishStopwords

from os import listdir,remove
import ijson,json
import operator
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pyrebase
import threading


files = listdir("./textdumps")  # Folder for dataset
righttopics = ["Paikkakunnat","Terveys"]    # topics to be matched 

# Keeping tracck of number of threads and comments fetched
data = {"threads" : 0,
        "comments" : 0}

#### Dictionaries initializations 
named_entities_data={}  # Task 1 
overall_sentiment_data={}   # Task 6 
paser_positive_data={}  # Task 7
paser_negative_data={}  # Task 8

def analyzeFiles():
    '''
    Analyze files and dump outputs to post process to improve processing times
    '''

    sentencesList=[]    # All sentences of the discussions: expected output is big and will be matched by 30 most frequent ner
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
                    body = co_occurence.checkSentence(body) # check sentences and remove unidentified chars
                    sentencesList.extend(body)  
                    noStopWords = co_occurence.removeStopWords(body)    # remove stopwords while keeping sentencesList with stopwords for parsers

                    timestamp = co_occurence.getDateString(o["created_at"]) #### TODO: TIMESTAMP ANALYSIS
                    anonnick = co_occurence.getValueIntoList(o["anonnick"])

                    for sentence in noStopWords:
                        named_entity=named_entities.polyglotNER(sentence)
                        if(named_entity):
                            addToDictNER(named_entity,named_entities_data)

                    for c in o["comments"]:
                        if c["deleted"] is True:
                            continue
                        
                        data["comments"]+=1

                        body = c["body"]
                        body = co_occurence.checkSentence(body)
                        sentencesList.extend(body)
                        noStopWords = co_occurence.removeStopWords(body)

                        timestamp = co_occurence.getDateString(c["created_at"]) #### TODO: TIMESTAMP ANALYSIS
                        anonnick = co_occurence.getValueIntoList(c["anonnick"])

                        for sentence in noStopWords:
                            named_entity=named_entities.polyglotNER(sentence)
                            if(named_entity):
                                addToDictNER(named_entity,named_entities_data)

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
    print("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
    return


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

#writing out to log-file the current contents of wordcount
def writeToFile(data,filename):
    '''
    write outputs to json files: for dictionaries 
    '''
    with open("post_process/"+filename,"w+") as f:
        json.dump(data,fp=f)
    return

def writeToFileTxt(data,filename):
    '''
    write outputs to text files: for strings 
    '''
    with open("post_process/"+filename,"a") as f:
        for items in data:
            f.write(items+'\n')
    return

def visualize(data_to_visualize, x_title, y_title, plotly_filename):
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

'''
1. Frequency of Named entities
'''
def freqNER(named_entities_data):
    '''
    return most frequent ner
    '''
    named_entities_data = sorted(named_entities_data.items(),
                        key=operator.itemgetter(1), reverse=True)
    return named_entities_data[0:30]

'''
2. Histogram for NER
'''
def histogramNER():
    '''
    construct a histogram of most repeated ner 
    '''
    with open("post_process/named_entities.json","r") as f:
        mydata=json.load(fp=f)
        common=freqNER(mydata)
        visualize(common, x_title='named entities', y_title='frequency', plotly_filename='named-entities')
    return

'''
3. Categories for NER
'''
def categoriesNER(parameter_list):
    '''
    building categories from ner list
    '''
    pass

'''
4. Parser tree on 30 most frequent NER
'''
def fetchSentences():
    '''
    fetch sentences that contains any of the most repeated named entities
    '''
    sentencesFile = open("post_process/sentences.txt","r")
    sentences = sentencesFile.read().split(",")
    sentences = sentences[0].split("\n")
    sentencesFile.close()

    mysentences = []
    with open("post_process/named_entities.json","r") as f:
        mydata=json.load(fp=f)
        common=freqNER(mydata)
        for element in common:
            for sentence in sentences:
                if element in sentence:
                    mysentences.append(sentence)
        return mysentences

def parserTree(named_entities_data):
    '''
    lunching Turku parser on most frequent named entites 
    '''
    with open("post_process/named_entities.json","r") as f:
        mydata=json.load(fp=f)
        common=freqNER(mydata)
    return common

'''
5. Most co-occuring pairs 
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
6. Overall sentiment analysis 
'''
def overallSentiment(text):
    '''
    evaluate overall sentiment using afinn
    '''
    sentiment.afinnSent(text)
    pass

'''
7. Parser tree on positive sentiment
'''
def parserPositive(parameter_list):
    pass

'''
8. Parser tree on negative sentiment 
'''
def parserNegative(parameter_list):
    pass

'''
9. LDA and sentiment variation per year
'''
def yearVariation(parameter_list):
    pass

'''
10. Identify diseases
'''
def identifyDiseases(parameter_list):
    pass

'''
11. frequency of diseases per month 
'''
def diseasesFrequency(parameter_list):
    pass

'''
12. Top 5 diseases analysis 
'''
def topDiseases(parameter_list):
    pass


# sentences=fetchSentences()
# histogramNER()
# commoncooccurred = mostCooccuring()
analyzeFiles()