import React from 'react';
import './App.css';
import Footer from './Footer';

class App extends React.Component {
  render() {
    return (
      <div>
        <header>
          <p>
            Edit <code>src/App.js</code> and save to reload.
        </p>
          <a
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
        </a>
        </header>
        <Logo/>
        <Navbar/>
        <Footer />
      </div>
    );
  }
}

export default App;
