# extended edit distance
#coding:utf-8
import re, math
from gensim.models.keyedvectors import KeyedVectors

model = KeyedVectors.load_word2vec_format('/Users/lingfeizeng/MSDS/CS512/project/google.bin', binary=True)

WORD = re.compile(r'\w+')

def sentence_to_word(sentence):
    sentence = re.sub("[^a-zA-Z]", " ", sentence.lower())
    words = WORD.findall(sentence)
    return words

def edit_distance(s1, s2):

    words_1 = sentence_to_word(s1)
    words_2 = sentence_to_word(s2)

    m=len(words_1)+1
    n=len(words_2)+1

    tbl = {} # k: v
    bestMove={}
    for i in range(m):
        tbl[i,0]=i
        bestMove[i, 0] = 'D'

    for j in range(n):
        tbl[0,j]=j
        bestMove[0, j] = 'I'


    for i in range(1, m):
        for j in range(1, n):
            #cost = 0 if words_1[i-1] == words_2[j-1] else 1
            if words_1[i-1] == words_2[j-1]:
                cost = 0
                minVal = 10000000
                if tbl[i, j - 1] + 1 < minVal:
                    minVal = tbl[i, j - 1] + 1
                    bestMove[i, j] = 'D'
                if tbl[i - 1, j] + 1 < minVal:
                    minVal = tbl[i - 1, j] + 1
                    bestMove[i, j] = 'I'
                if tbl[i - 1, j - 1] + cost < minVal:
                    minVal = tbl[i - 1, j - 1] + cost
                    bestMove[i, j] = ' ' # meaning that this is not a real replacement, both sides shift right by one
            else:
                try:
                    word2vec_cost = 1 - model.similarity(words_1[i - 1], words_2[j - 1])
                except KeyError, e:
                    word2vec_cost = 1  # expected value of unknown words

                cost = 2*word2vec_cost

                #print words_1[i-1], words_2[j-1], word2vec_cost

                minVal = 10000000
                if tbl[i, j - 1] + 1 < minVal:
                    minVal = tbl[i, j - 1] + 1
                    bestMove[i, j] = 'D'
                if tbl[i - 1, j] + 1 < minVal:
                    minVal = tbl[i - 1, j] + 1
                    bestMove[i, j] = 'I'
                if tbl[i - 1, j - 1] + cost < minVal:
                    minVal = tbl[i - 1, j - 1] + cost
                    bestMove[i, j] = 'R'




            tbl[i, j] = minVal
            #tbl[(i,j)] = min(tbl[(i, j-1)]+1, tbl[(i-1, j)]+1, tbl[(i-1, j-1)]+cost)

    iTmp = i
    jTmp = j
    counting = 0
    while True:
        #print(iTmp,jTmp)
        if bestMove[iTmp, jTmp] == 'R' or bestMove[iTmp, jTmp] == ' ':
            if bestMove[iTmp, jTmp] == 'R':
                #print('R')
                counting += 1
            #else:
                #print('both sides move forward by one')

            iTmp -= 1
            jTmp -= 1
        elif bestMove[iTmp, jTmp] == 'D':

            #print('D')
            jTmp -= 1
        elif bestMove[iTmp, jTmp] == 'I':

            #print('I')
            iTmp -= 1

        if iTmp == 0 or jTmp == 0:
            break


    #print("replace#", counting)


    counting += max(m-1,n-1)
    return tbl[i,j]/counting


import pandas as pd
import numpy as np
import collections

# input data, generate distance matrix

tweets = pd.read_csv('.\tweets.csv')
n = len(tweets)
tweets_content = tweets["Tweet content"][:n]
print tweets_content


score = {}
for i in range(0, n):
    for j in range(0, n):
        s1 = tweets_content[i]
        s2 = tweets_content[j]
        score[i, j] = edit_distance(s1, s2)


oscore = collections.OrderedDict(sorted(score.items()))

oscore = np.matrix(oscore.values()).reshape(n,n)

print oscore






