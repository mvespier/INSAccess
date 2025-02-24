import { Routes, Route } from 'react-router-dom';

import Tests from './pages/tests.js';
import Calendar from './pages/calendar.js';
import Signup from './pages/signup.js';
import About from './pages/about.js';
import Day from './js/dateUtils.js'
import minWidth from './js/constants.js'
import { useWindowDimensions } from './js/randomUtils.js'

const Main = () => {
  let first_day = new Day("2025-02-03");
  let dimensions = useWindowDimensions();

  const data = '/api/get_week/2025-02-24'//'http://localhost:3000/api/get_week/2025-02-03'
  const data_asso = 'http://localhost:3000/data_asso.json'//'http://localhost:3000/api/get_week/2025-02-03'

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