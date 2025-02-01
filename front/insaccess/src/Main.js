import { Routes, Route } from 'react-router-dom';

import Home from './pages/Home';
import Calendar from './pages/calendar.js';
import Signup from './pages/signup.js';
import About from './pages/about.js';
import Associations from './pages/associations.js';
import Day from './js/dateUtils.js'

const Main = () => {
  let first_day = new Day("2025-01-31");
  
  return (
    <Routes> 
      <Route exact path='' element={<Home />}></Route >
      <Route exact path='/signup' element={<Signup />}></Route>
      <Route exact path='/calendar' element={<Calendar start={first_day.startOfWeek().getDate()}/>}></Route>
      <Route exact path='/about' element={<About />}></Route>
      <Route exact path='/associations' element={<Associations start={first_day.startOfWeek().getDate()}/>}></Route>
    </Routes>
  );
}

export default Main;