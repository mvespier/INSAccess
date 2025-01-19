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
      if (string == "1815"){
        return result;
      }
    }
    currentHour += 1;
    currentMinute = 0;
  }
  return result;
}

async function fetchData(){
  const response = await fetch('../static/data.json');
  const result = await response.json();
  return result;
}

function SingleEvent({start_time, end_time, label, color}){
  let start_index = hours_events.indexOf(start_time)+1;
  let end_index = hours_events.indexOf(end_time)+1;
  const hours_events = createHours();

  const eventStyle = {
    gridRowStart: start_index, 
    gridRowEnd: end_index
  };

  return (
    <div className={`event ${color}`} style={eventStyle}>
      <p className="title">{label}</p>
      <p className="time">{hours_events[start_index-1]} - {hours_events[end_index-1]}</p>
    </div>
  );
}

async function AllEvents(){
  const events_list = [];
  const data = await fetchData()

  let i = 0;
  for (let element in data.monday){
    console.log(element.label)
    events_list.push(<SingleEvent key={i} start_time={element.start_time} end_time={element.end_time} label={element.label} color={Color.DefaultColor} />);
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
    <>
        {hours}
    </>
  );
}

ReactDOM.createRoot(document.getElementById('eventsMon')).render(<AllEvents />);

ReactDOM.createRoot(document.getElementById('hours')).render(<TimeBar />);
