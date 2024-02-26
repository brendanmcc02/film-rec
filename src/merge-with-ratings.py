# given over-60-min-basics.json, merge this dataset with title.ratings.tsv

import pandas as pd
import json


def main():
    # import title-ratings.tsv
    ratings_df = pd.read_csv('../data/imdb-data/title.ratings.tsv', sep='\t', dtype=str)
    ratings = ratings_df.to_dict('records')
    # import over-60-min-basics.json
    over60Data = open('../data/over-60-min-basics.json')
    over60DataDict = json.load(over60Data)

    length_ratings = len(ratings)
    length_over60 = len(over60DataDict)

    # iterate through each film in over-60-min-basics.json:
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
            except ValueError:
                del ratings[j]
                length_ratings = length_ratings - 1
                break

        # if the film is not found in title-ratings.tsv
        if not found:
            del over60DataDict[i]
            i = i - 1
            length_over60 = length_over60 - 1

        i = i + 1

    # write to file
    with open('../data/merged.json', 'w') as convert_file:
        convert_file.write(json.dumps(over60DataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()
