import './App.css';
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import background from "./social-network-1.jpg"
// import '@fortawesome/fontawesome-free/css/all.css'; // works on windows if this is commented out
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileImport } from '@fortawesome/free-solid-svg-icons';
import { faFileUpload } from '@fortawesome/free-solid-svg-icons';

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [errorText, setErrorText] = useState("");
  const [fileName, setFileName] = useState("");
  const navigate = useNavigate();

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
    setFileName("Selected File: " + event.target.files[0].name); // Update fileName state
    setErrorText(""); // Reset error text when a new file is selected
  };

  const handleFileUpload = async () => {
    if (selectedFile) {
      let fileExtension = selectedFile.name.split('.').pop();
      if (fileExtension === "csv") {
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
          const response = await fetch('/verifyUserUploadedFile', {
            method: 'POST',
            body: formData
          });

          if (response.ok) {
            navigate('/recs');  // go to next page
          } else {
            setErrorText(await response.text()); // Update errorText state
          }
        } catch (error) {
          setErrorText(error.message); // Update errorText state
        }
      } else {
        setErrorText("File must be .csv"); // Update errorText state
      }
    } else {
      setErrorText("You must select a file first"); // Update errorText state
    }
  };

  const backgroundStyle = {
    backgroundImage: `url(${background})`,
    height: '100vh',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    backgroundSize: 'cover'
  }

  return (
    <>
      <div style={backgroundStyle}></div>
      <div className="title">
        <h1>FILM REC</h1>
        <h3>A film recommendation app.</h3>
        <h3>Letterboxd users: Upload the <a
            href="https://letterboxd.com/data/export"><u>ratings.csv</u></a> file.</h3>
        <h3>IMDB Users: Upload your <a href="https://www.wikihow.com/Export-Your-IMDb-Custom-Lists-to-a-CSV-File"><u>exported
          ratings</u></a> csv file.</h3>
      </div>

      <div className="file-div">
        <label htmlFor="select-file" className="file-button">
          <FontAwesomeIcon icon={faFileImport} className="select-file-icon" /> Select
          <input id="select-file" type="file" onChange={handleFileSelect} />
        </label>

        <p className="file-text">{fileName}</p>

        <button className="file-button" onClick={handleFileUpload}>
          <FontAwesomeIcon icon={faFileUpload} className="select-file-icon" /> Upload
        </button>

        <p className="file-text">{errorText}</p>
      </div>
    </>
  );
}

export default App;
