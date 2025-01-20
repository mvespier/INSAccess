import data from './data.json'
import React from 'react'

const hours_timeline = ["8h00", "9h45", "11h30", "13h15", "15h00", "16h45", "18h15"];

const Color = {
  Blue: "colBlue",
  Red: "colRed",
  Green: "colGreen",
  Yellow: "colYellow",
  DefaultColor: "colGreen"
};

function createHours(){
  let result = [];
  result.push("0755");
  let string = "";
  let currentHour = 8;
  let currentMinute = 0;
  for (let i = 0; i <= 10; i++){
    for (let j = 0; j < 12; j++){
      string = "";
      if (currentHour < 10){
        string += "0";
      }
      string += `${currentHour}`;
      if (currentMinute < 10){
        string += "0";
      }
      string += `${currentMinute}`;
      result.push(string);
      currentMinute += 5;
      if (string === "1815"){
        return result;
      }
    }
    currentHour += 1;
    currentMinute = 0;
  }
  return result;
}

function presentableHour(hour){
  return hour[0]+hour[1]+":"+hour[2]+hour[3]
}

function SingleEvent({start_time, end_time, label, color, teacher, room}){
  const hours_events = createHours();
  let start_index = hours_events.indexOf(start_time)+1;
  let end_index = hours_events.indexOf(end_time)+1;

  const eventStyle = {
    gridRowStart: start_index, 
    gridRowEnd: end_index
  };

  return (
    <div className={`event ${color}`} style={eventStyle}>
      <p className="title">{label}</p>
      <p className="room">{room}</p>
      <p className="teacher">{teacher}</p>
      <p className="time">{presentableHour(hours_events[start_index-1])} - {presentableHour(hours_events[end_index-1])}</p>
    </div>
  );
}

function getEventsOfDay(date){
  const events = []
  data.forEach(ev => {
    if (ev.date == date) {
      events.push(ev)
    }
  })
    return events;
}

function getDateInfo(date){
  const dayList = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
  const year = parseInt(date.slice(0, 4))
  const month = parseInt(date.slice(4, 6))
  const day = parseInt(date.slice(6, 8))
  const date_object = new Date(year, month-1, day)
  return [dayList[date_object.getDay()-1], date_object.getDate()]

}

function EventsOfDay(date){
  const events_list = [];
  
  let i = 0;
  const events_of_day = getEventsOfDay(date.date)
  const infos = getDateInfo(date.date)

  for (let element in events_of_day){
    const object = events_of_day[element]
    events_list.push(<SingleEvent key={i} start_time={object.start_time} end_time={object.end_time} label={object.label} color={Color.DefaultColor} teacher={object.teacher} room={object.room} />);
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
  for (let i = 0; i < hours_timeline.length; i++){
    hours.push(<div key={i} className="time-marker">{hours_timeline[i]}</div>)
  }
  return (
    <div className="timeline">
        {hours}
    </div>
  );
}

function NavBar(){
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary" id="navbar">
      <div className="container-fluid">
          <a className="navbar-brand" href="#">Navbar</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div className="navbar-nav">
                <a className="nav-link active" aria-current="page" href="#">Home</a>
                <a className="nav-link" href="#">Features</a>
                <a className="nav-link" href="#">Pricing</a>
                <a className="nav-link disabled" aria-disabled="true">Disabled</a>
            </div>
          </div>
      </div>
    </nav>
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

export default { Calendar, NavBar }