import unittest
from crawler import crawler
from crawler import page_rank


# Here's our "unit tests".
class IsOk(unittest.TestCase):

	def testOne(self):
		bot = crawler(None, "urls.txt")
		bot.crawl(depth=2)
		inverted_index = bot.inverted_index()
		print inverted_index
		expected_inverted_index = {1: set([1, 3]), 2: set([1]), 3: set([2])}

		
		got_page_rank = page_rank(bot.links())
		expected_page_rank = {1: 0.05000000000000001, 2: 0.092500000000000027, 3: 0.12862500000000002}
		

		self.failUnless(inverted_index == expected_inverted_index)
		self.failUnless(got_page_rank == expected_page_rank)

def main():
	unittest.main()

if __name__ == '__main__':
	main()