import './App.css';
import React, { Component } from "react";
import background from "./social-network.jpg"

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

        return (
          <>
              <div style={backgroundStyle}></div>
              <div className="title">
                  <h1>FILM REC</h1>
                  <h3>A film recommendation algorithm.</h3>
                  <h3>Upload your exported ratings.csv from your IMDB account.</h3>
                  <br/>
                  <a>How do I export my IMDb ratings?</a>
              </div>

              <div className="fileUpload">
                  <input id="uploadButton" type="file" onChange={this.onFileChange} />

                  {/*<button onClick={this.onFileUpload}>Upload</button>*/}
              </div>
          </>
        );
    }
}

export default App;
