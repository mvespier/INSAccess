import { useAuth } from "../contexts/AuthContext";
import constants from '../js/constants.js'
import { Error, Loading } from './templates.js'

const API_URL = constants.API_URL;

const ProtectedRoute = ({ children }) => {
    const { token, loading, error } = useAuth();

    const url_login = API_URL+"/login"


    if (loading) {
        return <Loading />
    } else if (!token){
        window.location.replace(url_login)
    }

    if (token){
        return children;
    }

    if (error){
        window.location.replace(url_login)

        return <Error message={error}/>
    }
};

export default ProtectedRoute;
