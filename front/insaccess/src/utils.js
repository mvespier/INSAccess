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

function SingleEvent({start_time, end_time, label, color}){
  const hours_events = createHours();
  let start_index = hours_events.indexOf(start_time)+1;
  let end_index = hours_events.indexOf(end_time)+1;

  //console.log(start_time, end_time)

  const eventStyle = {
    gridRowStart: start_index, 
    gridRowEnd: end_index
  };

  return (
    <div className={`event ${color}`} style={eventStyle}>
      <p className="title">{label}</p>
      <p className="time">{presentableHour(hours_events[start_index-1])} - {presentableHour(hours_events[end_index-1])}</p>
    </div>
  );
}

function EventsOfDay(day){
  const events_list = [];

  let i = 0;
  for (let element in data.monday){
    console.log(element)
    events_list.push(<SingleEvent key={i} start_time={data.monday[element].start_time} end_time={data.monday[element].end_time} label={data.monday[element].label} color={Color.DefaultColor} />);
    i += 1;
  } 
    return (
      <>
        {events_list}        
      </>
    );
}

function TimeBar(){
  const hours = [];
  hours.push(<div key={-1} className="spacer"></div>);
  for (let i = 0; i < hours_timeline.length; i++){
    hours.push(<div key={i} className="time-marker">{hours_timeline[i]}</div>)
  }
  return (
    <div>
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
          <div className="day mon">
            <div className="date">
                <p className="date-num">9</p>
                <p className="date-day">Mon</p>
            </div>
            <div className="events">
              <EventsOfDay day="monday" />
            </div>
          </div>
          
          <div className="day tues">
            <div className="date">
                <p className="date-num">10</p>
                <p className="date-day">Tues</p>
            </div>
            <div className="events">
            </div>
          </div>

          <div className="day wed">
            <div className="date">
                <p className="date-num">11</p>
                <p className="date-day">Wed</p>
            </div>
            <div className="events">
            </div>
          </div>

          <div className="day thurs">
            <div className="date">
                <p className="date-num">12</p>
                <p className="date-day">Thurs</p>
            </div>
            <div className="events">
            </div>
          </div>

          <div className="day fri">
            <div className="date">
                <p className="date-num">13</p>
                <p className="date-day">Fri</p>
            </div>
            <div className="events">
            </div>
          </div>

      </div>
  </div>
      
  );
}

export default { Calendar, NavBar }