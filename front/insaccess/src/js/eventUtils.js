import dateUtils from './dateUtils.js'
import PropTypes from 'prop-types';

const SingleEvent = (props) => {
  const hours_events = dateUtils.createHours();
  let start_index = hours_events.indexOf(props.start_time);
  let end_index = hours_events.indexOf(props.end_time);
  let eventHeight = dateUtils.getEventSize(start_index, end_index, hours_events.length);
  let eventPosY = dateUtils.getEventPos(start_index, hours_events.length);

  const eventStyle = {
    height: `${eventHeight}%`,
    top: `${eventPosY}%`,
  };

  return (
    <div className="event" style={eventStyle}>
      <p className="title">{props.label}</p>
      <p className="room">{props.room}</p>
      <p className="teacher">{props.teacher}</p>
      </div>
  );
}   

const TimeBar = () => {
  const hours = [];
  hours.push(<div key={-1} className="spacer"></div>);
  for (let i = 0; i < dateUtils.hours_timeline.length; i++){
    hours.push(<div key={i} className="time-marker">{dateUtils.hours_timeline[i]}</div>)
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
  room: PropTypes.string.isRequired
}

export default { TimeBar, SingleEvent };