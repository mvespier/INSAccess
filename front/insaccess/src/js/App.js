import logo from '../logo.svg';
import '../css/App.css';
import utils from './utils.js';
import menu from './menu.js'

function App() {
  return (
    <div className="App">
      <menu.Menu items={menu.items}/>
      <utils.Calendar />
    </div>
  );
}

export default App;
