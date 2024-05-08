import './App.css';
import background from "./social-network-2.jpeg"
import React, { useState, useEffect } from 'react';

const App = () => {

    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/init_rec')
            .then((response) => response.json())
            .then((jsonData) => {
                setData(jsonData); // Update state with fetched data
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

    const noBulletPoints = {
        listStyleType: 'none'
    }

    return (
        <>
            <div style={backgroundStyle}></div>
            <div className="title">
                <h1>RECS PAGE</h1>
                <h3>A film recommendation app.</h3>
            </div>

            <div className="file-div">
                    {data.map((film) => (
                        <p key={film.id}>
                            {film.similarity_score}%: - {film.title} ({film.year}) {film.genres}
                        </p>
                    ))}
            </div>
        </>
    );
}

export default App;
