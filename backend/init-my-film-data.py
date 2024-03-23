# given ratings.csv, filter it, and then write to my-film-data.json
import json
import csv


def main():
    # import ratings.csv
    myFilmData_list = []
    with open("../data/ratings.csv", 'r', encoding='utf-8', newline='') as myFilmData_file:
        reader = csv.DictReader(myFilmData_file, delimiter=',')
        for row in reader:
            myFilmData_list.append(dict(row))

    myFilmDataDict = {}  # create dict

    # for each film:
    for film in myFilmData_list:
        # filter out non-movies, <40 min runtime, and with no genres
        if film['Title Type'] == "movie" and int(film['Runtime (mins)']) >= 40 and film['Genres'] != "":
            # convert genres to array
            genres = film['Genres'].replace("\"", "").split(", ")
            # map the film id to a dict of it's attributes
            try:
                myFilmDataDict[film['Const']] = {
                    "title": film['Title'],
                    "year": int(film['Year']),
                    "myRating": int(film['Your Rating']),
                    "imdbRating": float(film['IMDb Rating']),
                    "numberOfVotes": int(film['Num Votes']),
                    "runtime": int(film['Runtime (mins)']),
                    "genres": genres
                }
            except ValueError:
                print("value error with film: " + film['Const'])

    # write to file
    with open('../data/my-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(myFilmDataDict, indent='\t', separators=(',', ': ')))


if __name__ == "__main__":
    main()
