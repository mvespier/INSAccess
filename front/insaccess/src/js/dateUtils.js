import constantes from './constantes.js'

const Day = class Day{

  date = new Date();
  
  constructor(date_object){
    console.log(date_object)
    this.date = date_object;
    this.day = date_object.getDay();
    this.month = date_object.getMonth();
    this.year = date_object.getYear();
  }

  setDay(date){
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

  getDay(){
    return this.day;
  }

  getMonth(){
    return this.month;
  }

  getYear(){
    return this.year;
  }

  getDate(){
    return this.date.getDate();
  }

  getDateObject(){
    return new Date(this.date);
  }

  setDate(day){
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





export default Day;