import pdb
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os

X=8
Y=1
scores = []
cwd = os.getcwd()
f = open(cwd + '\data_'+str(X)+'_gen_'+str(Y)+'_scores.txt', 'r')
for line in f:
	splitted = line.split()
	if float(splitted[-1]) > 0.05: #float may cause float(0) to be slightly > 0
		scores.append(float(splitted[-1]))

plt.hist(scores)
plt.show()