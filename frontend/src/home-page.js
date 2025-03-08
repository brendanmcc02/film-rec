import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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
    setFileName("Selected File: " + event.target.files[0].name);
    setErrorText(""); // Reset error text when a new file is selected
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('https://film-rec-backend.onrender.com/verifyUserUploadedFile', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        navigate('/recommendations-page');
      } else {
        setErrorText(await response.text());
      }
    } catch (error) {
      setErrorText(error.message);
    }
  };

  return (
    <>
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
          Please wait around 1-2 minutes, and then refresh the page and try again.
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
    </>
  );
}

export default App;
