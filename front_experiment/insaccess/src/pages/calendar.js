import AllEvents from '../js/eventUtils.js'

const Calendar = ({start, data_path}) => {
  return (
    <AllEvents start={start} data_path={data_path}/>
  )
}

export default Calendar;