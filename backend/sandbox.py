# # import numpy as np
# # import json
# # from datetime import datetime
# import os
# import glob
# import urllib.error
# import numpy as np
# import requests
# import json
# import time
# import urllib.request





# def main():
#     try:
#         file = open('../database/cached-tmdb-film-data.json')
#     except FileNotFoundError:
#         print("Check it exists.")
#         raise FileNotFoundError
#     cachedTmdb = json.load(file)

#     for filmID in cachedTmdb:
#         if len(cachedTmdb[filmID]['summary']) > 500:
             
#         cachedTmdb[filmID]['sum'] = convertRuntimeToHoursMinutes(allFilmData[imdbFilmId]['runtime'])

#     with open('../database/all-film-data.json', 'w') as convert_file:
#             convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))

# if __name__ == "__main__":
#     main()

