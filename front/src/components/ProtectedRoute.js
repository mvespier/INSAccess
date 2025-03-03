import { useAuth } from "../contexts/AuthContext";

const ProtectedRoute = ({ children }) => {
    const { token, loading, error } = useAuth();

    const url_login = "http://localhost:5000/login"


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

        return <div>Eoozverkjnervkjne</div>
    }
};

export default ProtectedRoute;
