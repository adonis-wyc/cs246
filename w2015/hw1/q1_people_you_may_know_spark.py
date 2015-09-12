# execfile('friend_you_may_know.py')

#fileName = 'q1testdata.txt'
#from pyspark import SparkContext, SparkConf
# conf = SparkConf()
# conf.setMaster("local")
# conf.setAppName("Friends you may know")
# conf.set("spark.executor.memory", "16g")
#sc = SparkContext(conf=conf)

import itertools

fileName = 'soc-LiveJournal1Adj.txt'

def connecteds_and_commons(line):
  minimum = -9999999999
  user, friends = line.split('\t')
  friends = friends.split(',')
  connecteds = [((user, friend), minimum) for friend in friends]
  commons = [(pair, 1) for pair in itertools.permutations(friends, 2)]
  return connecteds + commons

friendsListRDD = (sc
                  .textFile( fileName, 16 )
                  .flatMap( connecteds_and_commons )
                  .reduceByKey( lambda total, current: total + current )
                  .filter(lambda (pair, counts): counts > 0)
                  .map(lambda ((user, friend), counts): (user, (counts, friend)))
                  .groupByKey()
                  .map(lambda (user, suggestions):(user, sorted(list(suggestions), reverse=True)))
                  #.cache()
                   )


print "924"
print friendsListRDD.lookup('924')
#print friendsListRDD.collect()