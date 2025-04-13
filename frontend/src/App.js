import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileImport } from '@fortawesome/free-solid-svg-icons';
import { faFileUpload } from '@fortawesome/free-solid-svg-icons';
import { FaRegThumbsUp, FaRegThumbsDown } from "react-icons/fa";
import { FaRegStar } from "react-icons/fa";
import { TbRefresh } from "react-icons/tb";
import { FaInfoCircle } from "react-icons/fa";

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [errorText, setErrorText] = useState("");
  const [fileName, setFileName] = useState("");
  const [rowsOfRecommendations, setRowsOfRecommendations] = useState([]);
  const [rowsOfRecommendationButtonVisibility, setRowsOfRecommendationButtonVisibility] = useState([]);
  const [overflowY, setOverflowY] = useState('hidden');

  const homeScrollTargetReference = useRef(null);
  const recommendationsScrollTargetReference = useRef(null);
  const guidRef = useRef("");

  const FILE_UPLOADED_SUCCESSFULLY_TEXT = "File upload successful.";

  useEffect(() => {
    if (rowsOfRecommendations.length > 0 && recommendationsScrollTargetReference.current) {
      recommendationsScrollTargetReference.current.scrollIntoView({
        behavior: 'smooth',
      });
    }
  }, [rowsOfRecommendations]);

  useEffect(() => {
    if (homeScrollTargetReference.current) {
      homeScrollTargetReference.current.scrollIntoView({
        behavior: 'smooth',
      });
      setOverflowY('hidden');
    }
  }, [selectedFile]);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
    setFileName("Selected File: " + event.target.files[0].name);
    setErrorText("");
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('https://film-rec-backend.onrender.com/getInitialRowsOfRecommendations', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        setErrorText(FILE_UPLOADED_SUCCESSFULLY_TEXT);
        setOverflowY('auto');
        
        const responseJson = await response.json();
        guidRef.current = responseJson.guid;
        const responseRowsOfRecommendations = responseJson.rowsOfRecommendations;

        setRowsOfRecommendations(responseRowsOfRecommendations);

        const initialButtonVisibility = responseRowsOfRecommendations.map((row) => 
          row.recommendedFilms.map((film) => ({ 
              filmID: film.id, 
              isFilmButtonVisible: true
          }))
        );

        setRowsOfRecommendationButtonVisibility(initialButtonVisibility);
      } else {
        setErrorText(await response.text());
        setRowsOfRecommendations([]);
        setRowsOfRecommendationButtonVisibility([]);
      }
    } catch (error) {
      setErrorText(error.message);
    }
  };

  function isFilmButtonVisible(filmID) {
      for (const row of rowsOfRecommendationButtonVisibility) {
        for (const film of row) {
          if (film.filmID === filmID) {
            return film.isFilmButtonVisible;
          }
        }
      }

      return false;
  }

  function setFilmButtonInvisible(filmID) {
      setRowsOfRecommendationButtonVisibility((previousVisibility) => 
          previousVisibility.map((row) => 
              row.map((film) => 
                  film.filmID === filmID ? { ...film, isFilmButtonVisible: false } : film
              )
          )
      );
    }

  async function handleThumbsUpOrDownButton(filmId, isThumbsUp) {
      await reviewRecommendation(filmId, isThumbsUp);
      setFilmButtonInvisible(filmId);
  }

  async function reviewRecommendation(filmId, isThumbsUp) {
      try {
          const fetchUrl = ("https://film-rec-backend.onrender.com/reviewRecommendation" +
                            "?filmId=" + filmId.toString() + "&isThumbsUp=" + isThumbsUp + "&guid=" + guidRef.current.toString());
          const response = await fetch(fetchUrl);

          if (!response.ok) {
              console.log('reviewRecommendation response not ok. filmID: ' + filmId);
          } else {
              console.log(await response.text());
          }
      } catch (error) {
          console.log('error with reviewRecommendation. filmID: ' + filmId);
      }
  }
  
  async function handleRegenerateRecommendationsButton() {
      const fetchUrl = ("https://film-rec-backend.onrender.com/regenerateRecommendations" + "?guid=" + guidRef.current.toString());
      const response = await fetch(fetchUrl);

      const responseJson = await response.json();
      const responseRowsOfRecommendations = responseJson.rowsOfRecommendations;
      
      setRowsOfRecommendations(responseRowsOfRecommendations);
      const initialButtonVisibility = responseRowsOfRecommendations.map((row) => 
          row.recommendedFilms.map((film) => ({ 
              filmID: film.id, 
              isFilmButtonVisible: true
          }))
      );

      setRowsOfRecommendationButtonVisibility(initialButtonVisibility);
      console.log("Regenerated film recommendations.")
  }

  function getFilms(recommendedFilms) {
      return recommendedFilms.map((film, i) => (
          <div className="recommendedFilm" key={i}>
              <img src={`${film.poster}`} alt={film.title} className="posterImg" loading="lazy" />
              <div className='film-details'>
              <div className='film-title-and-year-container'>
                  <h2 className='film-title-and-year opacity-fade-in'>{film.title}&nbsp;({film.year})</h2>
                  <h2 className='film-info'><a href={film.imdbUrl} target="_blank"><FaInfoCircle /></a></h2>
              </div>
                  <div className='film-rating-runtime-genres-container opacity-fade-in'>
                      <h3 className='star'><FaRegStar /></h3>
                      <h3 className='film-rating-runtime-genres-text'>{film.imdbRating} | {film.runtimeHoursMinutes} | {getCommaSeparatedList(film.genres)}</h3>
                  </div>
                  <p className='film-summary hidden-scroll-bar opacity-fade-in'>
                      {film.summary}
                  </p>

                  <div className='buttons-and-similarity-score-container'>
                      {isFilmButtonVisible(film.id) && 
                          <div className="buttons-container">
                              <button className="up-down-button up-button opacity-fade-in" onClick={() => handleThumbsUpOrDownButton(film.id, true)}>
                                  <FaRegThumbsUp />
                              </button>
                              <button className="up-down-button down-button opacity-fade-in" onClick={() => handleThumbsUpOrDownButton(film.id, false)}>
                                  <FaRegThumbsDown />
                              </button>
                          </div>
                      }
                      
                      <p className="similarity-score opacity-fade-in">{film.similarityScore}%&nbsp;Match</p>
                  </div>
              </div>
          </div>
      ));
  }

  let rows = rowsOfRecommendations.map((row, i) => (
      <div key={i} className='recommendedRow'>
          <h1 className="recommendedRowText opacity-fade-in">{row.recommendedRowText}</h1>
          <div className="rowOfFilms">{getFilms(row.recommendedFilms)}</div>
      </div>
  ));

  function getCommaSeparatedList(originalList) {
      let commaSeparatedList = "";
      let isFirstElement = true;

      originalList.forEach(element => {
          if (isFirstElement) {
              commaSeparatedList += element;
          } else {
              commaSeparatedList += ", " + element;
          }

          isFirstElement = false;
          
      })

      return commaSeparatedList;
  }

  return (
    <>
      <div className='home-container' ref={homeScrollTargetReference}>
        <div className='title-and-subtitle-container'>
          <h1 className="home-title">FILM REC</h1>
          <h3 className='home-subtitle'>A film recommendation web app.</h3>
        </div>
        <div className='text-and-file-select-upload-container'>
          <div className="home-text-container">
            <h3 className='home-text'>Letterboxd users: Upload your <a
                href="https://letterboxd.com/data/export"><u>zip</u></a> file.</h3>
            <h3 className='home-text'>IMDB Users: Upload your <a href="https://www.imdb.com/exports/?ref_=rt" target="_blank"><u>exported
              ratings .csv</u></a> file.</h3>
              <h3 className='home-text'>Don't have a Letterboxd or IMDB account? Use 
                <a href="https://github.com/brendanmcc02/film-rec/blob/main/sample-letterboxd-data.csv" target="_blank">
                &nbsp;<u>this</u></a> sample dataset.</h3>
          </div>

          <div className="file-select-upload-container">
            <label htmlFor="select-file" className="base-button file-select-upload-button opacity-fade-in">
              <FontAwesomeIcon icon={faFileImport} className="select-file-icon" />&nbsp; Select
              <input id="select-file" type="file" onChange={handleFileSelect} />
            </label>

            <p className="file-text">{fileName}</p>

            <button className="base-button file-select-upload-button opacity-fade-in" onClick={handleFileUpload}>
              <FontAwesomeIcon icon={faFileUpload} className="select-file-icon" />&nbsp; Upload
            </button>

            <p className="file-text">{errorText}</p>
          </div>
        </div>
        <div className="patience-container">
          <h3 className="home-text">
            If the upload button is not responding, it's because the service goes down after inactivity.
          </h3>
          <h3 className="home-text">
            Please wait around 1-2 minutes after uploading your file.
          </h3>
          <h3 className="home-text">
            Your patience is appreciated - this isn't Netflix!
          </h3>
        </div>
        <div className='created-by-container'>
          <h3 className='additional-italic-text'>
            Created by <a href="https://github.com/brendanmcc02/" target="_blank"><u>Brendan McCann.</u></a>
          </h3>
        </div>
        <div className='behind-the-scenes-container'>
          <h3 className='additional-italic-text'>
            Interested in how it works? 
            See <a href="https://github.com/brendanmcc02/film-rec/blob/main/README.md" target="_blank"><u>here.</u></a>
          </h3>
        </div>
      </div>
      <div className="recommendations-container" ref={recommendationsScrollTargetReference}>
        <button className="base-button regenerate-button opacity-fade-in" onClick={() => handleRegenerateRecommendationsButton()}>
            <TbRefresh className='regenerate-icon'/>&nbsp;Regenerate
        </button>
        <div className='rows'>
            {rows}
        </div>
      </div>
      <style>
        {`
          body {
            overflow-y: ${overflowY};
          }
        `}
      </style>
    </>
  );
}

export default App;
