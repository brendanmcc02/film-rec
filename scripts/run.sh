# fetches, filters and vectorizes all-film-data & my-film-data.
# then, produce the recommended 25 films

cd ..
git pull
printf "\n[1/5] Downloading ratings.csv from my IMDb account...\n"
cd data/ || exit
rm ratings.csv
cd ../src/ || exit
python3 download-ratings.py

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

