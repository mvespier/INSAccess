import data from '../data_asso.json'
import utils from '../js/eventUtils.js'
import dateUtils from '../js/dateUtils.js'

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
      <utils.SingleEvent key={i} start_time={object.start_time} end_time={object.end_time} label={object.label} teacher={object.teacher} room={object.room} />
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

const Associations = () => {
  return (
    <div className="calendar">
      <utils.TimeBar />
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

export default Associations;