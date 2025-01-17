import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {AllEvents, TimeBar} from './eventManager';


ReactDOM.createRoot(document.getElementById('root')).render(<App />);

ReactDOM.createRoot(document.getElementById('events-mon')).render(<AllEvents />);

ReactDOM.createRoot(document.getElementById('hours')).render(<TimeBar />);