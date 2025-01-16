const hours_start = ["8h00", "9h45", "11h30", "13h15", "15h00", "16h45"]
const hours_end = ["9h30", "11h15", "13h", "14h45", "16h30", "18h15"]

function SingleEvent({start, end, label}){
  return (
    <div className={`event start-${start} end-${end} securities`}>
      <p className="title">{label}</p>
      <p className="time">{hours_start[start]} - {hours_end[end-1]}</p>
    </div>
  );
}

function AllEvents(){
    return (
      <>
        <SingleEvent start={0} end={1} label={"PROGRAV"} />
        <SingleEvent start={1} end={3} label={"AUTO"} />
      </>
    );
}

function TimeBar(){
  const hours = [];
  hours.push(<div key={-1} className="spacer"></div>);
  for (let i = 0; i < hours_start.length; i++){
    hours.push(<div key={i} className="time-marker">{hours_start[i]}</div>)
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