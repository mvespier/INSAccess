import data from '../data.json'
import utils from '../js/eventUtils.js'
import Day from '../js/dateUtils.js'
import useWindowDimensions from '../js/randomUtils.js'
import constantes from '../js/constants.js'
import { useState } from 'react'

const getEventsOfDay = (date, data) => {
  const events = []
  data.forEach(ev => {
    if (ev.date === date) {
      events.push(ev)
    }
  })
    return events;
}

const EventsOfDay = (props) => {
  const events_list = [];
  
  let i = 0;
  const events_of_day = getEventsOfDay(props.date, data);
  let day = new Day(props.date);
  const infos = day.getDateInfo();

  for (let element in events_of_day){
    const object = events_of_day[element]
    events_list.push(
      <utils.SingleEvent key={i} start_time={object.start_time} end_time={object.end_time} label={object.label} teacher={object.teacher} room={object.room} link={object.link} />
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

const Calendar = (props) => {
  let day = new Day(props.start);
  const [first_day, setDay] = useState(day);

  function handleDay(direction, value){
    if (direction === "prev"){
      setDay(first_day => first_day.prev(value))
    } else if (direction === "next"){
      setDay(first_day => first_day.next(value))
    }
  }
  
  let list_days = []
  let dimensions = useWindowDimensions()
  let minWidth = constantes.minWidth;
  let nb_days =  ((minWidth < dimensions.width) ? 5 : 1);
  let current_day = first_day.copy();

  for (let i = 0; i < nb_days; i++){
    list_days.push(<EventsOfDay key={i} date={ current_day.getDate() }/>);
    current_day = current_day.next(1);
  }

  //let skipDays = (nb_days == 1) ? 1 : 7;

  return (
    <div className="calendar">
      <button type="button" className="arrow-left" onClick={() => {handleDay("prev", 7)}}></button>
      <utils.TimeBar />
      <div className="days">
        {list_days}
      </div>
      <button type="button" className="arrow-right turned" onClick={() => {handleDay("next", 7)}}></button>
  </div>
      
  );
}

export default Calendar;