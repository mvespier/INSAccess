import { Routes, Route } from 'react-router-dom';

import Tests from './pages/tests.js';
import Calendar from './pages/calendar.js';
import Signup from './pages/signup.js';
import About from './pages/about.js';
import Day from './js/dateUtils.js'
import minWidth from './js/constants.js'
import { useWindowDimensions } from './js/randomUtils.js'

const Main = () => {
  const current_date = new Date()
  let first_day = new Day(current_date)
  let dimensions = useWindowDimensions();

  const data = 'http://localhost:3000/api/get_year/'+first_day.getDate();
  const data_asso = 'http://localhost:3000/data_asso.json'

  let day = (minWidth < dimensions.width) ? first_day.getDate() : first_day.startOfWeek().getDate()
  
  return (
    <Routes> 
      <Route exact path='' element={<Calendar start={day} data_path={data}/>}></Route >
      <Route exact path='/settings' element={<Signup />}></Route>
      <Route exact path='/about' element={<About />}></Route>
      <Route exact path='/tests' element={<Tests />}></Route>
      <Route exact path='/associations' element={<Calendar start={day} data_path={data_asso}/>}></Route>
    </Routes>
  );
}

export default Main;