# downloads, filters and vectorizes all-film-data & my-film-data.
# then, produce the recommended and non-recommended films

cd ..
git pull
printf "\n[1/6] Downloading ratings.csv from my IMDb account...\n"
cd src/ || exit
python3 download-my-film-data.py

printf "\n[2/6] Downloading title.basics.tsv & title.ratings.tsv..."
python3 download-all-film-data.py
# unzip the .gz files
cd ../data || exit
gzip -d title.basics.tsv.gz
gzip -d title.ratings.tsv.gz

printf "\n[3/6] Initialising my-film-data.json..."
cd ../src/ || exit
python3 init-my-film-data.py
rm ../data/ratings.csv  # # delete the csv file

printf "\n[4/6] Initialising all-film-data.json..."
cd ../src/ || exit
python3 init-all-film-data.py
# delete title.basics.tsv & title.ratings.tsv files
rm ../data/title.basics.tsv
rm ../data/title.ratings.tsv

printf "\n[5/6] Vectorize both all-film-data.json & my-film-data.json"
python3 vectorize.py

printf "\n[6/6] Calculating recommended and non-recommended films:\n"
python3 rec.py
cd ../data || exit
git add .
git commit -m "downloaded, filtered, and vectorized all-film-data & my-film-data"
git push
