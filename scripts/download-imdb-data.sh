# download the .gz files
cd ../src/ || exit
python3 download-imdb-gz-files.py

# unzip the .gz files
cd ../data || exit
gzip -d title.basics.tsv.gz
gzip -d title.ratings.tsv.gz
