import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from sm_settings import SMSettings
from sm_sentimental_analysis import SmSentimentalAnalysis
from fake_test_data import FakeTestData
import pandas as pd

import csv

import unittest

class TestSmSentimentalAnalysis(unittest.TestCase):

    def setUp(self):
        self.test_sm_sentimental_analysis =  SmSentimentalAnalysis()

    def test_classify_tweets(self):
        self.user_data_folder_path =  SMSettings.paths['dataForClassifications'].format(FakeTestData.twitter_screen_name)
        csv_data_file = self.user_data_folder_path+"MohammedAssaf89_1129084011664597001.csv"
        with open(csv_data_file) as csvfile:
             reader = csv.DictReader(csvfile)
             for row in reader:
                 self.test_sm_sentimental_analysis.predict_real_data(row["text"])


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
