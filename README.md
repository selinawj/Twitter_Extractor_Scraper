# Twitter_Extractor_Scraper
The 26 gb Twitter data can be downloaded from [here](http://an.kaist.ac.kr/~haewoon/release/twitter_social_graph/twitter_rv.zip).
Python programs to process the Twitter data:
1. Parse JSON Tweets to individual columns from several JSON files in a directory
2. Expand short urls to a full link
2. Extract each Twitter user ID's follower IDs from a large CSV database file
3. Scrape Twitter user ID's follower IDs from Twitter API

## What's Included
Parse JSON Tweets: tweets_reader.py
Expand short urls: parse_url.py
Extract user ID's follower IDs: extract_twitter_followers.py
Keep track of extraction row num: extract_check_row_num.py
Scrape Twitter follower IDs: scrape_twitter_followers.py

## Built With
* [Python](https://www.python.org/) - All Preprocessing Scripts.
* [Requests: HTTP for Humans](http://docs.python-requests.org/en/master/) - Requests Library in Python for sending HTTP requests and expand short URLs.
* [Numpy.genfromtxt](https://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html) - Used to load a data file.
* [Itertools](https://docs.python.org/2/library/itertools.html) - A Python module used to slice and extract a portion of data from a large file.
* [Tweepy](http://docs.tweepy.org/en/v3.5.0/) - A Python library for accessing the Twitter API.
* [Pandas](https://pandas.pydata.org/) - Used this library for manipulating and storing the resulting data in a dataframe structure.

## Authors

* **Selina Wong** - [SelinaWJ](https://github.com/SelinaWJ)

