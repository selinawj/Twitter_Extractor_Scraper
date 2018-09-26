import requests
from requests.exceptions import ConnectionError
import csv
import pandas as pd

def user_parser():
    with open('short_url.csv', 'wb') as urlFile:
        df = pd.read_csv('urls.csv')
        for i in range(0, len(df)):
            print i
            short_url = df.ix[i,0]
            string_url = str(short_url)
            if string_url != "nan":
                try:
                    print short_url
                    site = requests.get(short_url)
                    long_url = site.url
                    output = short_url + "," + long_url
                    urlFile.write(output)
                    urlFile.write('\n')
                except ConnectionError as e:
                    print e
                    long_url = "No response"
                    output = short_url + "," + " "
                    urlFile.write(output)
                    urlFile.write('\n')
            else:
                urlFile.write(" ")
                urlFile.write('\n')

url_parser()
