import React, { useState, useEffect } from 'react';
import { FaRegThumbsUp, FaRegThumbsDown } from "react-icons/fa";
import { FaRegStar } from "react-icons/fa";
import { TbRefresh } from "react-icons/tb";

const App = () => {
    const [rowsOfRecommendations, setRowsOfRecommendations] = useState([]);
    const [rowsOfRecommendationButtonVisibility, setRowsOfRecommendationButtonVisibility] = useState([]);

    useEffect(() => {
        fetch('https://film-rec-backend.onrender.com/initRowsOfRecommendations')
            .then((response) => response.json())
            .then((jsonData) => {
                setRowsOfRecommendations(jsonData);
                const initialButtonVisibility = jsonData.map((row) => 
                    row.recommendedFilms.map((film) => ({ 
                        filmID: film.id, 
                        isFilmButtonVisible: true
                    }))
                );
    
                setRowsOfRecommendationButtonVisibility(initialButtonVisibility);
            })
            .catch((error) => {
                console.error('Error fetching initial rows of recommendations:', error);
            });
    }, []); // Empty dependency array ensures this effect runs once on component mount

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

    async function handleUpButton(filmId) {
        await reviewRecommendation(filmId, true);
        setFilmButtonInvisible(filmId);
    }

    async function handleDownButton(filmId) {
        await reviewRecommendation(filmId, false);
        setFilmButtonInvisible(filmId);
    }

    async function reviewRecommendation(filmId, isThumbsUp) {
        try {
            const fetchUrl = ("https://film-rec-backend.onrender.com/reviewRecommendation?filmId=" 
                                + filmId.toString() + "&isThumbsUp=" + isThumbsUp)
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
        const response = await fetch('https://film-rec-backend.onrender.com/regenerateRecommendations');
        const jsonData = await response.json();
        setRowsOfRecommendations(jsonData);
        const initialButtonVisibility = jsonData.map((row) => 
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
                    </div>
                    <div className='film-rating-runtime-genres-container opacity-fade-in'>
                        <h3 className='star'><FaRegStar /></h3>
                        <h3 className='film-rating-runtime-genres-text'>{film.imdbRating} |&nbsp;</h3>
                        <h3 className='film-rating-runtime-genres-text'>{film.runtimeHoursMinutes} |&nbsp;</h3>
                        <h3 className='film-rating-runtime-genres-text'>{getCommaSeparatedList(film.genres)}</h3>
                    </div>
                    <p className='film-summary hidden-scroll-bar opacity-fade-in'>
                        {film.summary}
                    </p>

                    <div className='buttons-and-similarity-score-container'>
                        {isFilmButtonVisible(film.id) && 
                            <div className="buttons-container">
                                <button className="up-down-button up-button opacity-fade-in" onClick={() => handleUpButton(film.id)}>
                                    <FaRegThumbsUp />
                                </button>
                                <button className="up-down-button down-button opacity-fade-in" onClick={() => handleDownButton(film.id)}>
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
        <div className="button-and-rows-container">
            <button className="base-button regenerate-button opacity-fade-in" onClick={() => handleRegenerateRecommendationsButton()}>
                <TbRefresh className='regenerate-icon'/>&nbsp;Regenerate
            </button>
            <div className='rows'>
                {rows}
            </div>
        </div>
    );
    
}

export default App;
