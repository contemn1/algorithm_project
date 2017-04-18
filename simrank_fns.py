import pdb, traceback, sys
import csv
import operator
import collections

#compute distance between two graphs. If > 5, do not calculate a pair for them
#Create a bipartite graph of tweets and hashtags. Map each tweet to a pos int ID and each hashtag to a neg int ID
def create_graph(data_file):
  graph_dict = {}
  tweet_labels = {}
  hashtag_labels = {}
  i=1
  j = -1
  k=1
  f = open(data_file, 'r')
  hashtags = []
  hashtag_labels = {} #id : hashtag
  hashtag_labels_flip = {} #hashtag : id
  for tweet in f:
    if k > 1000: #b/c MemoryError, so only look at 500 tweets; k < 1000. Cannot use k > 5000. Even when using neg integers for hashtags
      break
    else:
      if '#' in tweet: #for now, only consider tweets with hashtags in them. 
        tweet_labels[i] = tweet #assign id i as tweet
        graph_dict[i] = [] 
        splitted_tweet = tweet.split()
        for word in splitted_tweet:
          if '#' in word and len(word) > 1: #if hashtag that's not just '#'
            if word not in hashtag_labels_flip:  #if it's a new hashtag
              hashtag_labels[j] = word #assign id j as hashtag
              hashtag_labels_flip[word] = j #assign hashtag as id j
              #the neighbors of hashtag j (even tho directed graph, this is for algos to know hashtag's neighbors)
              graph_dict[j] = [i] #create new hashtag entry in dictionary
              j -= 1
            else:
              graph_dict[hashtag_labels_flip[word]].append(i) #add onto old hashtag entry in dictionary
            if word not in graph_dict[i]: #avoid duplicate hashtags. Put this after labeling hashtags to id's
              graph_dict[i].append(hashtag_labels_flip[word]) #add hashtag to neighbors of tweet i
        if graph_dict[i] == []: #just in case tweet only contains words '#' of len 1
          del graph_dict[i]
        else:
          i += 1
    k += 1
  return graph_dict, tweet_labels, hashtag_labels

#Create G^2
def create_G_sq(G):
  G_sq = {}
  for tw_1 in G:
    for tw_2 in G:
      if (tw_1,tw_2) not in G_sq or (tw_2,tw_1) not in G_sq:
        #if type(tw_1) == type(tw_2):
        if tw_1 * tw_2 > 0:
          G_sq[(tw_1,tw_2)] = []
          for ht_1 in G[tw_1]:    #add in hashtag pair nodes
            for ht_2 in G[tw_2]:
              G_sq[(tw_1,tw_2)].append((ht_1,ht_2))
              if (ht_1,ht_2) not in G_sq or (ht_2,ht_1) not in G_sq:   #hashtag nodes
                G_sq[(ht_1,ht_2)] = [(tw_1,tw_2)]
              else:
                G_sq[(ht_1,ht_2)].append((tw_1,tw_2))
  return G_sq     

#run SimRank on G^2 to calculate similarity scores
def simrank(G, G_sq):
  C=0.8 #decay factor
  node_scores={}
  for node in G_sq:
    x = node[0]
    y = node[1]
    if x == y:
      node_scores[(x,y)] = 1
    else:
      node_scores[(x,y)] = 0

  #cont = on
  #while cont == on:
    #cont = off
  for k in range(20): #20 iterations
    for node in G_sq:
      x = node[0] #don't call it a and b b/c messes it up in pdb?
      y = node[1]
      if x != y:
        sim_sum = 0
        for neighbor1 in G[x]:
          for neighbor2 in G[y]:
            sim_sum += node_scores[(neighbor1,neighbor2)] 
        new_sim = (C/(len(G[x]) * len(G[y]))) * sim_sum
      #if new_sim != node_scores[(x,y)]: #if the prev score differs, continue
        #cont = on
        #if new_sim > 0: #only keep those that are > 0
        node_scores[(x,y)] = new_sim

  node_scores = { k:v for k, v in node_scores.items() if v < 1 } #sort by item, so can't use orderedDict
  sorted_scores = sorted(node_scores.items(), key=operator.itemgetter(1))
  sorted_scores.reverse()
  return node_scores, sorted_scores

#take in dictionary and return key : value list
def make_list(filename,input_dict):
  output = open(filename,'w')
  for head in input_dict: 
    row = str(head) + ' : ' + str(input_dict[head])
    output.write(row + '\n')
  output.close()

#take in list of tuples and return key : value list
def make_list_scores(filename, pair_list):
  output = open(filename,'w')
  for pair in pair_list: 
    row = str(pair[0]) + ' : ' + str(pair[1])
    output.write(row + '\n')
  output.close()

def make_graph_csv(filename, graph_dict,hashtag_labels):
  csv = open(filename,"w")
  for v in graph_dict: 
      row=str(v)
      edges = graph_dict[v]
      for t in edges:
          row += ';' + str(t)
      csv.write(row + '\n')
  #for v in hashtag_labels.values():
    #csv.write(str(v) + '\n')
  csv.close()

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


