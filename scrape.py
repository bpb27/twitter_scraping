from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime

try:
    with open('../names.json') as data_file:    
        users = json.load(data_file)
except:
    print("A problem occurred when parsing names.json")

userCounter = 0

start = datetime.datetime(2017, 9, 1)  # year, month, day
end = datetime.datetime(2017, 9, 2)  # year, month, day

# only edit these if you're having problems
delay = 1  # time to wait on each page load before reading the page
driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()

days = (end - start).days + 1
id_selector = '.time a.tweet-timestamp'
tweet_selector = 'li.js-stream-item'


def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(user, since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

def getTweets(counter):

    user = users[counter]["twitter"]
    twitter_ids_filename = './output/'+user[1:]+'.json'
    ids = []

    myDate = start
    userTweetCount = 0;
    for day in range(days):
        d1 = format_day(increment_day(myDate, 0))
        d2 = format_day(increment_day(myDate, 1))
        url = form_url(user, d1, d2)
        # print(url)
        # print(d1)
        driver.get(url)
        sleep(delay)


        try:
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment = 10

            while len(found_tweets) >= increment:
                # print('scrolling down to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(delay)
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                increment += 10


            for tweet in found_tweets:
                try:
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    ids.append(id)
                    userTweetCount += 1
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)

        except NoSuchElementException:
            print('no tweets on this day')


        myDate = increment_day(myDate, 1)


    
    print(' {} tweets by {}'.format(userTweetCount, user))

    try:
        with open(twitter_ids_filename) as f:
            all_ids = ids + json.load(f)
            data_to_write = list(set(all_ids))
            print('total tweet count: ', len(data_to_write))
    except FileNotFoundError:
        with open(twitter_ids_filename, 'w') as f:
            all_ids = ids
            data_to_write = list(set(all_ids))
            print('total tweet count: ', len(data_to_write))

    with open(twitter_ids_filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

    counter += 1
    
    if counter < len(users):

        getTweets(counter)

    else:
        driver.close()


    return


# START
getTweets(userCounter)

print('all done here')
