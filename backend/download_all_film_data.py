# this is intended to be run using `init-all-film-data.sh`, not as a standalone file

import urllib.error
import urllib.request
from datetime import datetime, timedelta


def main():
    try:
        lastDownload_str = open('../database/last-imdb-download-timestamp.txt', 'r').read()
    except FileNotFoundError:
        print("Error. last-imdb-download-timestamp.txt not found.")
        raise FileNotFoundError
    except Exception as e:
        print(f"Error: {e}")
        raise e

    lastImdbDownloadTimestamp = datetime.strptime(lastDownload_str, '%Y-%m-%d %H:%M:%S.%f')
    currentTimestamp = datetime.now()

    differenceInTimestamps = currentTimestamp - lastImdbDownloadTimestamp

    # if the file was downloaded >= 1 days ago: (I really don't want to get blacklisted)
    if differenceInTimestamps >= timedelta(days=1):
        try:
            urllib.request.urlretrieve("https://datasets.imdbws.com/title.basics.tsv.gz", "../database/title.basics.tsv.gz")
        except urllib.error.URLError:
            print("Error. URL not found. It may be outdated.")
            raise urllib.error.URLError
        except FileNotFoundError:
            print("File Not found. Check save directory of URL request is correct.")
            raise FileNotFoundError
        except Exception as e:
            print("Error: {e}")
            raise e
        
        try:
            urllib.request.urlretrieve("https://datasets.imdbws.com/title.ratings.tsv.gz",
                                    "../database/title.ratings.tsv.gz")
        except urllib.error.URLError:
            print("Error. URL not found. It may be outdated.")
        except FileNotFoundError:
            print("File Not found. Check save directory of URL request is correct.")
        except Exception as e:
            print("Error: {e}")
            raise e

        try:
            with open('../database/last-imdb-download-timestamp.txt', 'w') as file:
                file.write(str(datetime.now()))
        except FileNotFoundError:
            print("File Not Found Error. Check directory of file-write is ok.")
            raise FileNotFoundError
        except Exception as e:
            print("Error: {e}")
            raise e


if __name__ == "__main__":
    main()
