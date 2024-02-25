import json


def main():
    # import all-films-data.json to a variable
    filmData = open('../data/all-film-data.json')
    filmDictionary = json.load(filmData)

    # for each film:
    for film in filmDictionary:
        # *** DO NOT DELETE numberOfVotes; VERY IMPORTANT IF I WANT TO FILTER
        # DATABASE IN FUTURE
        pass

    # write to file
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(filmDictionary, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

