import coincoin from '../images/coincoin.png'
import coincoin2 from '../images/coincoin2.png'

const Card = ({title, img_src, content, column, link}) => {
    const styleCard = {
        "width": "18rem", 
        "gridColumn":column, 
        "justifySelf":"center",
        "padding":"2vh"
    }

    const styleButton = {
        "position":"absolute",
        "bottom":"0",
        "right":"0",
        "padding":"3vh"
    }

    return (
        <div className="card" style={styleCard}>
            <img src={img_src} className="card-img-top" alt="image_not_found"></img>
            <div className="card-body">
                <h5 className="card-title">{title}</h5>
                <p className="card-text">{content}</p>
                <div style={styleButton} >
                    <a href={link} target="_blank" rel="noreferrer noopener" className="btn btn-primary">This guy&apos;s github</a>
                </div>
            </div>
        </div>
    )
}

const Home = () => {
    const styleCard = {
        "display":"grid",
        "gridTemplateColumns":"repeat(auto, 1fr)",
        "margin":"3vh",
        "height":"100%"
    }
    return (
        <div style={styleCard}>
            <Card title="Raph" img_src={coincoin} content="Programmeur de génie" column={1} link="https://github.com/ImJustCookie"/>
            <Card title="Jules" img_src={coincoin2} content="Programmeur de génie (mais plus petit)" column={2} link="https://github.com/Onniryss"/>
        </div>
    )
}

export default Home;