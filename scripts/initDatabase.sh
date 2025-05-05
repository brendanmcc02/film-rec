clear
cd ..
git pull
git branch -D updateDatabase
git checkout -b updateDatabase

# download title.basics.tsv.gz & title.ratings.tsv.gz (only if it's been >12 hours)
cd backend/ || exit
python3 DownloadImdbFilmData.py
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
    printf "\n[2/2] Initialising allFilmData.json..."
    cd ../backend/ || exit
    python3 InitDatabase.py

    rm ../database/title.basics.tsv
    rm ../database/title.ratings.tsv

    git add ../database/
    git commit -m "Updating Database"
    git config --add --bool push.autoSetupRemote true
    git push
    # the echo | is necessary to simulate an enter keypress and submit the PR
    echo | gh pr create --title "Updating Database" --body "PR generated automatically"
    git checkout main
  fi
else
  printf "\n allFilmData.json was initialised >1 days ago, so the script was not run.\n"
fi
