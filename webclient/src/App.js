import React from 'react';
import Modal from 'react-modal';
//import logo from './logo.svg';
import './App.css';
import './css/HomeView.css';
import {HomeViewContainer} from './components/HomeViewContainer';

Modal.setAppElement('#root')

function App() {
  return (
    <div className="App" id = "app">
      <HomeViewContainer/>
    </div>
  );
}

export default App;
