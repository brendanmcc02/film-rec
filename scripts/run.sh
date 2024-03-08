# fetches, filters and vectorizes all-film-data & my-film-data.
# then, produce the recommended 25 films

cd ..
git pull
printf "\n[1/5] Copying my-film-data.json from film-data-vis repo...\n"
cd ../film-data-vis/data/ || exit
git pull
cp film-data.json ../../film-rec/data/
# remove all the attributes that are not needed in the dataset
cd ../../film-rec/src/ || exit
python3 filter-my-data.py
# remove film-data.json
cd ../data/ || exit
rm film-data.json

printf "\n[2/5] Downloading title.basics.tsv & title.ratings.tsv from https://datasets.imdbws.com/..."
cd ../src/ || exit
python3 download-imdb-gz-files.py

# unzip the .gz files
cd ../data || exit
gzip -d title.basics.tsv.gz
gzip -d title.ratings.tsv.gz

printf "\n[3/5] Create all-film-data.json..."
cd ../src/ || exit
python3 init-all-film-data.py
# delete title.basics.tsv & title.ratings.tsv files
cd ../data || exit
rm title.basics.tsv
rm title.ratings.tsv

printf "\n[4/5] Vectorize both all-film-data.json & my-film-data.json"
cd ../src || exit
python3 vectorize.py

printf "\n[5/5] Calculating 25 recommended films:\n"
python3 rec.py
cd ../data || exit
git add .
git commit -m "fetched, filtered, and vectorized all-film-data & my-film-data"
git push

