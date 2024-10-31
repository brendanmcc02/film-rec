# TODO

## New TODO List
- [x] create myFilmData from imported diary.csv through Flask (letterboxd)
- [x] integrate date rated - weight of how recently user has rated film.
- [x] tidy up code, make things as efficient as possible
- [x] fix windows upload diary.csv error
- [x] cache cosine sim comparisons
- [x] double check I didn't remove any necessary `global`s and fuck it up
- [x] deletion of ratings/diary.csv before saving to file
- [x] recent profile vector (last 30 days)
- [x] letterboxd search can be much more efficient 
- [x] work with np vector instead of list? is it more efficient?
- [x] ensure that a user can go back to home page and upload new file and recs still work smoothly
- [ ] letterboxd conversion: rather than relying on diary.csv, append latest `Watched Date` to corresponding entry in
`ratings.csv`. not all films rated on letterboxd account are in diary.csv, but all are in ratings.csv
- [ ] augment extra data? directors, country, language, etc.
- [ ] figure out how to diversify recs
- [ ] reduce comments in code and make it more readable (after watching code aesthetic's video)

## Data Retrieval
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

## General
- [x] switch from my-film-data.json to ratings.csv
- [x] add numVotes & runtime to human data
- [x] vectorize numberOfVotes & runtime
- [x] change run.sh to reflect various changes
- [x] error handling for imported ratings.csv
- [x] delete title.x.tsv files after getting all-film-data.json
- [x] don't normalise myRating
- [x] don't fix imdbRating to 1.0
- [x] instead of writing all-film-data-vec, my-film-data, etc. to file, create global variables in app.py, and then 
create endpoints for getters/setters
- [ ] drop numVotes threshold to 10k?

## Backend
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
- [x] init_rec writes all-film-data.json (w/o user rated films), my-film-data.json, all-film-data-vec.json, 
my-film-data-vec.json to file
- [x] call init_rec endpoint once when new page is loaded
- [x] thumbs up/down state logic
- [x] vector change in thumbs up/down
- [x] revert vector change
- [x] regen function
- [x] wildcard recs
- [x] everytime you change a vector (wildcard/user profile), ensure all values >=0.0 && <= 1.0
- [x] fix runtime vector wildcard
- [x] implement wildcard feedback factor
- [x] implement profileChanges instead of separate wildcardProfileChanges & userProfileChanges

## Frontend
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

## Tidying up code
- [x] go through all code removing redundancy, fine-tuning
- [x] rename variables & func to lowerCamelCase
- [x] change variables that are not constant from UPPER_CASE to underscore case
- [x] minimise global variables (you only need to call global if you want to **modify** the variable)
- [ ] error handling on potential div by 0 errors

## Windows
- [x] config frontend: npm, etc.
- [x] run flask app
- [ ] ~~finish converting init-all-film-data.sh to .bat~~

## Scripts
- [x] merge the 3 .sh files into one, consider renaming it as vectorizing can be included into it
- [x] reduce run.sh to startup.sh

## Data Processing
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
