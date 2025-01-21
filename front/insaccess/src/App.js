import logo from './logo.svg';
import './App.css';
import utils from './js/utils.js';

function App() {
  return (
    <div className="App">
      <utils.NavBar />
      <utils.Calendar />
    </div>
  );
}

export default App;
