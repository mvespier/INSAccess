const hours_start = ["8h", "9h45", "11h30", "13h15", "15h", "16h45"]
const hours_end = ["9h30", "11h15", "13h", "14h45", "16h30", "18h15"]

function SingleEvent({start, end, label}){
  return (
    <div className={`event start-${start+1} end-${end+1} securities`}>
      <p className="title">{label}</p>
      <p className="time">{hours_start[start]} - {hours_end[end-1]}</p>
    </div>
  );
}

function AllEvents(){
    return (
      <>
        <SingleEvent start={0} end={1} label={"PROGRAV"} />
        <SingleEvent start={2} end={3} label={"AUTO"} />
      </>
    );
}


const node = document.getElementById('events-mon');
const root = ReactDOM.createRoot(node);
root.render(<AllEvents />);