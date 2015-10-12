# PiSolver class, co-authored by Yuxuan Luo, Weijian Ma, Ge Wu
# Predicts the NAICS code according to given business information
#
# All rights reserved.

import requests
from HTMLParser import HTMLParser




class PiSolver(object):
	def __init__(self):
		self.httpGetter = HttpGetter()
		self.htmlParser = MyHTMLParser()

	
	def __setup__(self, labelingDict):
		pass
	def parseWebsite(self, url):
		# url: link to website with protocol type
		# return: content on the website parsed in text
		self.httpGetter.request(url)
		self.htmlParser.feed(self.httpGetter.getLastRequestContent())
		rtn = self.htmlParser.result
		self.htmlParser.reset_result()
		return rtn

class HttpGetter(object):
	def __init__(self, 
		accept='*/*',
		acceptEncoding="gzip, deflate, sdch",
		acceptLanguage="en-US,en;q=0.8,zh-CN;q=0.6",
		userAgent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"):
		self.lastRequest = ""
		self.payload = {
		'Accept': accept,
		'Accept-Encoding': acceptEncoding,
		'Accept-Language': acceptLanguage,
		'User-Agent': userAgent}
	def request(self, url):
		self.lastRequest = requests.get(url, params=self.payload)
	def getLastRequestContent(self):
		return self.lastRequest.content

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.lastTag = ''
		self.result = ''
	def handle_starttag(self, tag, attrs):
		self.lastTag = tag
	def handle_data(self, data):
		if not self.lastTag in ['style', 'meta', 'script']:
			self.result += ' ' + data
	def reset_result(self):
		self.lastTag = ''
		self.result = ''

# TESTING
# p = PiSolver()
# p.parseWebsite("http://www.baidu.com")