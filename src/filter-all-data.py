import pandas as pd
import json


# 1. import title-ratings.tsv & title-basics.tsv
# 2. combine both datasets together
# 3. keep films that:
#       a. have 'movie' as titleType
#       b. <10000 numVotes
# 4. delete:
#       a. numVotes
#       b. primaryTitle
#       c. originalTitle
#       d. isAdult
#       e. endYear
#       f. runtimeMinutes
#       g. titleType
# 5. rename startYear => year
def main():
    basics_df = pd.read_csv('../data/imdb-data/title.basics-sample.tsv', sep='\t', dtype=str)
    basics = basics_df.to_dict('records')
    ratings_df = pd.read_csv('../data/imdb-data/title.ratings-sample.tsv', sep='\t', dtype=str)
    ratings = ratings_df.to_dict('records')

    length = len(basics)
    # todo print(i) so i know how long it takes
    # todo sample doesn't work for some reason (check output, numVotes & rating doesn't match title
    # this was running for 2hrs15mins and still not done so idk
    i = 0
    while i < length:
        basics[i]['imdbRating'] = float(ratings[i]['averageRating'])
        basics[i]['numberOfVotes'] = int(ratings[i]['numVotes'])

        # todo was 1000 but i increased it due to the amount of films
        if basics[i]['titleType'] != 'movie' or basics[i]['numberOfVotes'] < 1000:
            del basics[i]
            i = i - 1
            length = length - 1
        else:
            del basics[i]['titleType']
            del basics[i]['primaryTitle']
            # del basics[i]['originalTitle']
            del basics[i]['isAdult']
            del basics[i]['endYear']
            del basics[i]['runtimeMinutes']
            basics[i]['year'] = basics[i]['startYear']
            del basics[i]['startYear']
            # del basics[i]['numberOfVotes']

        i = i + 1

    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(basics, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    main()

