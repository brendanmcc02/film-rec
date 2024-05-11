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
    async function handleUpButton(index) {
        const newUpButtonStates = await Promise.all(upButtonStates.map(async (state, i) => {
            if (i === index) {
                if (state) {
                    // undo vector changes
                    await undoUserProfileChanges(index, "false")
                    return false;
                } else {
                    // if the down button was pressed, undo the changes made to the user profile
                    if (downButtonStates[index]) {
                        await undoUserProfileChanges(index, "true");
                    }

                    setDownButton(index, false); // down = false

                    // increase vector
                    await changeUserProfile(index, "true");

                    return true; // up = true
                }
            } else {
                return state;
            }
        }));

        setUpButtonStates(newUpButtonStates); // todo check if states are still maintained
    }

    // undo vector changes
    async function undoUserProfileChanges(index, add) {
        try {
            const fetchUrl = "/undo_change?index=" + index.toString() + "&add=" + add
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

    async function changeUserProfile(index, add) {
        try {
            const fetchUrl = "/change_user_profile?index=" + index.toString() + "&add=" + add
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
                  await undoUserProfileChanges(index, "true")
                  return false;
              } else {
                  if (upButtonStates[index]) {
                  // undo vector changes
                        await undoUserProfileChanges(index, "false");
                  }

                  setUpButton(index, false); // up = false

                  // decrease vector
                  await changeUserProfile(index, "false");
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
