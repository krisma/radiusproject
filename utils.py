from random import sample

# def zip(*sequences):
#     """Returns a list of lists, where the i-th list contains the i-th
#     element from each of the argument sequences.

#     >>> zip(range(0, 3), range(3, 6))
#     [[0, 3], [1, 4], [2, 5]]
#     >>> for a, b in zip([1, 2, 3], [4, 5, 6]):
#     ...     print(a, b)
#     1 4
#     2 5
#     3 6
#     >>> for triple in zip(['a', 'b', 'c'], [1, 2, 3], ['do', 're', 'mi']):
#     ...     print(triple)
#     ['a', 1, 'do']
#     ['b', 2, 're']
#     ['c', 3, 'mi']
#     """
#     return list(map(list, _zip(*sequences)))

def merge(dict1, dict2):
	for key in dict2:
		value = dict2[key]
		if key in dict1:
			dict1[key] += value
		else:
			dict1[key] = value
	return dict1
