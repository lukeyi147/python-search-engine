import unittest
from crawler import crawler


# Here's our "unit tests".
class IsOk(unittest.TestCase):

	def testOne(self):
		bot = crawler(None, "urls.txt")
		bot.crawl(depth=2)
		inverted_index = bot.inverted_index()
		resolved_inverted_index = bot.resolved_inverted_index()

		expected_inverted_index = bot.inverted_index()
		expected_resolved_inverted_index = bot.resolved_inverted_index()

		self.failUnless(inverted_index == expected_inverted_index)
		self.failUnless(resolved_inverted_index == expected_resolved_inverted_index)

def main():
	unittest.main()

if __name__ == '__main__':
	main()