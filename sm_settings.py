import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

class SMSettings:
    default_lang = 'ar'
    paths = {
        'trainingDataSets' : currentdir+'/trainingDataSets/{}/',
        'dataForClassifications': currentdir+'/dataForClassifications/{}/'
    }
    training_dataset_name = 'data_warehouse_all.csv'
    test_dataset_name = 'test_tweets_data_all.csv'
    twitter_app_settings = {
        'consumer_key': '',
        'consumer_secret': '',
        'access_token': '',
        'access_secret': ''
    }
