import data from '../data.json'
import dateUtils from '../js/dateUtils.js'

/* eslint-disable-next-line react/prop-types */
function SingleEvent({start_time, end_time, label, teacher, room}){
  const hours_events = dateUtils.createHours();
  let start_index = hours_events.indexOf(start_time);
  let end_index = hours_events.indexOf(end_time);
  let eventHeight = dateUtils.getEventSize(start_index, end_index, hours_events.length);
  let eventPosY = dateUtils.getEventPos(start_index, hours_events.length);

  const eventStyle = {
    height: `${eventHeight}%`,
    position: "absolute",
    top: `${eventPosY}%`,
    width: "93%",
    background: "rgb(140, 201, 252)"//"linear-gradient(70deg,rgb(140, 201, 252), #ffb7ef)"
   
  };

  return (
    <div className="event" style={eventStyle}>
      <p className="title">{label}</p>
      <p className="room">{room}</p>
      <p className="teacher">{teacher}</p>
      </div>
  );
}   

function getEventsOfDay(date){
  const events = []
  data.forEach(ev => {
    if (ev.date === date) {
      events.push(ev)
    }
  })
    return events;
}

function EventsOfDay(date){
  const events_list = [];
  
  let i = 0;
  const events_of_day = getEventsOfDay(date.date, data)
  const infos = dateUtils.getDateInfo(date.date, data)

  for (let element in events_of_day){
    const object = events_of_day[element]
    events_list.push(
      <SingleEvent key={i} start_time={object.start_time} end_time={object.end_time} label={object.label} teacher={object.teacher} room={object.room} />
    );
    i += 1;
  } 


  return (
    <div className="day">
      <div className="date">
        <p className="date-day">{infos[0]}</p>
        <p className="date-num">{infos[1]}</p> 
      </div>
      <div className="events">
        {events_list}
      </div>
    </div>
  );
}

function TimeBar(){
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

function Calendar(){
  return (
    <div className="calendar">
      <TimeBar />
      <div className="days">
        <EventsOfDay date="20250120"/>
        <EventsOfDay date="20250121"/>
        <EventsOfDay date="20250122"/>
        <EventsOfDay date="20250123"/>
        <EventsOfDay date="20250124"/>
      </div>
  </div>
      
  );
}

export default Calendar;