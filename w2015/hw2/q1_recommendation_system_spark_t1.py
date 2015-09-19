# Under the PySpark shell, type:
# execfile('q1_recommendation_system_spark_t1.py')

#from pyspark import SparkContext, SparkConf
# conf = SparkConf()
# conf.setMaster("local")
# conf.setAppName("Recommendation System")
# conf.set("spark.executor.memory", "16g")
#sc = SparkContext(conf=conf)
# from scipy.spatial import distance
#from scipy.spatial import distance as dt
from collections import Counter
import numpy as np

def center_vector(vector): #[7, 6, 0, 2] => [2, 1, 0, -3] (center only on nonzeros)
  mean = float( sum(vector) ) / np.nonzero(vector)[0].size
  return [0 if item == 0 else item - mean for item in vector]

def pearson_nonzero(list1, list2):
  return np.corrcoef(center_vector(list1), center_vector(list2))[0, 1]

def parse_line(line):
  return [ int(item) for item in line.split() ]

def map_tops(row, topN=2):
  self_data, counter = [], Counter()
  for original_data_pair, (id_pair, similarity) in row: #([5, 0, 4, 0, 0, 0], [0, 0, 2, 5, 4, 3]) (8, 4) 0.4743
    print "\nline 31: ", original_data_pair, id_pair, similarity
    self_data = original_data_pair[0]
    counter[ id_pair[1] ] = similarity, original_data_pair[1]
  return self_data, dict(counter.most_common( topN ))

#fileName = 'q1-dataset/q1-dataset/user-shows.txt'
fileName = '07-recsys1.txt'
topN     = 2
dataRDD  = (sc.textFile(fileName) #partition goes here
             .map( parse_line )
             .zipWithIndex()   #([count, count,...], line#) just like (data, id)
           )

suggestRDD = (dataRDD
              .cartesian( dataRDD ) #get all possible permutations
              .filter(lambda ((data1, id1), (data2, id2)): id1 != id2 ) #remove self-self combination
              .map(lambda ((data1, id1), (data2, id2)): (id1, ((data1, data2), ( (id1, id2), pearson_nonzero(data1, data2) ) )  ) )  
              .groupByKey()
              .mapValues( map_tops )
              # # 
              )


#print dataRDD
print suggestRDD.take(2)
#print suggestRDD.count()
