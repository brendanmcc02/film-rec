## TODO

### Scripts
- [x] merge the 3 .sh files into one, consider renaming it as vectorizing can be included into it

### Creating user profile
- [x] calculate user profile using weighted averages
- [x] mess around with weights of year and genres

### Vectorizing the data
- [x] normalise years
- [x] normalise imdbRating
- [x] one-hot encoding for genres
- [x] vectorize all-film-data
- [x] verify vectorizing was done correctly
- [x] vectorize my-film-data
- [x] how to weight myRating - currently doing scalar multiplication
- [x] how much do I round values by? - not rounding values, no reason to do it

### Initialising the Database
- [x] get rid of non-movies, rename attributes, convert genres to array, delete unnecessary attributes (basics.tsv)
- [x] get rid of < 1930 films (basics.tsv), delete films with genres = '\\N'
- [x] get rid of films with <60 min runtime
- [x] merge/match up the two datasets
- [x] get rid of films with < 10,000 votes
- [x] change the order of .json attributes
- [x] filter out films that I have rated
- [x] find out efficient way to work with .tsv files
- [x] filter my-film-data to match all-film-data
- [x] combine stages 1-3 into stage 1
- [x] think about combining other stages/making the incremental filtering process more efficient
- [x] create hashmap for stage 4 (instead of linear searching)
- [x] verify data is correct
- [x] init all-film-data.py
- [x] for .sh files change paths to be relative to device
- [x] add title attribute to dataset
- [x] change data structure from list of dicts => dict of dicts (key: filmID, value: dict(film))
