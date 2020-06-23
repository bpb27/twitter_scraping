from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime
import csv


# edit these three variables
user = 'alferdez'
start = datetime.datetime(2014, 4, 2)  # year, month, day
end = datetime.datetime(2020, 6, 1)  # year, month, day

# only edit these if you're having problems
delay = 4  # time to wait on each page load before reading the page
driver = webdriver.Chrome()  # options are Chrome() Firefox() Safari()


# don't mess with this stuff
twitter_ids_filename = 'all_ids.json'
days = (end - start).days + 1
id_selector = 'article > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o ' \
                 '> div:nth-child(1) > div > div > div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > a'

tweet_selector = 'div > div > div > main > div > div > div > div > div > div > div > div > section > div > div > div > div > div > div > div > div > article'

user = user.lower()
ids = []

def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

for day in range(days):
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(d1, d2)
    print(url)
    print(d1)
    driver.get(url)
    sleep(delay)

    try:
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        increment = 10

        while len(found_tweets) >= increment:
            print('scrolling down to load more tweets')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment += 10

        print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))

        for tweet in found_tweets:
            try:
                id_user = tweet.find_element_by_css_selector(id_selector).get_attribute('href')
                id = [id_user.split('/')[-1] for x in id_user if id_user.split('/')[-3] == user]
                ids.append(id)
                print(id_user)
            except StaleElementReferenceException as e:
                print('lost element reference', tweet)

    except NoSuchElementException:
        print('no tweets on this day')

    start = increment_day(start, 1)

ids = [sublist[:1] for sublist in ids]
json_results = {
    user:{
        'tw_id':ids
    }
}

print(json_results)
try:
    with open(twitter_ids_filename) as f:
        all_ids = json_results
        data_to_write = all_ids
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))
except FileNotFoundError:
    with open(twitter_ids_filename, 'w') as f:
        all_ids = ids
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))

with open(twitter_ids_filename, 'w') as outfile:
    json.dump(data_to_write, outfile)

print(ids)

print('all done here')
driver.close()
