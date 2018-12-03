from finnish_toolkit import co_occurence, helper
from os import listdir,remove
import ijson

files = listdir("./textdumps")

data = {"threads" : 0,
        "comments" : 0,
        "wordpairs" : 0}


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
                if o["deleted"] is True:
                    #checkTopic(o["topics"],helper.righttopics) or #extra check above
                    #print(o["topics"],o["deleted"])
                    continue
                topics=co_occurence.extractTopics(o["topics"])
                body = o["body"]
                #foundKeywords = search_keywords(body)
                #if foundKeywords:
                    #fKeyWords = foundKeywords.copy()
                body = co_occurence.checkSentence(body)
                timestamp = co_occurence.getDateString(o["created_at"])
                anonnick = co_occurence.getValueIntoList(o["anonnick"])

                for sentence in body:
                    wordcount={}
                    data["threads"]+=1
                    #clean = [word for word in sentence.split() if word.lower() not in stopwords]
                    #print(foundKeywords)
                    #print(timestamp,anonnick)
                    co_occurence.addSentence(sentence,topics,False,timestamp,anonnick)
                for c in o["comments"]:
                    if c["deleted"] is True:
                        continue
                    sent = c["body"]
                    #if (search_keywords(s,keywords)==True):
                    sent = co_occurence.checkSentence(sent)
                    timestamp = co_occurence.getDateString(c["created_at"])
                    anonnick = co_occurence.getValueIntoList(c["anonnick"])
                    for s in sent:
                        wordcount={}
                        data["comments"]+=1
                        #cleanC = [word for word in body.split() if word.lower() not in stopwords]
                        #print(timestamp2,anonnick2)
                        co_occurence.addSentence(s,topics,True,timestamp,anonnick)
        except ValueError:
            print("ValueError")
            continue
        except ijson.common.IncompleteJSONError:
            print("IncompleteJSONError")
            continue

    #writeToFile(data)

#pprint(data)
print("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
