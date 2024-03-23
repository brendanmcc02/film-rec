# downloads, filters and vectorizes all-film-data.
# this is intended to run when the website starts up, hence startup.sh

cd ..
git pull

printf "\n[1/2] Downloading title.basics.tsv & title.ratings.tsv..."
cd data/ || exit

# download title.basics.tsv.gz & title.ratings.tsv.gz (only if it's been >24 hours)
cd ../backend/ || exit
python3 download-all-film-data.py
cd ../data || exit

# unzip the .gz files, only if .gz files have been downloaded
if test -f title.basics.tsv.gz; then
  if test -f title.basics.tsv; then
    rm title.basics.tsv
  fi
  gzip -d title.basics.tsv.gz
fi
if test -f title.ratings.tsv.gz; then
  if test -f title.ratings.tsv; then
    rm title.ratings.tsv
  fi
  gzip -d title.ratings.tsv.gz
fi

printf "\n[2/2] Initialising all-film-data-vectorized.json..."
cd ../backend/ || exit
python3 init-all-film-data.py

git add ../data/
git commit -m "downloaded, filtered, and vectorized all-film-data.json"
git push
