import json
import pandas as pd


def main():
    # import only-movies.json
    onlyMoviesData = open('../data/only-movies-basics.json')
    onlyMoviesDataDict = json.load(onlyMoviesData)
    # import title.basics.tsv
    basics_df = pd.read_csv('../data/imdb-data/title.basics.tsv', sep='\t', dtype=str)
    basics = basics_df.to_dict('records')

    # films in both datasets are sorted by film ID (e.g. tt0468569, tt0468570, ...)
    # so when searching for corresponding film ID's, there is no need to start searching
    # basics.tsv from the beginning, when we know that the last film ID was found at index
    # 500 for example. that's the logic behind the 'start' variable in the for loop.

    # for each film
    start = 0
    length = len(basics)
    str_length = str(length)
    for film in onlyMoviesDataDict:
        filmId = film['id']
        # find the corresponding film in basics.tsv
        for i in range(start, length):
            if filmId == basics[i]['tconst']:
                start = i + 1  # update start variable for next iteration in for loop
                try:
                    # add the runtime attribute
                    film['runtime'] = int(basics[i]['runtimeMinutes'])
                    print(str(i) + "/" + str_length)
                    break
                except ValueError:
                    film['runtime'] = -1

    # write to file
    with open('../data/only-movies-runtime-basics.json', 'w') as convert_file:
        convert_file.write(json.dumps(basics, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

