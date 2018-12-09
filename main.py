from finnish_toolkit import co_occurence, helper, named_entities, part_of_speech, sentiment
from english_toolkit import lda_topic, stanford_ner, translator

from os import listdir,remove
import ijson,json
import operator
import plotly.plotly as py
import plotly.graph_objs as go

files = listdir("./textdumps")
righttopics = ["Paikkakunnat","Terveys"]

data = {"threads" : 0,
        "comments" : 0}

#### Dictionaries initializations 
named_entities_data={}  # Task 1 and 2
parser_tree_data={}  # Task 4 
most_co_occuring_data={} # Task 5 
overall_sentiment_data={}   # Task 6 
paser_positive_data={}  # Task 7
paser_negative_data={}  # Task 8

def analyizeFiles(): ### def analyizeFiles(filesLocation):
    
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
                    if co_occurence.checkTopic(o["topics"],righttopics) or o["deleted"] is True:
                        continue

                    data["threads"]+=1

                    body = o["body"]
                    body = co_occurence.checkSentence(body)
                    noStopWords = co_occurence.removeStopWords(body)

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

                        sent = c["body"]
                        sent = co_occurence.checkSentence(sent)
                        noStopWords = co_occurence.removeStopWords(sent)

                        timestamp = co_occurence.getDateString(c["created_at"]) #### TODO: TIMESTAMP ANALYSIS
                        anonnick = co_occurence.getValueIntoList(c["anonnick"])

                        for sentence in noStopWords:
                            named_entity=named_entities.polyglotNER(sentence)
                            if(named_entity):
                                addToDictNER(named_entity,named_entities_data)

            except ValueError:
                print("ValueError")
                continue
            except ijson.common.IncompleteJSONError:
                print("IncompleteJSONError")
                continue

    writeToFile(data=named_entities_data,filename='named_entities.json')
    print("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
    return


def addToDict(elements, dictionary):
    if (elements != ''):
        if (elements in dictionary):
            ## increment that elements
            dictionary[elements] += 1
        else:
            ## add elements to list
            dictionary[elements] = 1 
    return


### special function for named entities specifically polyglot
def addToDictNER(elements, dictionary):
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
    with open("post_process/"+filename,"a") as f:
        json.dump(data,fp=f)
    return


def visualize(data_to_visualize, x_title, y_title, plotly_filename):

    # Visualize Results  
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


'''
1. Frequency of Named entities
'''
def freqNER(named_entities_data):
    named_entities_data = sorted(named_entities_data.items(),
                        key=operator.itemgetter(1), reverse=True)
    print(named_entities)
    return named_entities

'''
2. Histogram for NER
'''
def histogramNER(named_entities_data):
    visualize(named_entities_data, x_title='named entities', y_title='frequency', plotly_filename='named-entities')

'''
3. Categories for NER
'''
def categoriesNER(parameter_list):
    pass

'''
4. Parser tree on 30 most frequent NER
'''
def parserTree(named_entities_data):
    named_entities_set=freqNER(named_entities_data)
    ## parser tree on named_entities_set[0:30]

'''
5. Most co-occuring pairs 
'''
def mostOccuring(parameter_list):
    ## Call from database (firebase)
    pass

'''
6. Overall sentiment analysis 
'''
def overallSentiment(text):
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



analyizeFiles()