import { createContext, useContext, useState, useEffect } from "react";
import { fetchData } from '../js/randomUtils.js'
import constants from '../js/constants.js'

const AuthContext = createContext();

const API_URL = constants.API_URL;

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(false);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
          const result = await fetchData(API_URL+"/api/is_connected");
          if (result.data){
            setToken(result.data.is_connected);
          }
          setError(result.error);
          setLoading(false);
        };
    
        loadData();
    }, []);

    return (
        <AuthContext.Provider value={{ token, loading, error }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
