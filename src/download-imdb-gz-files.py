import urllib.request


def main():
    # download title.basics.tsv.gz
    urllib.request.urlretrieve("https://datasets.imdbws.com/title.basics.tsv.gz", "../data/title.basics.tsv.gz")

    # download title.ratings.tsv.gz
    urllib.request.urlretrieve("https://datasets.imdbws.com/title.ratings.tsv.gz", "../data/title.ratings.tsv.gz")


if __name__ == "__main__":
    main()
