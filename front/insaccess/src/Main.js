import { Routes, Route } from 'react-router-dom';

import Home from './pages/Home';
import Calendar from './pages/calendar.js';
import Signup from './pages/signup.js';
import About from './pages/about.js';
import Associations from './pages/associations.js';

const Main = () => {
  return (
    <Routes> 
      <Route exact path='' element={<Home />}></Route >
      <Route exact path='/signup' element={<Signup />}></Route>
      <Route exact path='/calendar' element={<Calendar start={Date.now()}/>}></Route>
      <Route exact path='/about' element={<About />}></Route>
      <Route exact path='/associations' element={<Associations start={Date.now()}/>}></Route>
    </Routes>
  );
}

export default Main;