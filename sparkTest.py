from pyspark import SparkConf, SparkContext
from time import time
import sys

# sys.path.append('~/Desktop/Radius Collider/radiusproject/')

sc = SparkContext(appName="myApp")

l = range(2**25)

# t0 = time()
t0 = time()
data = sc.parallelize(l)
data.map(lambda x: x * 2).map(lambda x: x * 2).map(lambda x: x * 2)
t1 = time()
print 'spark time taken = ' + repr(t1-t0)

t0 = time()
map(lambda x: x * 2, map(lambda x: x * 2, map(lambda x: x * 2, l)))
t1 = time()
print 'normal time taken = ' + repr(t1-t0)