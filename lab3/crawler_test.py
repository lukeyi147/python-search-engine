import unittest
from crawler import crawler


# Here's our "unit tests".
class IsOk(unittest.TestCase):

	def testOne(self):
		bot = crawler(None, "urls.txt")
		bot.crawl(depth=2)
		inverted_index = bot.inverted_index()
		resolved_inverted_index = bot.resolved_inverted_index()

		expected_inverted_index = {1: set([1, 2]), 2: set([1, 2])}
		expected_resolved_inverted_index = {u'index2': set(['http://hhaider.github.io/mygithubpage/index.html', u'http://hhaider.github.io/mygithubpage/index2.html']), u'index': set(['http://hhaider.github.io/mygithubpage/index.html', u'http://hhaider.github.io/mygithubpage/index2.html'])}

		self.failUnless(inverted_index == expected_inverted_index)
		self.failUnless(resolved_inverted_index == expected_resolved_inverted_index)

def main():
	unittest.main()

if __name__ == '__main__':
	main()