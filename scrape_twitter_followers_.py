import csv
import time
import tweepy
import pandas as pd

auth = tweepy.OAuthHandler("", "") #get Twitter Developer access tokens from https://apps.twitter.com/
auth.set_access_token("", "")

api = tweepy.API(auth)

users = pd.read_csv("NYT_twitter_scraped.csv")
userID = users['user_id']

def main():
    #get each individual's user ID
    i=2340 #start line num
    done=[] #keep track of done users
    while i <= len(userID)-1:
        print "line num: " + str(i) #keep track of line num
        tempID = str(userID[i])
        print "processing userID: " + tempID #keep track of userID

        try:
            #check if user is protected
            u = api.get_user(tempID)
            if u.protected == False:
                #obtain the no. of followers
                countFollowers = u.followers_count
                print "no. of followers: " + str(countFollowers)
                if countFollowers <= 1000:
                    #obtain followers' IDs
                    ids = []
                    for page in tweepy.Cursor(api.followers_ids, user_id=tempID).pages():
                        ids.extend(page)
                        time.sleep(60)

                    print len(ids)
                    #initialize array with user's ID
                    myID = [tempID] * (len(ids))
                    #write to csv
                    df = pd.DataFrame({"followerID": ids, "userID" : myID})
                    df.to_csv(tempID+'\\followers.csv', index = False, columns = ["userID", "followerID"])
                    done.append(1)
                    i+=1
                else:
                    done.append(0)
                    i+=1
            else: #move on to next user
                done.append(0)
                i+=1
        except tweepy.error.TweepError as t: #The code corresponding to the user not found error
            if t.message[0]['code'] == 50:
                print "User doesn't exist"
                done.append(0)
                i+=1
            elif t.message[0]['code'] == 88: #The code for the rate limit error
                time.sleep(15*60) #Sleep for 15 minutes
                print "Sleeping for 15 min"
                i+=1
            else:
                done.append(0)
                i+=1
        df = pd.DataFrame({"done" : done})
        df.to_csv('doneList.csv', index = False)

main()
