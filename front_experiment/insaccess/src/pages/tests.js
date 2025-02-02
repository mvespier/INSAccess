import { useMediaQuery } from 'react-responsive'

function Home(){
    const isMobile = useMediaQuery({ maxWidth: 850 });

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