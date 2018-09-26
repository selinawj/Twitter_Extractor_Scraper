# Twitter_Extractor_Scraper
The 26 gb Twitter data can be downloaded from [here](http://an.kaist.ac.kr/~haewoon/release/twitter_social_graph/twitter_rv.zip).
Python programs to process the Twitter data:
1. Parse JSON Tweets to individual columns from several JSON files in a directory
2. Expand short urls to a full link
2. Extract each Twitter user ID's follower IDs from a large CSV database file
3. Scrape Twitter user ID's follower IDs from Twitter API

## What's Included
1. Parse JSON Tweets: tweets_reader.py
2. Expand short urls: parse_url.py
3. Extract user ID's follower IDs: extract_twitter_followers.py
4. Keep track of extraction row num: extract_check_row_num.py
5. Scrape Twitter follower IDs: scrape_twitter_followers.py

## Built With
* [Python](https://www.python.org/) - All Preprocessing Scripts.
* [Requests: HTTP for Humans](http://docs.python-requests.org/en/master/) - Requests Library in Python for sending HTTP requests and expand short URLs.
* [Numpy.genfromtxt](https://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html) - Used to load a data file.
* [Itertools](https://docs.python.org/2/library/itertools.html) - A Python module used to slice and extract a portion of data from a large file.
* [Tweepy](http://docs.tweepy.org/en/v3.5.0/) - A Python library for accessing the Twitter API.
* [Pandas](https://pandas.pydata.org/) - Used this library for manipulating and storing the resulting data in a dataframe structure.

## Pre-processing Insights
### Extracted Twitter Users
**Process:** In ascending user ID number, slice and extract follower IDs in chunks from the large data file. The dictionaryArray stores multiple userID dictionaries for faster access & update. Ref: [{userID1: f1, f2, ...}, {userID2: ...}]. If the userID is already in the dictionaryArray, append follower IDs from CSV; if the userID is not in the dictionaryArray, create a new dictionary with userID as the key and append the new dictionary to the array. Once all the data from the CSV has been stored in the dictionaryArray, read in the reference file, lookup userID by rows and loop through to find the corresponding follower IDs.

**Speed:**
The python program ran faster in the beginning few rows of userID (smaller userIDs) most likely because there were fewer userIDs (a smaller network of Twitter users in the beginning of 2009) so it was much faster to retrieve the followers of these userIDs. On the contrary, the program ran very slowly, with userID matched only between large row intervals. FollowerIDs had to be extracted in smaller chunks (by about 1,000,000 interval each time per 15-20 min) as the userIDs at the back of the file were larger and there were more twitter accounts to sieve through (perhaps these twitter accounts also had more followers). For faster file processing, I have split the 26 GB file into 3 individual CSV batches.

**Missing userIDs in the CSV file**
The Twitter_RV.Net file (userIDs sorted in ascending order) only contained twitter users up to July 2009 with the last userID - 61578414. A total of 1,468,365,182 rows of twitter social graph data was run to extract the followerIDs. Some userID data were missing from the Twitter_RV.Net file although their account creation date didn’t differ from those which were extracted. I suspect it might possibly be due to private/deactivated account during the time of scraping in 2009 so the followerIDs of these userIDs were inaccessible.

### Scraped Twitter Users
**Process:** The try statement uses API to get to the user from userID and handles exceptions code 50 (user not found error) and code 88 (rate limit error). If user is not protected, obtain the followers count. The threshold for followers count is set at less than or equal to 1000 before obtaining the user's follower ID. UserIDs with 0 followers, protected, suspended, deactivated accounts or accounts with more than 1000 followers were not scraped. Tracking progress is saved in the doneList CSV after the program has completed running.

## Authors

* **Selina Wong** - [SelinaWJ](https://github.com/SelinaWJ)

