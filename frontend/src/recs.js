import './App.css';
import background from "./social-network-2.jpeg"

const App = async () => {

    const response = await fetch('/rec');
    const recs = response.json();
    recs.forEach(rec => {
       console.log(rec);
    });

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
            </div>
        </>
    );
}

export default App;
