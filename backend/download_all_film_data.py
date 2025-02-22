# this is intended to be run using `init-all-film-data.sh`, not as a standalone file

import urllib.error
import urllib.request
from datetime import datetime, timedelta


def main():
    lastDownloadString = open('../database/last-imdb-download-timestamp.txt', 'r').read()
    lastImdbDownloadTimestamp = datetime.strptime(lastDownloadString, '%Y-%m-%d %H:%M:%S.%f')
    currentTimestamp = datetime.now()

    differenceInTimestamps = currentTimestamp - lastImdbDownloadTimestamp

    # if the file was downloaded >= 1 days ago: (I really don't want to get blacklisted)
    if differenceInTimestamps >= timedelta(days=1):
        urllib.request.urlretrieve("https://datasets.imdbws.com/title.basics.tsv.gz", 
                                   "../database/title.basics.tsv.gz")
        urllib.request.urlretrieve("https://datasets.imdbws.com/title.ratings.tsv.gz", 
                                   "../database/title.ratings.tsv.gz")

        with open('../database/last-imdb-download-timestamp.txt', 'w') as file:
            file.write(str(datetime.now()))


if __name__ == "__main__":
    main()
