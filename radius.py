import json
from abstractions import Company
from utils import *
from random import sample
from pyspark import SparkConf, SparkContext, sql
from time import time

sc = SparkContext(appName="myApp")

NumOfClusters = 20
exclusion = ['service', 'has', 'years', 'one', 'with', 'experience', 'more', 
'company', 'also', 'clients', 'provide', 'home', 'needs', 'services', 'have', 
'best', 'for', 'an', 'as', 'at', 'be', 'by', 'all', 'the', 'products', 'i', 'new', 
'is', 'it', 'in', 'from', 'our', 'their', 'on', 'or', 'to', 'us', 'inc', 'we', 
'can', 'care', 'family', 'help', 'and', 'offer', 'this', 'of', 'that', 'business', 
'your', 'you', 'a', 'quality', 'over', 'are', 'will']

def stats(companies):
	wordStats = dict()
	for company in companies:
		merge(wordStats, company.coordinate())
	return wordStats

# Find the closest centroid to a given company.
def find_closest(company, centroids):
	return max(centroids, key=lambda c: company.closeness(c))

def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    pairs = pairs.collect()
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]
    # keys = sc.parallelize(keys)
    # result = keys.map(lambda key: [y for x, y in pairs if x == key])
    # return result

def group_by_centroid(companies, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # companies_centroids=[[find_closest(c,centroids), c] for c in companies]
    # centroids = centroids.collect()
    result = companies.map(lambda c: [find_closest(c,centroids), c])
    # result = result.groupByKey()
    # result = result.map(lambda x: x[1])
    # return result
    result = group_by_first(result)
    return result


def find_centroid(cluster):
    """Return the centroid of the locations of the companies in cluster."""
    size = float(len(cluster))
    temp = [company.coordinate() for company in cluster]
    rtn = dict()
    for coordinate in temp:
    	merge(rtn, coordinate)
    for key in rtn:
    	rtn[key] /= size
    l = [[key, rtn[key]] for key in rtn]
    l.sort(key=lambda x: -x[1])
    l = l[:20]
    rtn = dict()
    for elem in l:
    	rtn[elem[0]] = elem[1]
    return rtn

def k_means(companies, max_updates=1):
    """Use k-means to group restaurants by location into k clusters."""
    assert companies.count() >= NumOfClusters, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    # sample = sc.parallelize(companies.takeSample(True, NumOfClusters))
    sample = companies.takeSample(True, NumOfClusters)
    centroids = [s.coordinate() for s in sample]
    # centroids = sample.map(lambda company: company.coordinate())

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        clusters = group_by_centroid(companies, old_centroids)
        centroids = [find_centroid(cluster) for cluster in clusters]
        # centroids = clusters.map(lambda cluster: find_centroid(cluster))
        n += 1
    return centroids



# @main
def main(*args):
    data = json.load(open('challenge_set.json'))
    # wordStats = stats(companies)
    # exclusion = []
    # for stat in wordStats:
    #     if wordStats[stat] > 1000:
    #         exclusion.append(stat)
    # print(exclusion)
    #   if wordStats[stat] > 100 and wordStats[stat] < 150 :
    #       print (stat, wordStats[stat])
	# print (stat, wordStats[stat])
	# print(len(wordStats))

    # start = time()
  #   companies = [Company(j, exclusion) for j in data]
  #   end = time()
  #   print 'time taken = ' + repr(end - start)

  #   centroids = k_means(companies)
  #   for c in centroids:
		# l = [key for key in c]
		# print('centroid is: ' + repr(l) + '\n')

    companies = sc.parallelize(data).map(lambda j: Company(j, exclusion))

    start = time()
    centroids = k_means(companies)
    end = time()
    print 'total time taken = ' + repr(end - start)
    for centroid in centroids:
        print [key for key in centroid]
        print '\n'


if __name__ == "__main__":
	main()
