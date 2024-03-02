import json


def main():
    over10kData = open('../data/5-over-10k-votes.json')
    over10kDataDict = json.load(over10kData)

    # for each film:
    length = len(over10kDataDict)
    i = 0
    while i < length:
        over10kDataDict[i] = {
            'id': over10kDataDict[i]['id'],
            'year': over10kDataDict[i]['year'],
            'imdbRating': over10kDataDict[i]['imdbRating'],
            'genres': over10kDataDict[i]['genres'],
            'numberOfVotes': over10kDataDict[i]['numberOfVotes'],
            'runtime': over10kDataDict[i]['runtime']
        }

        i = i + 1

    # write to file
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(over10kDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()
