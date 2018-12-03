from polyglot.text import Text
import codecs
import subprocess

def polyglotPOS(text):
    text=Text(text)
    return text.pos_tags

def turkuParser(body):
    for sentence in body:
        newSentence = convertToConllu(sentence)
        with open('tempSent.txt','w+') as f:
            f.write(newSentence)
        subprocess.call('cat tempSent.txt | ./parse_conll.sh > output.conllu',shell=True)

        with codecs.open('output.conllu',u'rt',u'utf-8') as f:
            for line in f:
                l = line.strip()   
                print(l) 

def convertToConllu(sent):
    #sent = sent,"utf-8".rstrip()
    tokens = sent.split()
    newSent=""
    for tIdx,t in enumerate(tokens):
         newSent+=(u"%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\n"%(tIdx+1,t)) #.encode("utf-8")
    return newSent


from io import open
from conllu import parse_tree_incr

def readConllu(filename):
    data_file = open(filename, "r", encoding="utf-8")
    for tokentree in parse_tree_incr(data_file):
        print(tokentree)

def omorfi(input):
    pass