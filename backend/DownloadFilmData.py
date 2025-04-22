# downloads the publicly available imdb datasets.
# this is intended to be run using `init-all-film-data.sh`, not as a standalone file.

import urllib.request
from datetime import datetime, timedelta

class DownloadFilmData:

    MIN_HOURS_UNTIL_LAST_DOWNLOAD = 12

    def main(self):
        lastImdbDownloadString = open('../database/LastImdbDownloadTimestamp.txt', 'r').read()
        lastImdbDownloadTimestamp = datetime.strptime(lastImdbDownloadString, '%Y-%m-%d %H:%M:%S.%f')
        currentTimestamp = datetime.now()

        differenceInTimestamps = currentTimestamp - lastImdbDownloadTimestamp

        if differenceInTimestamps >= timedelta(hours=self.MIN_HOURS_UNTIL_LAST_DOWNLOAD):
            urllib.request.urlretrieve("https://datasets.imdbws.com/title.basics.tsv.gz", 
                                       "../database/title.basics.tsv.gz")
            urllib.request.urlretrieve("https://datasets.imdbws.com/title.ratings.tsv.gz", 
                                       "../database/title.ratings.tsv.gz")

            with open('../database/LastImdbDownloadTimestamp.txt', 'w') as file:
                file.write(str(datetime.now()))


if __name__ == "__main__":
    downloadFilmData = DownloadFilmData()
    downloadFilmData.main()
