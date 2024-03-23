# downloads, filters and vectorizes all-film-data.
# filters and vectorizes my-film-data.
# user needs to have ratings.csv in data/ to proceed
# then, produce the recommended and non-recommended films

cd ..
git pull
# *** DEPRECATED, read comments in download-my-film-data.py to see why
#printf "\n[1/5] Downloading ratings.csv from my IMDb account...\n"
#cd src/ || exit
#python3 download-my-film-data.py

printf "\n[1/5] Downloading title.basics.tsv & title.ratings.tsv..."
cd data/ || exit
# if there are left over files, delete them before re-downloading
if test -f title.basics.tsv.gz; then
  rm title.basics.tsv.gz
fi
if test -f title.ratings.tsv.gz; then
  rm title.ratings.tsv.gz
fi
if test -f title.basics.tsv; then
  rm title.basics.tsv
fi
if test -f title.ratings.tsv; then
  rm title.ratings.tsv
fi

cd ../src/ || exit
python3 download-all-film-data.py
# unzip the .gz files
cd ../data || exit
gzip -d title.basics.tsv.gz
gzip -d title.ratings.tsv.gz

printf "\n[2/5] Initialising my-film-data.json..."
if ! test -f ratings.csv; then
  printf "\n ratings.csv not found. Please export it to data/.\n"
  exit
fi

cd ../src/ || exit
python3 init-my-film-data.py
rm ../data/ratings.csv  # # delete the csv file

printf "\n[3/5] Initialising all-film-data.json..."
cd ../src/ || exit
python3 init-all-film-data.py
# delete title.basics.tsv & title.ratings.tsv files
rm ../data/title.basics.tsv
rm ../data/title.ratings.tsv

printf "\n[4/5] Vectorize both all-film-data.json & my-film-data.json"
python3 vectorize.py

printf "\n[5/5] Calculating recommended and non-recommended films:\n"
python3 rec.py
git add ../data/
git commit -m "downloaded, filtered, and vectorized all-film-data & my-film-data"
git push
