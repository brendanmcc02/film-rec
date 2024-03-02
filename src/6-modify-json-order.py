# 5-filter-over-10k-votes.json => 6-modified-order.json
# change the order of the json attributes
import json


def main():
    # import 5-over-10k-votes.json as a dictionary
    over10kData = open('../data/5-over-10k-votes.json')
    over10kDataDict = json.load(over10kData)

    # for each film:
    length = len(over10kDataDict)
    i = 0
    while i < length:
        # change the order of the json attributes
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
    with open('../data/6-modified-order.json', 'w') as convert_file:
        convert_file.write(json.dumps(over10kDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()
