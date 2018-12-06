#!/usr/bin/env python
# -*- coding: utf-8 -*-
from finnish_toolkit import helper,firebase_key
from finnish_toolkit import finnish_keywords as keywords
from os import listdir,remove
from pprint import pprint
import string
import nltk
import re
import datetime
import pyrebase

wordcount = {}

#Load keywords and stopwords, and define characters to be removed
stopwords_file = open("./finnish_toolkit/finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()

# punctuation loading
punc = set(string.punctuation)

# firebase initialization
firebase = pyrebase.initialize_app(firebase_key.pyrebase_config)
db = firebase.database()
kw=db.child("keywords").get()

#check if one of the keywords exist in the given string
def search_keywords(string):
    keywords_found=[]
    #keywords_found={"death":0,"illness":0,"treatment":0,"social":0,"financial":0}
    for word in kw.val()["death"]:
        if word in string.lower():
            keywords_found.append("death")
            #keywords_found["death"]=1
            break
    for word in kw.val()["illness"]:
        if word in string.lower():
            keywords_found.append("illness")
            #keywords_found["illness"]=1
            break
    for word in kw.val()["treatment"]:
        if word in string.lower():
            keywords_found.append("treatment")
            #keywords_found["treatment"]=1
            break
    for word in kw.val()["social"]:
        if word in string.lower():
            keywords_found.append("social")
            #keywords_found["social"]=1
            break
    for word in kw.val()["financial"]:
        if word in string.lower():
            keywords_found.append("financial")
            #keywords_found["financial"]=1
            break
    return keywords_found

#helper function to add word into the dictionary
def addword(word,dist,topics,comment,time,nicknames):
    if dist>25:
        return
    if word not in wordcount:
        wordcount[word] = {}
        wordcount[word]["wordDistance"]=addDistance(dist)
        wordcount[word]["subforums"]=formatIntoDict(topics)
        #wordcount[word]["keyWords"]=formatIntoDict(foundKeywords)
        wordcount[word]["isComment"]=isComment(comment)
        wordcount[word]["nicknames"]=formatIntoDict(nicknames)
        wordcount[word]["postTimes"]=formatIntoDict(time)
    else:
        vals = addDistance(dist)
        #kvals = formatIntoDict(foundKeywords)
        tvals = formatIntoDict(topics)
        nvals = formatIntoDict(nicknames)
        timevals=formatIntoDict(time)
        cvals = isComment(comment)
        obj = wordcount[word]
        addStuff(obj["wordDistance"],vals)
        #addStuff(obj["keyWords"],kvals)
        addStuff(obj["subforums"],tvals)
        addStuff(obj["nicknames"],nvals)
        addStuff(obj["postTimes"],timevals)
        addStuff(obj["isComment"],cvals)

def isComment(b):
    if b:
        return {"inComments":1}
    else:
        return {"inTopic":1}

def addStuff(obj,vals):
    for k in vals:
        try:
            obj[k] += vals[k]
        except KeyError:
            obj[k] = vals[k]

def formatIntoDict(items):
    itemList={}
    for w in items:
        itemList[w]=1
    return itemList

def addDistance(dist):
    #a = {"1-2":0,"3-5":0,"6-8":0,"8-14":0,"15+":0}
    a={}
    if dist<3:
        a["1-2"]=1
    elif dist<6:
        a["3-5"]=1
    elif dist<9:
        a["6-8"]=1
    elif dist<15:
        a["8-14"]=1
    else:
        a["15+"]=1
    return a

def addNewValues(dbobj,newobj):
    addStuff(dbobj["wordDistance"],newobj["wordDistance"])
    addStuff(dbobj["topics"],newobj["topics"])
    #addStuff(dbobj["keyWords"],newobj["keyWords"])
    return dbobj

#Check if the thread is in the correct topics
def checkTopic(topics,righttopics):
    for topic in topics:
        if topic["title"] in righttopics:
            return False
            #return checkSubtopic(topics)
    return True

#def checkSubtopic(topics)

#helper function to extract onlif keywords_found:

def extractTopics(topics):
    retTopics=[]
    for t in topics:
        retTopics.append(t["title"])
    return retTopics

#Handling final checks of the sentences before actual words are added
def addSentence(w,topics,comment,time,nicknames):
    #print(w)
    wordlist=[word for word in w.split()]
    for i in range(len(wordlist)):
        for j in range(i+1,len(wordlist)):
            #print("test1")
            #print(wordlist[i],wordlist[j])
            if wordlist[i] == "<poistettu>" or wordlist[j] == "<poistettu>":
                continue
            if len(wordlist[i]) > 2 and len(wordlist[j]) > 2 and wordlist[i]!=wordlist[j] and wordlist[i] != " " and wordlist[j] != " ":
                #print("test2")
                addword((wordlist[i],wordlist[j]),j-i,topics,comment,time,nicknames)



#Helper function to remove odd characters from single words
def checkWord(wrd):
    return re.sub(r'[^\w0-9]','',wrd)

def checkSentence(string):
    ret = []
    sents = nltk.sent_tokenize(string)
    for s in sents:
        tmp = ""
        if "http" in s or "json" in s:
            #print("http")
            continue
        tokens = nltk.word_tokenize(s)
        for w in tokens:
            w=checkWord(w)
            w=w.lower()
            if w in stopwords:
                #print(w)
                tmp+="<poistettu>"+" "
                continue
            tmp+=w+" "
        ret.append(tmp)
    return ret

def getValueIntoList(val):
    ret = []

    ret.append(val)
    return ret
def getDateString(unixts):
    obj=[]
    d=datetime.datetime.fromtimestamp(unixts/1000).strftime("%m-%Y")
    obj.append(d)
    return obj
