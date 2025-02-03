import AllEvents from '../js/eventUtils.js'

const Calendar = (props) => {
  return (
    <AllEvents start={props.start} data_path={props.data_path}/>
  )
}

export default Calendar;