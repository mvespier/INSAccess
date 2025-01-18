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

let hours_events = createHours();
let data;
let data_file = document.currentScript.getAttribute('data_json')

fetch(data_file)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error fetching JSON:', error));

function SingleEvent({start_time, end_time, label, color}){
  let start_index = hours_events.indexOf(start_time)+1;
  let end_index = hours_events.indexOf(end_time)+1;

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

function AllEvents(){
  const events_list = [];
  for (element in data.monday){
    events_list.push(<SingleEvent start_time={element.start_time} end_time={end_time} label={element.label} color={Color.DefaultColor} />);
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

ReactDOM.createRoot(document.getElementById('events-mon')).render(<AllEvents />);

ReactDOM.createRoot(document.getElementById('hours')).render(<TimeBar />);
