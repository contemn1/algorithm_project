import pdb, traceback, sys
import operator

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

def simrank(G, G_sq):
  C=0.8
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
  for k in range(20):
    for node in G_sq:
      x = node[0] #don't call it a and b b/c messes it up in pdb?
      y = node[1]
      if x != y:
        sim_sum = 0
        for neighbor1 in G[x]:
          for neighbor2 in G[y]:
            sim_sum += node_scores[(neighbor1,neighbor2)] 
        new_sim = (C/(len(G[x]) * len(G[y]))) * sim_sum
      #if new_sim != node_scores[(x,y)]:
        #cont = on
        node_scores[(x,y)] = new_sim

  node_scores = { k:v for k, v in node_scores.items() if v < 1 }
  sorted_scores = sorted(node_scores.items(), key=operator.itemgetter(1))
  sorted_scores.reverse()
  return sorted_scores

def make_list_scores(filename, pair_list):
  output = open(filename,'w')
  for pair in pair_list: 
    row = str(pair[0]) + ' : ' + str(pair[1])
    output.write(row + '\n')
  output.close()

def main():
  #adjacency list of tweets (not hashtags). Test the functions
  G = {'a': [1,2], 'b': [2,3], 1:['a'], 2:['a','b'],3:['b']}
  G_sq = create_G_sq(G) 
  fn = 'C:\Users\Michael\Documents\_rsch\classes sp17/algo\project code/trial 2/sample_scores.txt'
  make_list_scores(fn,simrank(G, G_sq))

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
