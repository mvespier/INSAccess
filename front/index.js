const hours_events = ["8h00", "8h05", "8h10", "8h15", "8h20", "8h25", "8h30", "8h35", "8h40", "8h45", "8h50", "8h55", 
                      "9h00", "9h05", "9h10", "9h15", "9h20", "9h25", "9h30", "9h35", "9h40", "9h45", "9h50", "9h55", 
                      "10h00", "10h05", "10h10", "10h15", "10h20", "10h25", "10h30", "10h35", "10h40", "10h45", "10h50", "10h55", 
                      "11h00", "11h05", "11h10", "11h15", "11h20", "11h25", "11h30", "11h35", "11h40", "11h45", "11h50", "11h55", 
                      "12h00", "12h05", "12h10", "12h15", "12h20", "12h25", "12h30", "12h35", "12h40", "12h45", "12h50", "12h55", 
                      "13h00", "13h05", "13h10", "13h15", "13h20", "13h25", "13h30", "13h35", "13h40", "13h45", "13h50", "13h55", 
                      "14h00", "14h05", "14h10", "14h15", "14h20", "14h25", "14h30", "14h35", "14h40", "14h45", "14h50", "14h55", 
                      "15h00", "15h05", "15h10", "15h15", "15h20", "15h25", "15h30", "15h35", "15h40", "15h45", "15h50", "15h55", 
                      "16h00", "16h05", "16h10", "16h15", "16h20", "16h25", "16h30", "16h35", "16h40", "16h45", "16h50", "16h55",  
                      "17h00", "17h05", "17h10", "17h15", "17h20", "17h25", "17h30", "17h35", "17h40", "17h45", "17h50", "17h55",
                      "18h00", "18h05", "18h10", "18h15" 
                    ]

const hours_timeline = ["8h00", "9h45", "11h30", "13h15", "15h00", "16h45", "18h15"]

const Color = {
  Blue: "colBlue",
  Red: "colRed",
  Green: "colGreen",
  Yellow: "colYellow"
};


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
    return (
      <>
        <SingleEvent start_time={"8h00"} end_time={"9h30"} label={"PROGRAV"} color={Color.Red} />
        <SingleEvent start_time={"9h45"} end_time={"13h00"} label={"AUTO"} color={Color.Yellow}/>
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

const events1 = document.getElementById('events-mon');
const rootEvents1 = ReactDOM.createRoot(events1);
rootEvents1.render(<AllEvents />);

const time_bar = document.getElementById('hours');
const rootTimeBar = ReactDOM.createRoot(time_bar);
rootTimeBar.render(<TimeBar />);