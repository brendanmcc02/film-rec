# downloads, filters and vectorizes all-film-data.
# filters and vectorizes my-film-data.
# user needs to have ratings.csv in data/ to proceed
# then, produce the recommended and non-recommended films

cd ..
git pull

printf "\n[1/4] Downloading title.basics.tsv & title.ratings.tsv..."
cd data/ || exit

# download title.basics.tsv.gz & title.ratings.tsv.gz (only if it's been >24 hours)
cd ../backend/ || exit
python3 download-all-film-data.py
cd ../data || exit
# before unzipping, delete leftover .tsv files if they are still in the folder
if test -f title.basics.tsv; then
  rm title.basics.tsv
fi
if test -f title.ratings.tsv; then
  rm title.ratings.tsv
fi

# unzip the .gz files, only if .gz files have been downloaded
if test -f title.basics.tsv.gz; then
  gzip -d title.basics.tsv.gz
fi
if test -f title.ratings.tsv.gz; then
  gzip -d title.ratings.tsv.gz
fi

printf "\n[2/4] Initialising all-film-data-vectorized.json..."
cd ../backend/ || exit
python3 init-all-film-data.py

printf "\n[3/4] Initialising my-film-data-vectorized.json..."
if ! test -f ../data/ratings.csv; then
  printf "\n ratings.csv not found. Please export it to data/.\n"
  exit
fi

python3 init-my-film-data.py
rm ../data/ratings.csv  # # delete the csv file

printf "\n[4/4] Calculating recommended films:\n"
python3 rec.py
git add ../data/
git commit -m "downloaded, filtered, and vectorized all-film-data & my-film-data"
git push
