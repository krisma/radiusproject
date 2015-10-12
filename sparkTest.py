from pyspark import SparkConf, SparkContext
from time import time
import sys

# sys.path.append('~/Desktop/Radius Collider/radiusproject/')

sc = SparkContext(appName="myApp")

l = []
for i in range(2**22):
	l.append(i)

data = sc.parallelize(l)

t0 = time()
data.map(lambda x: x * 2)
t1 = time()
print 'time taken = ' + repr(t1-t0) + '\n'

t0 = time()
map(lambda x: x * 2, l)
t1 = time()
print 'time taken = ' + repr(t1-t0) + '\n'