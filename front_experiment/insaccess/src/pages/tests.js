import { useMediaQuery } from 'react-responsive'
import data from '../data.json'
import { DataContainer } from '../js/randomUtils';

function Home(){
    const isMobile = useMediaQuery({ maxWidth: 850 });
    console.log(data)
    let data_obj = new DataContainer(data)
    console.log(data_obj)
    console.log(data_obj.data)
    console.log(typeof(data))
    console.log(typeof(data_obj))

    return (
        <div>
            <div>Page test</div>
            <div>
                {!isMobile && <p>You are on a desktop or laptop device.</p>}
                {isMobile && <p>You are on a mobile device.</p>}
            </div>
        </div>
    )
}

export default Home;