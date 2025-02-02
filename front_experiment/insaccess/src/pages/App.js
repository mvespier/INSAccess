import '../css/App.css';
import Main from '../Main.js'
import NavBar from '../js/navbar.js'

function App() {
  return (
    <div className="App">
      <NavBar.NavBar items={NavBar.items}/>
      <Main />
    </div>
  );
}

export default App;
