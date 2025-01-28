import constantes from './constantes.js'

const Day = class Day{
  
  constructor(date){
    this.date = date || Date.now();
    this.day = this.date.getDay();
    this.month = this.date.getMonth();
    this.year = this.date.getYear();
  }

  set setDay(date){
    this.date = date;
  }

  static nextDay(day){
    let newDay = day.copy();
    newDay.date.setDate(newDay.getDate()+1);
    return newDay;
  }
  
  static prevDay(day){
    let newDay = day.copy();
    newDay.date.setDate(newDay.getDate()+1);
    return newDay;
  }

  copy(){
    let res = new Day(this.date);
    return res;
  }

  startOfWeek(){
    //let current_day = this.getDate();
  }
    
  static presentableHour(hour){
    return hour[0]+hour[1]+":"+hour[2]+hour[3]
  }

  get getDay(){
    return this.day;
  }

  get getMonth(){
    return this.month;
  }

  get getYear(){
    return this.year;
  }

  get getDate(){
    return this.date.getDate();
  }

  set setDate(day){
    this.date.setDate(day.getDate());
  }
  
  getDateInfo(){
      return [constantes.dayList[this.getDay()], this.getDate()];
  }

  toString(){
    return ""+this.getYear()+this.getMonth()+this.getDate()
  }

  static createHours(){
    let result = [];
    let string = "";
    let last_hour = "2015"
    let currentHour = 8;
    let currentMinute = 0;
    for (let i = 0; i <= 12; i++){
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
        if (string === last_hour){
          return result;
        }
      }
      currentHour += 1;
      currentMinute = 0;
    }
    return result;
  }
  
  // nextDay.propTypes = PropTypes.string.isRequired;
  // prevDay.propTypes = PropTypes.string.isRequired;
} 





export default { Day };