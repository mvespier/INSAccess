import '../css/App.css';
import eventUtils from './eventUtils.js';
import menu from './menu.js'

function App() {
  return (
    <div className="App">
      <menu.Menu items={menu.items}/>
      <eventUtils.Calendar />
    </div>
  );
}

export default App;
