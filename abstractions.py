import re

# The Company Object
class Company:
	def __init__(self, json, exclusion=[]):
		self.name = json['name']
		self.address = json['address']
		self.description = json['description']
		self.website = json['website']
		self.unique_id = json['unique_id']
		self.exclusion = exclusion

	def coordinate(self):
		repl = '[/"~&:!,.\-\'\d]'
		nameWords = [s for s in re.sub(repl, '', self.name).encode('utf-8').lower().split() if s not in self.exclusion]
		desWords = [s for s in re.sub(repl, '', self.description).encode('utf-8').lower().split() if s not in self.exclusion]
		rtn = dict()
		for key in (nameWords + desWords):
			if key not in rtn:
				rtn[key] = 1
			else:
				rtn[key] += 1
		return rtn

	def closeness(self, compare):
		myCoordinate = self.coordinate()
		if type(compare) == Company:
			compare = compare.coordinate()
		rtn = 0
		for key in myCoordinate:
			if key in compare:
				rtn += myCoordinate[key] * compare[key]
		return rtn

	