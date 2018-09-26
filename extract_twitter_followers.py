import pandas as pd
import csv
from numpy import genfromtxt
import itertools

#create dictionary to store userIDs without running the userIDs repeatedly
def createDict():
    #change this manually
    start, end = 0,
    dictionaryArray = []
    userDict = {}
    #initialize dictionary array
    with open("twitter_RV.csv", 'rt') as f:
        data = csv.reader(f)
        for line in itertools.islice(data, start, end):
            new = ''.join(line)
            userID = new.split()[0]
            print userID #track current database userID
            followerID = new.split()[1]
            if any(userID in d for d in dictionaryArray): #if key is in array, update
                userDict[userID].append(followerID)
            else: #if key is not in array, create new dictionary
                userDict[userID] = [followerID]
                dictionaryArray.append(userDict)
        match(dictionaryArray)

#generate userID match from NYT userID csv file
def match(myArray):
   #get each individual's user ID
    #read batch1 file
    j=0
    my_data = genfromtxt('NYT_tweets_users.csv')
    while j < len(my_data):
        print "line num: " + str(j) #keep track of line num
        tempID = str(int(my_data[j]))
        print "processing userID: " + tempID
        if any(tempID in e for e in myArray): #if tempID matches key in dict
            ids = userDict[tempID]
            print ids
            #initialize array with user's ID
            myID = [tempID] * (len(ids))
            #write to csv
            df = pd.DataFrame({"followerID": ids, "userID" : myID})
            df.to_csv(tempID+'\\followers.csv', index = False, columns = ["userID", "followerID"])
            j+=1
        else:
            j+=1

createDict()
