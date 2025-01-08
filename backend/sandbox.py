# import numpy as np
# import json
# from datetime import datetime
import os
import glob
import urllib.error
import numpy as np
import requests
import json
import time
import urllib.request


def main():
    try:
        urllib.request.urlretrieve("https://datasets.imdbws.com/title.basics.tsv.gz", "../dataase/title.basics.tsv.gz")
    except urllib.error.URLError:
        print("Error. URL not found. It may be outdated.")


if __name__ == "__main__":
    main()

