import { Routes, Route } from 'react-router-dom';

import Tests from './pages/tests.js';
import Calendar from './pages/calendar.js';
import Signup from './pages/signup.js';
import About from './pages/about.js';
import Associations from './pages/associations.js';
import Day from './js/dateUtils.js'
import minWidth from './js/constants.js'
import useWindowDimensions from './js/randomUtils.js'

const Main = () => {
  let first_day = new Day("2025-02-03");
  let dimensions = useWindowDimensions();
  
  return (
    <Routes> 
      <Route exact path='' element={<Calendar start={(minWidth < dimensions.width) ? first_day.getDate() : first_day.startOfWeek().getDate()}/>}></Route >
      <Route exact path='/settings' element={<Signup />}></Route>
      <Route exact path='/about' element={<About />}></Route>
      <Route exact path='/tests' element={<Tests />}></Route>
      <Route exact path='/associations' element={<Associations start={(minWidth < dimensions.width) ? first_day.getDate() : first_day.startOfWeek().getDate()}/>}></Route>
    </Routes>
  );
}

export default Main;