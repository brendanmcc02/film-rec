# copies film-data.json from film-data-vis to current repo
cp /home/brendanmcc02/Desktop/projects/film-data-vis/data/film-data.json /home/brendanmcc02/Desktop/projects/film-rec/data/
# remove all the attributes that are not needed in the dataset
cd /home/brendanmcc02/Desktop/projects/film-rec/src/ || exit
python3 filter.py
# remove film-data.json
cd /home/brendanmcc02/Desktop/projects/film-rec/data/ || exit
rm film-data.json

