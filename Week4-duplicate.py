from scipy import spatial
import pandas as pd
import numpy as np
import math

#Reading the tapas-csv file
telecom = pd.read_csv("tapas.csv")
telecom.head()
print(telecom.shape)
print()
print(telecom.describe())
print()
print(telecom.info())
print()
print()

#Initializing the arrays
dataSetI = []
dataSetII = []

#Opening the file, and adjusting to find the int part of the line
f = open("tapas.csv", "r")
count = 0
for x in f:
  dataset_views1 = x.rpartition(': ')
  if(count % 2 == 0):
    dataSetI.append(int(dataset_views1[2]))
  else:
      dataSetII.append(int(dataset_views1[2]))
  count += 1


#Function to calculate cosine similarity
def cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

v1,v2 = dataSetI, dataSetII
print(v1, v2)
print("The cosine similarity of the two data is", cosine_similarity(v1, v2))
