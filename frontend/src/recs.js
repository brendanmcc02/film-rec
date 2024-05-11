import './App.css';
import background from "./social-network-2.jpeg"
import React, { useState, useEffect } from 'react';

const App = () => {

    let initButtonStates = Array.from({ length: 20 }, () => false);

    const [films, setFilms] = useState([]);
    const [upButtonStates, setUpButtonStates] = useState(initButtonStates);
    const [downButtonStates, setDownButtonStates] = useState(initButtonStates);

    useEffect(() => {
        fetch('/init_rec')
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
    function handleUpButton(index) {
        const newUpButtonStates = upButtonStates.map(async (state, i) => {
            if (i === index) {
                if (state) {
                    return false;
                } else {
                    // if the down button was pressed, undo the changes made to the user profile
                    if (downButtonStates[index]) {
                        // undo vector changes todo
                        try {
                            const response = await fetch(`/undo_change?index=$\{index}&add=$\{True}`);

                            if (!response.ok) {
                                console.log('Undo change API request not ok. Index: ' + index);
                            }
                        } catch (error) {
                            console.log('Undo change API request failed. Index: ' + index);
                        }
                    }

                    setDownButton(index, false); // down = false

                    // increase vector todo
                    try {
                        const response = await fetch(`/change_user_profile?index=$\{index}&add=$\{True}`);

                        if (!response.ok) {
                            console.log('Undo change API request not ok. Index: ' + index);
                        }
                    } catch (error) {
                        console.log('Undo change API request failed. Index: ' + index);
                    }

                    return true; // up = true
                }
            } else {
                return state;
            }
        });

        setUpButtonStates(newUpButtonStates);
    }

    // called when down button is pressed
    function handleDownButton(index) {
        const newDownButtonStates = downButtonStates.map((state, i) => {
          if (i === index) {
              if (state) {
                  return false;
              } else {
                  if (upButtonStates[index]) {
                      // revert vector changes todo
                  }

                  setUpButton(index, false); // up = false

                  // decrease vector todo
                  return true; // down = true
              }
          } else {
            return state;
          }
        });

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

    let filmRecs = films.map((film, i) =>
        <div key={i}>
            <p>{film.similarity_score}% - {film.title} ({film.year}) {film.genres}</p>
            <button className="up-button" onClick={() => {handleUpButton(i);}}>Up</button>
            <button className="down-button" onClick={() => {handleDownButton(i);}}>Down</button>
        </div>
    );

    return (
        <>
            <div style={backgroundStyle}></div>
            <div className="title">
                <h1>RECS PAGE</h1>
                <h3>A film recommendation app.</h3>
            </div>

            <div className="file-div">
                {filmRecs}
            </div>
        </>
    );
}

export default App;
