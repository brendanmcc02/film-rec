import './App.css';
import React, { useState, useEffect } from 'react';

const App = () => {
    const [rowsOfRecommendations, setRowsOfRecommendations] = useState([]);
    const [rowsOfRecommendationButtonVisibility, setRowsOfRecommendationButtonVisibility] = useState([]);

    useEffect(() => {
        fetch('/initRowsOfRecommendations')
            .then((response) => response.json())
            .then((jsonData) => {
                setRowsOfRecommendations(jsonData); // Update state with fetched database
                const initialButtonVisibility = jsonData.map((row) => 
                    row.recommendedFilms.map((film) => ({ 
                        filmID: film.id, 
                        isFilmButtonVisible: true
                    }))
                );
    
                setRowsOfRecommendationButtonVisibility(initialButtonVisibility);
            })
            .catch((error) => {
                console.error('Error fetching database:', error);
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
        console.log("Up button clicked for filmId: " + filmId);
        await reviewRec(filmId, true);
        setFilmButtonInvisible(filmId);
    }

    async function handleDownButton(filmId) {
        console.log("Down button clicked for filmId: " + filmId);
        await reviewRec(filmId, false);
        setFilmButtonInvisible(filmId);
    }

    async function reviewRec(filmId, isThumbsUp) {
        try {
            const fetchUrl = "/reviewRec?filmId=" + filmId.toString() + "&isThumbsUp=" + isThumbsUp
            const response = await fetch(fetchUrl);

            if (!response.ok) {
                console.log('Change user profile API request not ok. filmID: ' + filmId);
            } else {
                console.log(await response.text());
            }
        } catch (error) {
            console.log('Change user profile API request failed. filmID: ' + filmId);
        }
    }

    async function handleRegenButton() {
        // let changeMade = false;

        // // check if the user has given a 'thumbs up' to any film
        // let len = upButtonStates.length;
        // for (let i = 0; i < len && !changeMade; i++) {
        //     if (upButtonStates[i]) {
        //         changeMade = true;
        //     }
        // }

        // // check if the user has given a 'thumbs down' to any film
        // for (let i = 0; i < len && !changeMade; i++) {
        //     if (downButtonStates[i]) {
        //         changeMade = true;
        //     }
        // }

        // // only call /regen if the user has responded to > 1 rec
        // if (changeMade) {
        //     try {
        //         let response = await fetch('/regen');
        //         setRowsOfRecommendations(await response.json());
        //         setUpButtonStates(initButtonStates); // reset up button states
        //         setDownButtonStates(initButtonStates); // reset down button states
        //         console.log("Called /regen");
        //     } catch (error) {
        //         console.error('Error fetching /regen API:', error);
        //     }
        // } else {
        //     console.log("No changes made, so /regen not called.");
        // }
    }

    function getFilms(recommendedFilms) {
        return recommendedFilms.map((film, i) => (
            <div className="recommendedFilm" key={i}> 
                <img src={`${film.mainPoster}`} alt={film.title} className="mainPosterImg" />
                {isFilmButtonVisible(film.id) && 
                    <div className="buttons">
                        <button className="up-button" onClick={() => handleUpButton(film.id)}>
                            Up
                        </button>
                        <button className="down-button" onClick={() => handleDownButton(film.id)}>
                            Down
                        </button>
                    </div>
                }
            </div>
        ));
    }
    
    let rows = rowsOfRecommendations.map((row, i) => (
        <div key={i} className='recommendedRow'>
            <h1 style={{color:'black'}}>{row.recommendedRowText}</h1>
            <div className="rowOfFilms">{getFilms(row.recommendedFilms)}</div>
        </div>
    ));

    return (
        <>
            <button className="regen-button" onClick={() => handleRegenButton()}>
                    Regen
            </button>
            <div className='rows'>
                {rows}
            </div>
        </>
    );
    
}

export default App;
