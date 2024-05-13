// imports
import './App.css';
import background from "./social-network-2.jpeg"
import React, { useState, useEffect } from 'react';

// make an API call to get the global constant TOTAL_RECS from app.py
const response = await fetch('/getTotalRecs');
const TOTAL_RECS = parseInt(await response.text());
const initButtonStates = Array.from({ length: TOTAL_RECS }, () => false);

const App = () => {

    const [films, setFilms] = useState([]);
    const [upButtonStates, setUpButtonStates] = useState(initButtonStates);
    const [downButtonStates, setDownButtonStates] = useState(initButtonStates);

    useEffect(() => {
        fetch('/initRec')
            .then((response) => response.json())
            .then((jsonData) => {
                setFilms(jsonData); // Update state with fetched data
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
            });
    }, []); // Empty dependency array ensures this effect runs once on component mount

    const backgroundStyle = {
        backgroundImage: `url(${background})`,
        height: '100vh',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover'
    }

    // called when up button is pressed
    async function handleUpButton(index) {
        const newUpButtonStates = await Promise.all(upButtonStates.map(async (state, i) => {
            if (i === index) {
                if (state) {
                    // undo vector changes
                    await undoVectorChanges(index, "false")
                    return false;
                } else {
                    // if the down button was pressed, undo vector changes
                    if (downButtonStates[index]) {
                        await undoVectorChanges(index, "true");
                    }

                    setDownButton(index, false); // down = false

                    // increase vector
                    await changeVector(index, "true");

                    return true; // up = true
                }
            } else {
                return state;
            }
        }));

        setUpButtonStates(newUpButtonStates);
    }

    // undo vector changes
    async function undoVectorChanges(index, add) {
        try {
            const fetchUrl = "/undoResponse?index=" + index.toString() + "&add=" + add
            const response = await fetch(fetchUrl);

            if (!response.ok) {
                console.log('Undo change API request not ok. Index: ' + index);
            } else {
                console.log(await response.text());
            }
        } catch (error) {
            console.log('Undo change API request failed. Index: ' + index);
        }
    }

    async function changeVector(index, add) {
        try {
            const fetchUrl = "/response?index=" + index.toString() + "&add=" + add
            const response = await fetch(fetchUrl);

            if (!response.ok) {
                console.log('Change user profile API request not ok. Index: ' + index);
            } else {
                console.log(await response.text());
            }
        } catch (error) {
            console.log('Change user profile API request failed. Index: ' + index);
        }
    }

    // called when down button is pressed
    async function handleDownButton(index) {
        const newDownButtonStates = await Promise.all(downButtonStates.map(async (state, i) => {
          if (i === index) {
              if (state) {
                  // undo vector changes
                  await undoVectorChanges(index, "true")
                  return false;
              } else {
                  if (upButtonStates[index]) {
                  // undo vector changes
                        await undoVectorChanges(index, "false");
                  }

                  setUpButton(index, false); // up = false

                  // decrease vector
                  await changeVector(index, "false");
                  return true; // down = true
              }
          } else {
            return state;
          }
        }));

        setDownButtonStates(newDownButtonStates);
    }

    // set the state of the up button specified by an index
    function setUpButton(index, stateValue) {
        const newUpButtonStates = upButtonStates.map((state, i) => {
          if (i === index) {
              return stateValue;
          } else {
            return state;
          }
        });

        setUpButtonStates(newUpButtonStates);
    }

    // set the state of the down button specified by an index
    function setDownButton(index, stateValue) {
        const newDownButtonStates = downButtonStates.map((state, i) => {
          if (i === index) {
              return stateValue;
          } else {
            return state;
          }
        });

        setDownButtonStates(newDownButtonStates);
    }

    async function handleRegenButton() {
        let changeMade = false;

        // check if the user has given a 'thumbs up' to any film
        let len = upButtonStates.length;
        for (let i = 0; i < len && !changeMade; i++) {
            if (upButtonStates[i]) {
                changeMade = true;
            }
        }

        // check if the user has given a 'thumbs down' to any film
        for (let i = 0; i < len && !changeMade; i++) {
            if (downButtonStates[i]) {
                changeMade = true;
            }
        }

        // only call /regen if the user has responded to > 1 rec
        if (changeMade) {
            try {
                let response = await fetch('/regen');
                setFilms(await response.json());
                setUpButtonStates(initButtonStates); // reset up button states
                setDownButtonStates(initButtonStates); // reset down button states
                console.log("Called /regen");
            } catch (error) {
                console.error('Error fetching /regen API:', error);
            }
        } else {
            console.log("No changes made, so /regen not called.");
        }
    }

    let filmRecs = films.map((film, i) =>
        <div key={i}>
            <p>{film.similarityScore}% - {film.title} ({film.year}), {film.genres}. Wildcard: {film.wildcard}</p>
            <button className="up-button" onClick={() => {handleUpButton(i);}}>
                Up
            </button>
            <button className="down-button" onClick={() => {handleDownButton(i);}}>
                Down
            </button>
        </div>
    );

    return (
        <>
            <div style={backgroundStyle}></div>
            <div className="title">
                <button className="regen-button" onClick={() => {handleRegenButton();}}>
                    Regen
                </button>
            </div>

            <div className="file-div">
                {filmRecs}
            </div>
        </>
    );
}

export default App;
