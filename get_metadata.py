import tweepy
import json
import math
from tweepy import TweepError
from time import sleep

consumer_key = '98ribFB1JnMr7gHAd2AtawSLh'
consumer_secret = '4Vd5dkZp2PiEZrYenwVyORtc9iGYBLtg7k9TqPVJFjADPurf3K'
access_token = '773554088210534400-VsxhGK6ACMU3v0nvWhlWfzYbtJ8kgtV'
access_token_secret = '2oaaMiY1FWpYiHNICvMhqOP1umXpLx0nGMziwy0cFquav'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

with open('all_ids.json') as f:
    ids = json.load(f)

print('Total ids: {}'.format(len(ids)))

all_data = []
start = 0
end = 100
limit = len(ids)
i = math.ceil(limit / 100)

for go in range(i):
    print('Currently getting {} - {}'.format(start, end))
    sleep(6)  # needed to prevent hitting API rate limit
    id_batch = ids[start:end]
    start += 100
    end += 100
    tweets = api.statuses_lookup(id_batch)
    for tweet in tweets:
        all_data.append(dict(tweet._json))

print("All done.")
with open('everything.json', 'w') as outfile:
    json.dump(all_data, outfile)
