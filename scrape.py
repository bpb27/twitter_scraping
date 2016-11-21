from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime

# Editable Parameters
start = datetime.datetime(2016, 11, 15)  # year, month, day
end = datetime.datetime(2016, 11, 20)  # year, month, day
user = "realdonaldtrump"

# you can also try Chrome() or Firefox()
driver = webdriver.Safari()

tweets = []
id_selector = ".time a.tweet-timestamp"
tweet_selector = "li.js-stream-item"

def wrap_up():
    driver.close()

def form_url(since, until):
    return ''.join([
        'https://twitter.com/search?f=tweets&vertical=default&q=from%3A',
        user,
        '%20since%3A',
        since,
        '%20until%3A',
        until,
        'include%3Aretweets&src=typd'
    ])

def check_for_tweets(increment):
    global tweets
    try:
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        if len(found_tweets) >= increment:
            increment = increment + 10
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolling down and waiting for more to load")
            sleep(4)
            check_for_tweets(increment)
        else:
            tweets = found_tweets
    except NoSuchElementException:
        print("Didn't find shit for this day")
        tweets = []

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def check_page(date):
    if date == end:
        print("We're all done here")
        return wrap_up()
    else:
        r1 = format_day(increment_day(date, 0))
        r2 = format_day(increment_day(date, 1))
        url = form_url(r1, r2)
        print(url)

        print("Checking ", r1)
        sleep(4)
        driver.get(url)
        check_for_tweets(10)
        print("{} tweets found".format(len(tweets)))
        all_data = []

        if not len(tweets):
            check_page(increment_day(date, 1))
        else:
            for tweet in tweets:
                try:
                    id_str = tweet.find_element_by_css_selector(id_selector).get_attribute("href").split('/')[-1]
                    all_data.append(id_str)
                except StaleElementReferenceException as e:
                    print("Lost element reference", tweet)

            with open('all_ids.json') as json_data:
                all_data += json.load(json_data)
                data_to_write = unique_data = list(map(lambda x: json.loads(x), set(map(lambda x: json.dumps(x), all_data))))
                print("Final collection count: {}".format(len(data_to_write)))
            with open('all_ids.json', 'w') as outfile:
                json.dump(data_to_write, outfile)

            check_page(increment_day(date, 1))

check_page(increment_day(start, 0))
