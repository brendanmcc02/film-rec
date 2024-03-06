# copies film-data.json from film-data-vis to this repo.
# then run a filtering script on this data.

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
