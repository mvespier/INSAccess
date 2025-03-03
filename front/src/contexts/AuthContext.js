import { createContext, useContext, useState, useEffect } from "react";

const fetchData = async (data_path) => {
    const initConfig = {
        method:'GET',
        headers:{'Content-Type':'application/json', 'Accept':'application/json'},
        mode:'cors'
    }
    try {
        const response = await fetch(data_path, initConfig);
        if (!response.ok) {
        throw new Error("Erreur, vérification de la connection de l'utilisateur impossible");
        }
        const json = await response.json();
        return { data: json, error: null };
    } catch (error) {
        return { data: null, error: error.message };
    }
};

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(false);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
          const result = await fetchData("/api/is_connected");
          setToken(result.data.is_connected);
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
