## TODO

### Ideas

1. one hot encoding for directors? or some sort of way to recommend films from directors that you like but haven't seen. (can't really do this because all-film-data doesn't have directors)
2. add a feature for a user to search films and input that as their 'user profile': to accommodate for people who don't have an IMDB account
3. add letterboxd integration?
4. wildcard, some way to introduce novel films instead of just the same type. Users don't always watch the same type, they also want variety 

### General
- [x] switch from my-film-data.json to ratings.csv
- [x] add numVotes & runtime to human data
- [x] vectorize numberOfVotes & runtime
- [x] change run.sh to reflect various changes
- [x] error handling for imported ratings.csv
- [x] delete title.x.tsv files after getting all-film-data.json
- [x] don't normalise myRating
- [x] don't fix imdbRating to 1.0
- [x] instead of writing all-film-data-vec, my-film-data, etc. to file, create global variables in app.py, and then create endpoints for getters/setters
- [ ] rename variables & func from lowerCamelCase to underscore
- [ ] change variables that are not constant from UPPER_CASE to underscore case

### Backend
- [x] all-film-data doesn't filter out films that have been rated
- [x] vectorize all-film-data in init-all-film-data.py
- [x] init-my-film-data filters out films that have been rated from all-film-data (also rm vector entries)
- [x] keep title.basics.tsv & title.ratings.tsv
- [x] add last-download.txt. if downloaded <24 hours, skip the step
- [x] finish init-my-file-data.py to reflect above changes
- [x] research how/where to store files, run .py scripts etc.
- [x] upload button calls /verifyFile API
- [x] upload error handling
- [x] change return type of recs function
- [x] init_rec writes all-film-data.json (w/o user rated films), my-film-data.json, all-film-data-vec.json, my-film-data-vec.json to file
- [x] call init_rec endpoint once when new page is loaded
- [x] thumbs up/down state logic
- [x] vector change in thumbs up/down
- [x] revert vector change
- [x] regen function
- [ ] wildcard recs

### Frontend
- [x] do text div 
- [x] do file upload (visuals only) div
- [x] href what is rating.csv/how to export it
- [x] finish home page (visuals only, file upload func later)
- [x] re-do text element showing selected files, errors, etc. (lost changes rip)
- [x] manage multiple pages (check sweng project)
- [x] go to results page if verifyFile ok
- [x] verify api calls for vector change funcs are working
- [x] /initial_recs api calls more than once?
- [ ] make results page look presentable/nice

### Windows
- [x] config frontend: npm, etc.
- [x] run flask app
- [ ] finish converting init-all-film-data.sh to .bat

### Scripts
- [x] merge the 3 .sh files into one, consider renaming it as vectorizing can be included into it
- [x] reduce run.sh to startup.sh

### Vectorizing the data
- [x] normalise years
- [x] normalise imdbRating
- [x] one-hot encoding for genres
- [x] vectorize all-film-data
- [x] verify vectorizing was done correctly
- [x] vectorize my-film-data
- [x] how to weight myRating - currently doing scalar multiplication
- [x] how much do I round values by? - not rounding values, no reason to do it
- [x] calculate user profile using weighted averages
- [x] mess around with weights of year and genres

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
