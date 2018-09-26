import sys, os
import csv
import json
import codecs
import requests
from requests.exceptions import ConnectionError

outpath = os.getcwd()
directory = os.getcwd()

def main():
    data = []
    ###iterate on all json files in working directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
        # print(os.path.join(directory, filename))
            try:
                print 'processing file ' + filename
                json_file = open(filename,"r")
            except:
                print 'fail to open file ' + filename

        data.extend(jsfile_parser(json_file))

    colnames = ['tweet_id', 'user_id', 'user_link', 'user_join', 'user_description', 'user_website','user_followings', 'user_followers', 'user_favorites', 'user_lists', 'user_statuses', 'user_timezone', 'user_verified', 'user_utcoffset', 'user_name', 'user_language', 'user_location', 'tweet_action', 'tweet_timestamp', 'tweet_client', 'tweet_link', 'tweet_text', 'tweet_favorites', 'tweet_location', 'tweet_geo', 'tweet_retweets', 'tweet_hash', 'tweet_symbol', 'tweet_mention_names', 'tweet_mention_ids','tweet_obj', 'st_shorturl', 'st_longurl', 'klout']

    with open(outpath+'\\tweets.csv', 'wb') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=colnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

def jsfile_parser(file):
    tweet_list = []
    line = file.readline()
        # print line
    i = 0
    while(line):
        ###avoid blank lines
        if len(line)>10:
            #print 'len(line)=%s', len(line)
            line = line.decode('utf-8')
            #print 'type(line): ', type(line)
            js_object = json.loads(line)
            ###test not reaching the summary line
            if 'info' not in js_object.keys():
                ###record how many tweets have been found in current file
                i += 1
                # print 'activity ', i
                ###create a dictionary to contain the tweet information
                tweet_dict = tweet_extractor(js_object)
                tweet_list.append(tweet_dict)
            else:
                if (js_object['info']['activity_count']!=i):
                    print 'tweets number '+str(i)+' doesn\'t match the summary line'
                else:
                    print str(i)+' tweets'
        line = file.readline()
    return tweet_list


def tweet_extractor(js_obj):
    tweet = {}
    ###get all fields needed
    try:
        tweet['tweet_id'] = int(js_obj['id'].split(':')[2])
        ###user profile
        tweet['user_id'] = int(js_obj['actor']['id'].split(':')[2])
        tweet['user_link'] = js_obj['actor']['link']
        tweet['user_join'] = js_obj['actor']['postedTime']
        tweet['user_description'] = js_obj['actor']['summary']
        if tweet['user_description'] != None:
            tweet['user_description'] = tweet['user_description'].replace('\n', ' ').replace('\r', ' ').encode('utf-8')
        # print 'type(user_description):', type(tweet['user_description'])
        tweet['user_website'] = js_obj['actor']['links'][0]['href']
        if tweet['user_website'] != None:
            tweet['user_website'] = tweet['user_website'].replace('\n', ' ').replace('\r', ' ').encode('utf-8')
        tweet['user_followings'] = int(js_obj['actor']['friendsCount'])
        tweet['user_followers'] = int(js_obj['actor']['followersCount'])
        # tweet['user_favorites'] = int(js_obj['actor']['favoritesCount']) no favoritesCount
        tweet['user_lists'] = int(js_obj['actor']['listedCount'])
        tweet['user_statuses'] = int(js_obj['actor']['statusesCount'])
        tweet['user_timezone'] = js_obj['actor']['twitterTimeZone']
        tweet['user_verified'] = js_obj['actor']['verified']
        tweet['user_utcoffset'] = js_obj['actor']['utcOffset']
        tweet['user_name'] = js_obj['actor']['preferredUsername'].encode('utf-8')
        tweet['user_language'] = ','.join(item for item in js_obj['actor']['languages'])
        if 'location' in js_obj['actor'].keys():
            tweet['user_location'] = js_obj['actor']['location']['displayName'].encode('utf-8')
        else:
            tweet['user_location'] = ''

        tweet['tweet_action'] = js_obj['verb']
        tweet['tweet_timestamp'] = js_obj['postedTime']
        tweet['tweet_client'] = js_obj['generator']['displayName'].encode('utf-8')
        tweet['tweet_link'] = js_obj['link']
        tweet['tweet_text'] = js_obj['body'].replace('\n', ' ').replace('\r', ' ').encode('utf-8')
        # tweet['tweet_favorites'] = int(js_obj['favoritesCount']) no favoritesCount
        if 'location' in js_obj.keys():
            tweet['tweet_location'] = js_obj['location']['displayName'].encode('utf-8')
        else:
            tweet['tweet_location'] = ''
        if 'geo' in js_obj.keys():
            tweet['tweet_geo'] = js_obj['geo']['coordinates']
        else:
            tweet['tweet_geo'] = ''
        if js_obj['retweetCount'] != None:
            tweet['tweet_retweets'] = int(js_obj['retweetCount'])
        else:
            tweet['tweet_retweets'] = 'None'
        tweet['tweet_hash'] = ','.join(item['text'] for item in js_obj['twitter_entities']['hashtags']).encode('utf-8')
        # tweet['tweet_symbol'] = ','.join(item['text'] for item in js_obj['twitter_entities']['symbols']).encode('utf-8') no symbols
        tweet['tweet_mention_names'] = ','.join(item['screen_name'] for item in js_obj['twitter_entities']['user_mentions'])
        tweet['tweet_mention_ids'] = ','.join(str(item['id']) for item in js_obj['twitter_entities']['user_mentions'])
        tweet['tweet_obj'] = int(js_obj['object']['id'].split(':')[2])

        tweet['st_shorturl'] = ','.join(item['url'] for item in js_obj['twitter_entities']['urls'])
        # print js_obj['twitter_entities']['urls']
        expanded_urls = []
        longurl = []
        for item in js_obj['twitter_entities']['urls']:
            print item
            if 'expanded_url' in item.keys():
                expanded_urls.append(item['expanded_url'])
                short_url = str(item['url'])
                try:
                    site = requests.get(short_url)
                    long_url = site.url
                    longurl.append(long_url)
                    print short_url
                    print long_url
                except ConnectionError as e:
                    print e
                    long_url = "No response"
                    longurl.append(long_url)
        if not None in expanded_urls:
            tweet['st_longurl'] = ','.join(item for item in expanded_urls)
            tweet['new_longurl'] = ','.join(item for item in longurl)
        if 'klout_score' in js_obj['gnip'].keys(): #no klout_score
           tweet['klout'] = int(js_obj['gnip']['klout_score'])
        else:
           tweet['klout'] = ''

    except IOError, e:
        print "error encountered" + e

    return tweet


if __name__ == '__main__':
    main()
