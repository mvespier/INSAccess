const hours_start = ["8h00", "8h30", "9h00", "9h45", "10h15", "10h45", "11h30", "12h00", "12h30", "13h15", "13h45", "14h15", "15h00", "15h30", "16h00", "16h45", "17h15", "17h45"]
const hours_end = ["8h15", "8h45", "9h30", "10h00", "10h30", "11h15", "11h45", "12h15", "13h00", "13h30", "14h00", "14h45", "15h15", "15h45", "16h30", "17h00", "17h30", "18h15"]
const hours_timeline = ["8h00", "9h45", "11h30", "13h15", "15h00", "16h45", "18h15"]

function SingleEvent({start_time, end_time, label, color}){
  let start_index = hours_start.indexOf(start_time)+1;
  let end_index = hours_end.indexOf(end_time)+2;

  const eventStyle = {
    gridRowStart: start_index, 
    gridRowEnd: end_index
  };

  return (
    <div className={`event ${color}`} style={eventStyle}>
      <p className="title">{label}</p>
      <p className="time">{hours_start[start_index]} - {hours_end[end_index]}</p>
    </div>
  );
}

function AllEvents(){
    return (
      <>
        <SingleEvent start_time={"8h00"} end_time={"9h30"} label={"PROGRAV"} color={"colRed"} />
        <SingleEvent start_time={"9h45"} end_time={"13h00"} label={"AUTO"} color={"colBlue"}/>
      </>
    );
}

function TimeBar(){
  const hours = [];
  hours.push(<div key={-1} className="spacer"></div>);
  for (let i = 0; i < hours_start.length; i++){
    hours.push(<div key={i} className="time-marker">{hours_timeline[i]}</div>)
  }
  return (
    <>
        {hours}
    </>
  );
}

const events1 = document.getElementById('events-mon');
const rootEvents1 = ReactDOM.createRoot(events1);
rootEvents1.render(<AllEvents />);

const time_bar = document.getElementById('hours');
const rootTimeBar = ReactDOM.createRoot(time_bar);
rootTimeBar.render(<TimeBar />);