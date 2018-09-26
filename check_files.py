import sys, os
from os import listdir
from os.path import isfile, join

directory = os.getcwd()

###iterate on all json files in working directory
for filename in os.listdir(directory):
    if filename.endswith('followers.csv'):
        print(os.path.join(filename))
