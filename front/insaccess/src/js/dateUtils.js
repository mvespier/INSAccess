const hours_timeline = ["8h00", "9h45", "11h30", "13h15", "15h00", "16h45", "18h15"];

function createHours(){
    let result = [];
    //result.push("0755");
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

function getDateInfo(date){
    const dayList = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    const year = parseInt(date.slice(0, 4))
    const month = parseInt(date.slice(4, 6))
    const day = parseInt(date.slice(6, 8))
    const date_object = new Date(year, month-1, day)
    return [dayList[date_object.getDay()-1], date_object.getDate()]
  
}

function getEventSize(start_index, end_index, nb_div){
  return ((end_index-start_index)/(nb_div+1))*100
}

function getEventPos(start_index, nb_div){
  return 100*(start_index+1)/(nb_div+1);
}

export default { getDateInfo, presentableHour, createHours, hours_timeline, getEventSize, getEventPos };