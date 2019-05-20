import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


from sm_twitter_collector import SMTwitterCollector
from fake_test_data import FakeTestData
import unittest

class TestSmTwitterCollector(unittest.TestCase):

    def setUp(self):
        self.sm_twitter_collector =  SMTwitterCollector(FakeTestData.twitter_screen_name)

    def test_get_tweets(self):
        self.assertTrue(self.sm_twitter_collector.get_user_tweets(5) != None)

    def test_prepare_classification(self):
        (max_id, user_json_file) = self.sm_twitter_collector.get_user_tweets(5)
        (status, user_csv_file) = self.sm_twitter_collector.process_tweets_json_to_csv(max_id)
        self.assertTrue(status)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
