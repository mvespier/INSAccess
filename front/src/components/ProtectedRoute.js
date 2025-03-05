import { useAuth } from "../contexts/AuthContext";
import constants from '../js/constants.js'

const API_URL = constants.API_URL;

const ProtectedRoute = ({ children }) => {
    const { token, loading, error } = useAuth();

    const url_login = API_URL+"/login"


    if (loading) {
        return <div>Chargement ...</div>
    } else if (!token){
        window.location.replace(url_login)
    }

    if (token){
        return children;
    }

    if (error){
        window.location.replace(url_login)

        return <div> { error } </div>
    }
};

export default ProtectedRoute;
