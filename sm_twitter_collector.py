from sm_settings import SMSettings
import tweepy  # https://github.com/tweepy/tweepy
import os,sys,inspect
import api_keys
import pathlib
import simplejson as json

class SMTwitterCollector:
    twitter_api = None
    tweets_repo_array = []
    def __init__(self):
        auth = tweepy.OAuthHandler(SMSettings.twitter_app_settings['consumer_key'], SMSettings.twitter_app_settings['consumer_secret'])
        auth.set_access_token(SMSettings.twitter_app_settings['access_token'], SMSettings.twitter_app_settings['access_secret'])
        self.twitter_api = tweepy.API(auth)

    def _check_data_collected_before(self, user_data_folder_path, max_id):
        saved_tweets_files = os.listdir(user_data_folder_path)
        for saved_tweets_file in saved_tweets_files:
            splited_file_name = saved_tweets_file.split("_")
            if(str(max_id) == str(splited_file_name[1])):
                return True, saved_tweets_file
        return False, None

    def get_user_tweets(self, screen_name):
        collected_before = False
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        user_data_folder_path = currentdir + "/" + SMSettings.paths['dataForClassifications'].format(screen_name)

        new_tweets = self.twitter_api.user_timeline(screen_name=screen_name, count=200,
                                           tweet_mode='extended')

        self.tweets_repo_array.extend(new_tweets)
        first_tweet_id = self.tweets_repo_array[-1].id - 1
        max_tweet_id = self.tweets_repo_array[1].id

        if not os.path.exists(user_data_folder_path):
            pathlib.Path(user_data_folder_path).mkdir(parents=True, exist_ok=True)
        else:
            (collected_before, user_json_file) = self._check_data_collected_before(user_data_folder_path, max_tweet_id)
        if(collected_before):
            return user_json_file
        #recursive looping
        while len(new_tweets) > 0:
            print("getting tweets before {}".format(first_tweet_id))

            new_tweets = self.twitter_api.user_timeline(screen_name=screen_name, count=200,
                                           max_id=first_tweet_id, tweet_mode='extended')

            self.tweets_repo_array.extend(new_tweets)
            first_tweet_id = self.tweets_repo_array[-1].id - 1

        min_id = self.tweets_repo_array[-1].id
        max_id = self.tweets_repo_array[1].id

        user_json_file = user_data_folder_path+'{}.json'.format(screen_name + "_" + str(max_id) + "_" + str(min_id))

        with open(user_json_file, 'w') as outfile:
            for t in self.tweets_repo_array:
                outfile.write(json.dumps(t._json))
                outfile.write('\n')
        return user_json_file
