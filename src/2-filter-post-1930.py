# non-movies were deleted from title.basics and written to a file: 1-only-movies.json
# this script will take that data, and remove films released before 1930, and films with no genres
import json


def main():
    # import 1-only-movies.json
    onlyMoviesData = open('../data/1-only-movies.json')
    onlyMoviesDataDict = json.load(onlyMoviesData)

    # for each film:
    i = 0
    length = len(onlyMoviesDataDict)
    while i < length:
        try:
            # if:
            # 1. film was released before 1930
            # 2. film has no genres
            if onlyMoviesDataDict[i]['year'] < 1930 or onlyMoviesDataDict[i]['genres'][0] == r"\N":
                # delete the film
                del onlyMoviesDataDict[i]
                i = i - 1
                length = length - 1
            # else: keep the film
            else:
                print(str(i) + "/" + str(length))
        except ValueError:
            # for some reason, some entries in 'startYear' are not int types, so this catches the exception and
            # just deletes the film
            del onlyMoviesDataDict[i]
            i = i - 1
            length = length - 1

        i = i + 1

    # write to file
    with open('../data/2-post-1930.json', 'w') as convert_file:
        convert_file.write(json.dumps(onlyMoviesDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

