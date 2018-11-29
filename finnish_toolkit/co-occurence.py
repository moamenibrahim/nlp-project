
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir,remove
import sys
import ijson
#import operator
from pprint import pprint
import string
import nltk
import subprocess
import codecs
# reload(sys)
# sys.setdefaultencoding('utf8')
import re


wordcount = {}

data = {"threads" : 0,
        "comments" : 0,
        "wordpairs" : 0}

#check if one of the keywords exist in the given string
def search_keywords(string, keywords):
    for word in keywords:
        if word in string:
            return True
    return False

#helper function to add word into the dictionary
def addword(word,dist):
    if dist>25:
        return
    if word not in wordcount:
        wordcount[word] = addDistance(dist)
    else:
        vals = addDistance(dist)
        obj = wordcount[word]
        for k in vals:
            obj[k] += vals[k]

def addDistance(dist):
    a = {"1-2":0,"3-5":0,"6-8":0,"8-14":0,"15+":0}
    if dist<3:
        a["1-2"]+=1
    elif dist<6:
        a["3-5"]+=1
    elif dist<9:
        a["6-8"]+=1
    elif dist<15:
        a["8-14"]+=1
    else:
        a["15+"]+=1
    return a

#writing out to log-file the current contents of wordcount
def writeToFile():
    try:
        remove("logs.txt")
    except OSError:
        pass
    #print(wordcount)
    #sorted_wc = sorted(wordcount.items(),key=operator.itemgetter(1),reverse=True)
    #pprint(wordcount)

    with open("logs.txt","a") as f:
        f.write("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
        f.write("Most common wordpairs in text: \n\n")
        #r= 250 if len(sorted_wc) > 250 else len(sorted_wc)
        #for i in range(0, r):
        i = 0
        for key,val in sorted(wordcount.items(), key=lambda i:sum(i[1].values()),reverse=True):
            #print(key,val)
            f.write("%s,%s,\n\t\t'total': %i,\n\t\t'1-2': %i, \n\t\t'3-5': %i, \n\t\t'6-8': %i,\n\t\t'8-14': %i,\n\t\t'15+': %i'\n\n" %
            (key[0],key[1],sum(val.values()),val['1-2'],val['3-5'],val['6-8'],val['8-14'],val['15+']))
            if (i>300):
                break
            i+=1
        f.close()

#def

#Load keywords and stopwords, and define characters to be removed
toberemoved = ["<p>","</p>",",","?","!","-"]

keyword_file = open("../scraper-test/finnish_keywords.txt","r")
sents = keyword_file.read().split(",")
keywords = sents[0].split("\n")
keyword_file.close()


righttopics = ["Paikkakunnat","Terveys"]
stopwords_file = open("../scraper-test/finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()
#location of json folder to read data from
files = listdir("../scraper-test/textdumps")
punc = set(string.punctuation)

#simple checking if the string contains wrong messages

#Check if the thread is in the correct topics
def checkTopic(topics,righttopics):
    for topic in topics:
        if topic["title"] in righttopics:
            return False
    return True
#Handling final checks of the sentences before actual words are added
def addSentence(w):
    #wordlist=[word for word in w.split()]
    #print w
    l = [word for word in w.split(u'\t')]
    print(l)
    """
        for i in range(len(wordlist)):
        for j in range(i+1,len(wordlist)):
            #print("test1")
            #print(wordlist[i],wordlist[j])
            if len(wordlist[i]) >= 2 and len(wordlist[j]) >= 2 and wordlist[i]!=wordlist[j] and wordlist[i] != " " and wordlist[j] != " ":
                #print("test2")
                addword((wordlist[i],wordlist[j]),j-i)
"""


#Helper function to remove odd characters from single words
def checkWord(wrd):
    return re.sub(r'[^a-zA-Z0-9åäöÅÄÖ]','',wrd)

def checkSentence(string):
    ret = []
    sents = nltk.sent_tokenize(string)
    for s in sents:
        tmp = ""
        if "http" in s:
            #print("http")
            continue

        tokens = nltk.word_tokenize(s)
        for w in tokens:
            w=checkWord(w)
            #if w.lower() in stopwords:
                #print(w)
            #    tmp+="<poistettu>"+" "
            #    continue
            if len(w)<2:
                continue
            tmp+=w+" "

        ret.append(tmp)
    return ret

def convertToConllu(sent):
    #sent = sent,"utf-8".rstrip()
    tokens = sent.split()
    newSent=""
    for tIdx,t in enumerate(tokens):
         newSent+=(u"%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\n"%(tIdx+1,t)) #.encode("utf-8")
    return newSent

for fileN in files:
    if fileN.endswith(".json"):
        filename="../scraper-test/textdumps/{}".format(fileN)
    else:
        continue
    with open(filename) as f:
        print(filename)
        try:
            items = ijson.items(f,"item")
            for o in items:
                if checkTopic(o["topics"],righttopics) or o["deleted"] is True:
                    continue
                body = o["body"]
                if search_keywords(body,keywords):
                    body = checkSentence(body)
                    for sentence in body:
                        newSentence = convertToConllu(sentence)
                        with open('tempSent.txt','w+') as f:
                            f.write(newSentence)
                        subprocess.call('cat tempSent.txt | ./parse_conll.sh > output.conllu',shell=True)

                        with codecs.open('output.conllu',u'rt',u'utf-8') as f:
                            for line in f:
                                l = line.strip()
                                addSentence(l)
                        data["threads"]+=1

                    for c in o["comments"]:
                        if c["deleted"] is True:
                            continue
                        sent = c["body"]
                        #if (search_keywords(s,keywords)==True):
                        sent = checkSentence(sent)
                        for s in sent:
                            data["comments"]+=1
                            #cleanC = [word for word in body.split() if word.lower() not in stopwords]
                            addSentence(s)

        except ValueError:
            print("ValueError")
            continue
        except ijson.common.IncompleteJSONError:
            print("IncompleteJSONError")
            continue
        writeToFile()

#pprint(data)
