REM function to unzip .gz file
Function DeGZip-File{
    Param(
        $infile,
        $outfile = ($infile -replace '\.gz$','')
    )

    $input = New-Object System.IO.FileStream $inFile, ([IO.FileMode]::Open), ([IO.FileAccess]::Read), ([IO.FileShare]::Read)
    $output = New-Object System.IO.FileStream $outFile, ([IO.FileMode]::Create), ([IO.FileAccess]::Write), ([IO.FileShare]::None)
    $gzipStream = New-Object System.IO.Compression.GzipStream $input, ([IO.Compression.CompressionMode]::Decompress)

    $buffer = New-Object byte[](1024)
    while($true){
        $read = $gzipstream.Read($buffer, 0, 1024)
        if ($read -le 0){break}
        $output.Write($buffer, 0, $read)
    }

    $gzipStream.Close()
    $output.Close()
    $input.Close()
}

@ECHO OFF
REM downloads, filters, and produces all-film-data.json

cd ..
git pull

ECHO [1/2] Downloading title.basics.tsv & title.ratings.tsv...

REM download title.basics.tsv.gz & title.ratings.tsv.gz (only if it's been >3 days)
cd backend
python .\download-all-film-data.py
cd ../data

REM unzip the .gz files, only if .gz files have been downloaded
if exist title.basics.tsv.gz (
  if exist title.basics.tsv (
    del title.basics.tsv
  )

    DeGZip-File "title.basics.tsv.gz" "title.basics.tsv"
)
if exist title.ratings.tsv.gz (
  if exist title.ratings.tsv (
    del title.ratings.tsv
  )

    DeGZip-File "title.ratings.tsv.gz" "title.ratings.tsv"
)

REM run init-all-film-data.py on .tsv files
if exist title.ratings.tsv AND exist title.basics.tsv (
    ECHO [2/2] Initialising all-film-data.json...
    cd ../backend
    python .\init-all-film-data.py

    del ../data/title.basics.tsv
    del ../data/title.ratings.tsv

    git add ../data
    git commit -m "downloaded and filtered all-film-data.json"
    git push
) else (
    ECHO [2/2] all-film-data.json was initialised >3 days ago, so the script was not run.
)

PAUSE
