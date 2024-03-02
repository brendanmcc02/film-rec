# given 4-merge-with-ratings.json, get rid of films with under 10,000 votes
import json


def main():
    # import 4-merge-with-ratings.json
    mergedData = open('../data/5-over-10k-votes.json')
    mergedDataDict = json.load(mergedData)

    print(len(mergedDataDict))


if __name__ == "__main__":
    main()
