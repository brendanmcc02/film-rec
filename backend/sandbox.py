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
        file = open('../database/cached-tmdb-film-data.json')
    except FileNotFoundError:
        print("Check it exists.")
        raise FileNotFoundError
    cachedTmdb = json.load(file)

    for filmID in cachedTmdb:
        cachedTmdb[filmID]['poster'] = cachedTmdb[filmID]['mainPoster']
        del cachedTmdb[filmID]['mainPoster']

    with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
            convert_file.write(json.dumps(cachedTmdb, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    main()

