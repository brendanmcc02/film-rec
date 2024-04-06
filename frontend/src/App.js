import './App.css';
import React, { Component } from "react";
import background from "./social-network.jpg"
import '@fortawesome/fontawesome-free/css/all.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileImport } from '@fortawesome/free-solid-svg-icons';
import { faFileUpload } from '@fortawesome/free-solid-svg-icons';

class App extends Component {
    state = {
        // Initially, no file is selected
        selectedFile: null,
    };

    // On file select (from the pop-up)
    onFileChange = (event) => {
        // Update the state
        this.setState({
            selectedFile: event.target.files[0],
        });
    };

    // On file upload (click the upload button)
    onFileUpload = () => {
        // Create an object of formData
        const formData = new FormData();

        // Update the formData object
        formData.append(
            "myFile",
            this.state.selectedFile,
            this.state.selectedFile.name
        );
    };

    render() {
        const backgroundStyle = {
            backgroundImage: `url(${background})`,
            height: '100vh',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'cover'
        }

        // fetch("/startup").then((res) => console.log(res.text()))



        return (
          <>
              <div style={backgroundStyle}></div>
              <div className="title">
                  <h1>FILM REC</h1>
                  <h3>A film recommendation algorithm.</h3>
                  <h3>Upload your exported ratings.csv (keep filename the same) from your IMDB account.</h3>
                  <h3><a href="https://www.wikihow.com/Export-Your-IMDb-Custom-Lists-to-a-CSV-File"><u>
                      How do I export my IMDb ratings?
                  </u></a></h3>

              </div>

              <div className="file-div">
                  <label htmlFor="select-file" className="file-button">
                      <FontAwesomeIcon icon={faFileImport} className="select-file-icon"/> Select ratings.csv
                      <input id="select-file" type="file" onChange={this.onFileChange}/>
                  </label>


                  <br/><br/><br/>

                  <button className="file-button" onClick={this.onFileUpload}>
                      <FontAwesomeIcon icon={faFileUpload} className="select-file-icon"/> Upload
                  </button>
              </div>
          </>
        );
    }
}

export default App;
