import { createContext, useContext, useState, useEffect } from "react";

// Crée un contexte d'authentification
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    // Vérifier si l'utilisateur est déjà connecté (ex: via un token en cookie)
    useEffect(() => {
        fetch("/api/me", { credentials: "include" }) // Flask doit gérer la session
            .then((res) => res.ok ? res.json() : Promise.reject())
            .then((data) => setUser(data))
            .catch(() => setUser(null));
    }, []);

    const login = async (username, password) => {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include", // Important pour Flask et les sessions
            body: JSON.stringify({ username, password }),
        });

        if (res.ok) {
            const data = await res.json();
            setUser(data);
            return true;
        } else {
            return false;
        }
    };

    const logout = async () => {
        await fetch("/api/logout", { method: "POST", credentials: "include" });
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

// Hook pour accéder facilement au contexte
export const useAuth = () => useContext(AuthContext);
