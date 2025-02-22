# Data Retrieval
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
- [x] add title attribute to dataset
- [x] change data structure from list of dicts => dict of dicts (key: filmID, value: dict(film))
- [x] augment letterboxdTitle, countries, languages and poster using TMDB API
- [x] finish running `init-all-film-data.py`
- [x] bug with `tt4330758`, make more bulletproof + better error handling
- [x] `tt4330758` ~~NOT SOLVED HOMIE~~
- [x] some key error with `cacheNormalisedYears`? see below
- [x] `cached-letterboxd-titles.json` does not work, file has been reduced drastically

# Data Cleaning
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
- [x] don't store whole poster image url, just the unique part (can prepend later)
- [x] delete poster attribute in all-film-data.json
- [x] manually create `cached-letterboxd-title-year.json` 
- [x] integrate `cached-letterboxd-title-year.json` func into script
- [x] get rid of `letterboxdYear` attribute
- [x] convert `cached-letterboxd-title-year.json` to `cached-letterboxd-title.json`
- [x] solve the letterboxd title year nonsense
- [x] add baseposterURL to dataset, reduces computation during online phase
- [x] remove `backdropPoster`
- [x] rename `mainPoster` to `filmPoster` or `poster`

# Letterboxd conversion
- [x] letterboxd: ask user to upload `ratings.csv` instead of `diary.csv` and make changes accordingly
- [x] get the tmdb title (aka letterboxd) when making the api and cache that somewhere instead of fucking around with 
preprocessing
- [x] when converting letterboxd to imdb format use the cached-tmdb-film-data.json
- [x] some letterboxd films are still not being captured by the conversion

# Vectorizing the Data
- [x] vectorize all-film-data in init-all-film-data.py
- [x] vector change in thumbs up/down
- [x] revert vector change
- [x] regen function
- [x] wildcard recs
- [x] everytime you change a vector (wildcard/user profile), ensure all values >=0.0 && <= 1.0
- [x] fix runtime vector wildcard
- [x] implement wildcard feedback factor
- [x] implement profileChanges instead of separate wildcardProfileChanges & userProfileChanges
- [x] integrate date rated - weight of how recently user has rated film.
- [x] cache cosine sim comparisons
- [x] one hot encode language & country
- [x] vectorize all-film-data in offline phase
- [x] cache allGenres, allLanguages, allCountries to a json file
- [x] cache & store all-film-data vector magnitudes in offline phase
- [x] recent profile vector (last 30 days)
- [x] add specialised way to calculate vector magnitude (i.e. dont over prioritise multi-genre/lang/country films unfairly)

## Genre Profiles
- [x] create 23 user profiles, modify each of them through iteration of `userFilmData`
- [x] ~~use weighted or normal average?~~ using weighted
- [x] apply `NUM_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD` weight to profile after iteration of `userFilmData`
- [x] pick top k profiles ranked on magnitude
- [x] show the recommendations of these films
- [x] sort genres by (meanRating & dateRatedWeight) instead of vector magnitude because it's inherently flawed
- [x] if a genre profile clashes with favouriteProfile, pick another genre

## Old Profile
- [x] implement basic version
- [x] implement advanced version with multiple genres

## Obscure Profile
- [x] implement basic version
- [x] implement advanced version with multiple genres

## International Profile
- [x] implement basic version
- [x] use countries instead of languages (fuck Alvin & the Chipmunks)
- [x] if GB or US is max, set both to 0.0 instead of only one of them

## Favourite Profile
- [x] implement
- [x] error handling if no fav films

# Reinforcement Learning Round 2
- [x] ensure `reviewRecommendation` works
- [x] re-implement `regen` after extensive refactoring
- [x] revise the maths behind reinforcement learning
- [x] revise genre profile implementation after testing RL
- [x] regen should take out **all** recommended films, not just films the user has reviewed

# Backend
- [x] for imdb, only vectorize films in userData that are in allFilmData (otherwise we can't get access to film languages, 
countries, poster)
- [x] I think it's done for letterboxd already but double check functionality
- [x] check functionality of backend works after offline phase additions

# Misc
- [x] switch from my-film-data.json to ratings.csv
- [x] add numVotes & runtime to human data
- [x] vectorize numberOfVotes & runtime
- [x] error handling for imported ratings.csv
- [x] delete title.x.tsv files after getting all-film-data.json
- [x] don't normalise myRating
- [x] don't fix imdbRating to 1.0
- [x] instead of writing all-film-data-vec, my-film-data, etc. to file, create global variables in app.py, and then 
create endpoints for getters/setters
- [x] deletion of ratings/diary.csv before saving to file
- [x] create myFilmData from imported diary.csv through Flask (letterboxd)
- [x] bug: if two profiles recommend the same film, the other profile should look for another film to replace it
- [x] bug: imdb recency doesn't work

# Windows OS
- [x] config frontend: npm, etc.
- [x] run flask app
- [x] fix windows upload diary.csv error

# Scripts
- [x] merge the 3 .sh files into one, consider renaming it as vectorizing can be included into it
- [x] reduce run.sh to startup.sh
- [x] change run.sh to reflect various changes
- [x] for .sh files change paths to be relative to device

# Recommendation Algorithm Round 1
- [x] all-film-data doesn't filter out films that have been rated
- [x] init-my-film-data filters out films that have been rated from all-film-data (also rm vector entries)
- [x] keep title.basics.tsv & title.ratings.tsv
- [x] add last-imdb-download-timestamp.txt. if downloaded <24 hours, skip the step
- [x] finish init-my-file-data.py to reflect above changes
- [x] research how/where to store files, run .py scripts etc.
- [x] upload button calls /verifyUserUploadedFile API
- [x] upload error handling
- [x] change return type of recs function
- [x] init_rec writes all-film-data.json (w/o user rated films), my-film-data.json, all-film-data-vec.json, 
my-film-data-vec.json to file
- [x] call init_rec endpoint once when new page is loaded
- [x] thumbs up/down state logic
- [x] bug with user profile?

# Nice to Have
- [x] change some files to get rid of hyphens, so I don't need an imported library to import them

# Recommendation Algorithm Round 2
- [x] get rid of countries. having country + language might be diminishing returns
- [x] do countries instead of languages BECAUSE ALVIN & THE CHIPMUNKS IS BEING RECOMMENDED AS A FOREIGN FILM
- [x] use user profile for old, obscure, international? results are disappointing despite multiple genres
- [x] include profileId in row instead of at film-level
- [x] interpret vector function "e.g. because you liked 2000s American Comedy Films"
- [x] combine cachedUserRating and cachedDateRated together, multiplication operations are wasted
- [x] delete obscureProfile? doesn't really work as expected, films aren't so 'obscure'
- [x] move around the profiles to something better
- [x] remove clashing, worse results
- [x] international: if no other countries than US/GB, return zero vector

## Testing & Evaluation
- [x] ~~test if specialized vector magnitude makes a better difference~~ results are ass so went back to normal vector magnitude
- [x] curve genres & countries **better results**
- [x] `DATE_RATED_WEIGHT`?
- [x] ~~try without runtime? if no difference, get rid of it~~ it does make a slight difference, gonna leave it in
- [x] `REC_REVIEW_FEEDBACK_FACTOR`?

# Code-Related & Functionality
- [x] double check I didn't remove any necessary `global`s and fuck it up
- [x] tidy up code, make things as efficient as possible
- [x] work with np vector instead of list? is it more efficient? 
- [x] letterboxd search can be much more efficient
- [x] ensure that a user can go back to home page and upload new file and recs still work smoothly
- [x] go through all code removing redundancy, fine-tuning
- [x] rename variables & func to lowerCamelCase
- [x] change variables that are not constant from UPPER_CASE to underscore case
- [x] minimise global variables (you only need to call global if you want to **modify** the variable)
- [x] error handling on potential div by 0 errors
- [x] reduce comments in code and make it more readable (after watching code aesthetic's video)
- [x] load in all files on the home page instead of waiting for the user to upload their files **just need to do for 
`all-film-data.json`**
- [x] error handling for no recent films
- [x] error handling for no favourite films
- [x] error handling on all file imports, api requests, etc. try-except
- [x] error handling for zero vector returns (in case it happens)
- [x] separate code pieces into separate classes/files; modularity wya
- [x] you can iterate through keys in a dict **without** the need to call `*.keys()`!!! change this!
- [x] `range(*)` is called once in python, no need to declare for loop limit beforehand

# Frontend
- [x] do text div 
- [x] do file upload (visuals only) div
- [x] href what is rating.csv/how to export it
- [x] finish home page (visuals only, file upload func later)
- [x] re-do text element showing selected files, errors, etc. (lost changes rip)
- [x] manage multiple pages (check sweng project)
- [x] go to results page if verifyUserUploadedFile ok
- [x] verify api calls for vector change funcs are working
- [x] /initial_recs api calls more than once?

## Recommendations Page
- [x] reduce vertical gap size between elements
- [x] put filmYear on same line as filmTitle
- [x] center the row
- [x] add genres to film div
- [x] re-do buttons
- [x] similarity score
- [x] change the star
- [x] get nice font
- [x] summary scroll
- [x] make film div fixed size
- [x] change colours
- [x] regen button
- [x] align the fucking icons with text

## Home Page
- [x] fix background
- [x] do home text and file upload container

# Finishing Touches
- [x] play around with `YEAR_WEIGHT`
- [x] play around with `GENRE_WEIGHT`
- [x] try fixing imdbRating to 1.0?

# Deployment
- [ ] figure out where to host flask app
- [ ] figure out react deployment

# README
- [ ] do `README.md`
