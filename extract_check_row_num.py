from numpy import genfromtxt
import itertools
import csv

#change this manually
start, end = 205000000, 205000001 #check with userID correspond to this section
#initialize dictionary array
with open("twitter_RV.csv", 'rt') as f:
    data = csv.reader(f)
    dictionaryArray = []
    userDict = {}
    for line in itertools.islice(data, start, end):
        new = ''.join(line)
        userID = new.split()[0]
        print userID
