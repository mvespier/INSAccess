import './css/App.css';
import NavBar from './js/navbar.js'
import { AuthProvider } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import { Routes, Route } from 'react-router-dom';
import Settings from './components/settings.js';
import Calendar from './components/calendar.js';
import About from './components/about.js';
import Day from './js/dateUtils.js';
import minWidth from './js/constants.js';
import { useWindowDimensions } from './js/randomUtils.js';

function App() {

  const current_date = new Date()
  let first_day = new Day(current_date)
  let dimensions = useWindowDimensions();

  const data = 'http://localhost:3000/api/get_year/'+first_day.getDate();
  const data_asso = 'http://localhost:3000/data_asso.json'

  let day = (minWidth < dimensions.width) ? first_day.getDate() : first_day.startOfWeek().getDate()
  
  return (
    <div className="App">
      <NavBar.NavBar items={NavBar.items}/>
      <AuthProvider>
          <Routes> 
            <Route exact path='' element={<ProtectedRoute><Calendar start={day} data_path={data}/></ProtectedRoute>}></Route >
            <Route exact path='/about' element={<ProtectedRoute><About /></ProtectedRoute>}></Route>
            <Route exact path='/settings' element={<ProtectedRoute><Settings /></ProtectedRoute>}></Route>
            <Route exact path='/associations' element={<ProtectedRoute><Calendar start={day} data_path={data_asso}/></ProtectedRoute>}></Route>
          </Routes>
      </AuthProvider>
    </div>
  );
}

export default App;
