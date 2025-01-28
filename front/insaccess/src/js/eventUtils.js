import Day from './dateUtils.js'
import PropTypes from 'prop-types';
import constantes from './constantes.js'
import {NavLink} from 'react-router-dom'

const getEventSize = (start_index, end_index, nb_div) => {
  return ((end_index-start_index)/(nb_div+1))*100
}

const getEventPos = (start_index, nb_div) => {
  return 100*(start_index+1)/(nb_div+1);
}

const SingleEvent = (props) => {
  const hours_events = Day.createHours();
  let start_index = hours_events.indexOf(props.start_time);
  let end_index = hours_events.indexOf(props.end_time);
  let eventHeight = getEventSize(start_index, end_index, hours_events.length);
  let eventPosY = getEventPos(start_index, hours_events.length);

  const eventStyle = {
    height: `${eventHeight}%`,
    top: `${eventPosY}%`,
    userSelect: "none"
  };

  return (
    <NavLink to={props.link}>
      <button type="button" className="event" style={eventStyle}>
        <p className="title">{props.label}</p>
        <p className="room">{props.room}</p>
        <p className="teacher">{props.teacher}</p>
      </button>
    </NavLink>
  );
}   

const TimeBar = () => {
  const hours = [];
  hours.push(<div key={-1} className="spacer"></div>);
  for (let i = 0; i < constantes.hours_timeline.length; i++){
    hours.push(<div key={i} className="time-marker">{constantes.hours_timeline[i]}</div>)
  }
  return (
    <div className="timeline">
        {hours}
    </div>
  );
}

SingleEvent.propTypes = {
  start_time: PropTypes.string.isRequired, 
  end_time: PropTypes.string.isRequired, 
  label: PropTypes.string.isRequired, 
  teacher: PropTypes.string.isRequired, 
  room: PropTypes.string.isRequired,
  link: PropTypes.string.isRequired
}

export default { TimeBar, SingleEvent };