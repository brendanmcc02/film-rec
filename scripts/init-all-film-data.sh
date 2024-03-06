# completely re-initialises all-film-data.json from scratch

git pull
printf "\n[1/3] Copying my-film-data.json from film-data-vis repo..."
./copy-my-film-data.sh

printf "\n[2/3] Downloading title.basics.tsv & title.ratings.tsv from https://datasets.imdbws.com/..."
cd ../scripts/ || exit
./download-imdb-data.sh

printf "\n[3/3] Filter the data..."
cd ../src/ || exit
python3 init-all-film-data.py
# delete title.basics.tsv & title.ratings.tsv files
cd ../data || exit
rm title.basics.tsv
rm title.ratings.tsv
cd ..
git add .
git commit -m "updated all-film-data.json"
git push
