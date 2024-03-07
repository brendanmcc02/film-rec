# fetches, filters and vectorizes all-film-data & my-film-data

git pull
printf "\n[1/4] Copying my-film-data.json from film-data-vis repo...\n"
cd ..
git pull
# copies film-data.json from film-data-vis to current repo
cp ../film-data-vis/data/film-data.json data/
# remove all the attributes that are not needed in the dataset
cd src/ || exit
python3 filter-my-data.py
# remove film-data.json
cd ../data/ || exit
rm film-data.json
git add my-film-data.json
git commit -m "copied & changed my-film-data.json"
git push

printf "\n[2/4] Downloading title.basics.tsv & title.ratings.tsv from https://datasets.imdbws.com/..."
cd ../src/ || exit
python3 download-imdb-gz-files.py

# unzip the .gz files
cd ../data || exit
gzip -d title.basics.tsv.gz
gzip -d title.ratings.tsv.gz

printf "\n[3/4] Create all-film-data.json..."
cd ../src/ || exit
python3 init-all-film-data.py
# delete title.basics.tsv & title.ratings.tsv files
cd ../data || exit
rm title.basics.tsv
rm title.ratings.tsv

printf "\n[4/4] Vectorize both all-film-data.json & my-film-data.json"
cd ../src || exit
python3 vectorize.py
cd ../data || exit
git add .
git commit -m "fetched, filtered, and vectorized all-film-data & my-film-data"
git push
