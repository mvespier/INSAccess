//import { useMediaQuery } from 'react-responsive'
import { LoadData, TDSelection } from '../js/randomUtils.js'
import { useEffect, useState } from 'react';

const Settings = () => {

    let {data, error, loading} = LoadData("/api/get_tds");
    let [user_tds, setUserTD] = useState(null);
    let [all_tds, setAllTD] = useState(null);

    useEffect(() => {
        if (data){
            setUserTD(data.user_tds)
            setAllTD(data.all_tds)
        }
    }, [data])

    if (loading) {
        return (
            <div>
                <h1>Settings</h1>
                <div>
                    <p>Chargement des paramètres ...</p>
                </div>
            </div>
        );
    }

    if (error){
        return <div>Erreur lors du fetch</div>
    }

    if (all_tds && user_tds){
        return (
            <div>
                <h1>Settings</h1>
                <TDSelection allTDs={all_tds} userTDs={user_tds} />
            </div>
        );  
    }
}

export default Settings;