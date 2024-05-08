import './App.css';
import background from "./social-network-2.jpeg"

const App = () => {
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
        <h1>RECS PAGE</h1>
        <h3>A film recommendation app.</h3>
        <h3>Upload your <a href="https://www.wikihow.com/Export-Your-IMDb-Custom-Lists-to-a-CSV-File"><u>exported
          ratings</u></a> from your IMDB account.</h3>
      </div>

      <div className="file-div">

      </div>
    </>
  );
}

export default App;
