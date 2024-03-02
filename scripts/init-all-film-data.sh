git pull
date
printf "\n[1/9] Updating my-film-data.json\n"
cd /home/brendanmcc02/Desktop/projects/film-rec/scripts/ || exit
./copy-my-film-data.sh
git add .
git commit -m "updated my-film-data.json"
git push
date
printf "\n[2/9] Downloading title.basics.tsv & title.ratings.tsv from https://datasets.imdbws.com/\n"
cd /home/brendanmcc02/Desktop/projects/film-rec/scripts/ || exit
./download-imdb-data.sh
date
printf "\n[3/9] Filtering out non-movies\n"
cd /home/brendanmcc02/Desktop/projects/film-rec/src/ || exit
python3 1-filter-only-movies.py
git add .
git commit -m "added 1-only-movies.json"
git push
date
printf "\n[4/9] Filtering out pre-1930 films\n"
python3 2-filter-post-1930.py
git add .
git commit -m "added 2-post-1930.json"
git push
date
printf "\n[5/9] Filtering out <60 min films\n"
python3 3-filter-over-60-min.py
git add .
git commit -m "added 3-over-60-min.json"
git push
date
printf "\n[6/9] Merging with title.ratings.tsv\n"
python3 4-merge-with-ratings.py
git add .
git commit -m "added 4-merge-with-ratings.json"
git push
date
printf "\n[7/9] Filtering out films with <10,000 votes\n"
python3 5-filter-over-10k-votes.py
git add .
git commit -m "added 5-over-10k-votes.json"
git push
date
printf "\n[8/9] Modifying order of json attributes\n"
python3 6-modify-json-order.py
git add .
git commit -m "added 6-modified-order.json"
git push
date
printf "\n[9/9] Filtering out films that I've rated\n"
python3 7-filter-unrated-films.py
git add .
git commit -m "added all-film-data.json"
git push
date
printf "\nCOMPLETE.\n"
