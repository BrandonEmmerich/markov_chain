import private
import sys
import tweepy

def open_twitter_api():
    auth = tweepy.OAuthHandler(private.CONSUMER_KEY, private.CONSUMER_SECRET)
    auth.set_access_token(private.ACCESS_KEY, private.ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

if __name__ == '__main__':
    api = open_twitter_api()
    sentence = sys.stdin.read()
    api.update_status(sentence)
