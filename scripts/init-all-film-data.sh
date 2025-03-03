# downloads, filters, and produces multiple .json files.

clear
cd ..
git pull

# download title.basics.tsv.gz & title.ratings.tsv.gz (only if it's been >1 days)
cd backend/ || exit
python3 downloadAllFilmData.py
cd ../database || exit

printf "\n[1/2] Downloading title.basics.tsv & title.ratings.tsv..."
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

if test -f title.basics.tsv; then
  if test -f title.ratings.tsv; then
    printf "\n[2/2] Initialising all-film-data.json..."
    cd ../backend/ || exit
    python3 initAllFilmData.py

    rm ../database/title.basics.tsv
    rm ../database/title.ratings.tsv

    git add ../database/
    git commit -m "downloaded and filtered all-film-data.json"
    git push
  fi
else
  printf "\n all-film-data.json was initialised >1 days ago, so the script was not run.\n"
fi
