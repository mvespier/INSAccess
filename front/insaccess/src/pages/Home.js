import Day from '../js/dateUtils.js'

function Home(){
    let day = new Day("2025-01-31")
    return (
        <div>
            <div>{day.next(7).date}</div>
            <div>{day.prev(7).date}</div>
            <div>{day.getDayOfWeek()}</div>
        </div>
    )
}

export default Home;