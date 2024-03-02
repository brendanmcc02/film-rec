# 3-over-60-min.json => 4-merge-with-ratings.json
# merge 3-over-60-min.json with title.ratings.tsv

import pandas as pd
import json


def main():
    # import title-ratings.tsv as dataframe
    ratings_df = pd.read_csv('../data/imdb-data/title.ratings.tsv', sep='\t', dtype=str)
    ratings = ratings_df.to_dict('records')
    # import 3-over-60-min.json as dictionary
    over60Data = open('../data/3-over-60-min.json')
    over60DataDict = json.load(over60Data)

    # get the length of the datasets
    length_ratings = len(ratings)
    length_over60 = len(over60DataDict)

    # the films are sorted by id:
    # i.e. tt000010 will always come after tt000009.
    # so, when the corresponding film is found in title-ratings.tsv,
    # I modify a 'start' variable, so when the code needs to look for
    # the next corresponding film, it starts looking where it left off.
    # this is more efficient.

    # iterate through each film in 3-over-60-min.json:
    i = 0
    start = 0
    while i < length_over60:
        if i % 500 == 0:
            print(str(i) + "/" + str(length_over60))

        filmId = over60DataDict[i]['id']
        found = False
        # find the corresponding film in title-ratings.tsv
        for j in range(start, length_ratings):
            found = False
            try:
                if ratings[j]['tconst'] == filmId:
                    # add imdbRating & numberOfVotes
                    over60DataDict[i]['imdbRating'] = float(ratings[j]['averageRating'])
                    over60DataDict[i]['numberOfVotes'] = int(ratings[j]['numVotes'])
                    start = j + 1
                    found = True
                    break
            # some films may not have 'numVotes' or 'averageRating' attributes
            except ValueError:
                # delete the film
                del ratings[j]
                length_ratings = length_ratings - 1
                break

        # if the film is not found in title-ratings.tsv
        if not found:
            # delete the film
            del over60DataDict[i]
            i = i - 1
            length_over60 = length_over60 - 1

        i = i + 1

    # write to file
    with open('../data/4-merge-with-ratings.json', 'w') as convert_file:
        convert_file.write(json.dumps(over60DataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()
