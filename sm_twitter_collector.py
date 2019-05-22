from sm_settings import SMSettings
import tweepy  # https://github.com/tweepy/tweepy
import os,sys,inspect
import pathlib
import simplejson as json
import helpers.tweet_cleaner as tweet_cleaner
import csv

class SMTwitterCollector:
    twitter_api = None
    tweets_repo_array = []
    tweets_replys_array = []

    def __init__(self, screen_name):
        auth = tweepy.OAuthHandler(SMSettings.twitter_app_settings['consumer_key'], SMSettings.twitter_app_settings['consumer_secret'])
        auth.set_access_token(SMSettings.twitter_app_settings['access_token'], SMSettings.twitter_app_settings['access_secret'])
        self.twitter_api = tweepy.API(auth)
        self.currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.screen_name = screen_name
        self.user_data_folder_path =  SMSettings.paths['dataForClassifications'].format(self.screen_name)


    def _check_data_collected_before(self, max_id):
        saved_tweets_files = os.listdir(self.user_data_folder_path)
        for saved_tweets_file in saved_tweets_files:
            splited_file_name = saved_tweets_file.split("_")
            if(str(max_id) == str(splited_file_name[1])):
                return True, saved_tweets_file
        return False, None

    def _clean_tweet_text(self, tweet):
        clean_text = tweet_cleaner.clean_tweet(tweet)
        clean_text = tweet_cleaner.normalize_arabic(clean_text)
        clean_text = tweet_cleaner.remove_repeating_char(clean_text)
        clean_text = tweet_cleaner.keep_only_arabic(clean_text.split())
        return clean_text

    def process_tweets_json_to_csv(self, max_id):
        (collected_before, user_json_file) = self._check_data_collected_before(max_id)
        if(not collected_before):
            return (False, None)

        user_json_file = self.user_data_folder_path+user_json_file

        data_classifications_csv = open(self.user_data_folder_path+self.screen_name+"_"+str(max_id)+".csv", encoding='utf-8', mode='w')

        writer_data_classifications_csv_file = csv.writer(data_classifications_csv)
        csv_data = []
        csv_data.append(["text"])
        with open(user_json_file) as json_reader:
            lines = json_reader.readlines()
            for line in lines:
                json_tweet = json.loads(line)
                text = json_tweet['text']
                clean_text = self._clean_tweet_text(text)
                csv_data.append([clean_text])
            writer_data_classifications_csv_file.writerows(csv_data)
            data_classifications_csv.close()
        return True, data_classifications_csv

    def get_user_tweets(self, limit=1):
        collected_before = False

        for tweet in tweepy.Cursor(self.twitter_api.user_timeline, screen_name=self.screen_name).items(limit):
            max_tweet_id = tweet.id

        if not os.path.exists(self.user_data_folder_path):
            pathlib.Path(self.user_data_folder_path).mkdir(parents=True, exist_ok=True)
        else:
            (collected_before, user_json_file) = self._check_data_collected_before(max_tweet_id)
        if(collected_before):
            return max_tweet_id, user_json_file

        for tweet in tweepy.Cursor(self.twitter_api.user_timeline, screen_name=self.screen_name).items(limit):
            self.tweets_repo_array.append(tweet)
            for tweet_reply in tweepy.Cursor(self.twitter_api.search,q='to:'+self.screen_name, since_id=tweet.id, result_type='recent',timeout=999999).items():
                if hasattr(tweet_reply, 'in_reply_to_status_id_str'):
                    if (tweet_reply.in_reply_to_status_id_str==tweet.id_str):
                        self.tweets_replys_array.append(tweet_reply)


        min_id = self.tweets_repo_array[1].id
        max_id = self.tweets_repo_array[-1].id

        tweets_repo_file_path = self.screen_name + "_" + str(max_id) + "_" + str(min_id)
        user_json_file = self.user_data_folder_path+'{}.json'.format(tweets_repo_file_path)
        user_replys_json_file = self.user_data_folder_path+'{}.json'.format(tweets_repo_file_path + "_replys")

        with open(user_json_file, 'w') as outfile:
            for t in self.tweets_repo_array:
                outfile.write(json.dumps(t._json))
                outfile.write('\n')
        outfile.close()
        with open(user_replys_json_file, 'w') as outReplyfile:
            for t in self.tweets_replys_array:
                outReplyfile.write(json.dumps(t._json))
                outReplyfile.write('\n')
        outReplyfile.close()
        return max_id, user_json_file
