import tweepy
import json
import math
from tweepy import TweepError
from time import sleep

with open('api_keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
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
#
# print("All done.")
# with open('everything.json', 'w') as outfile:
#     json.dump(all_data, outfile)
