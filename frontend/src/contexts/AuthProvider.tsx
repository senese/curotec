import React, {
  createContext,
  useState,
  useEffect,
  ReactNode,
  useContext,
} from "react";


interface AuthProviderProps {
  children: ReactNode;
}

interface IAuthContext {
  user: any;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
  createUser: (name: string, email: string, password: string) => any;
}

const AuthContext = createContext<IAuthContext | undefined>(undefined);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(function effect() {
    const token = localStorage.getItem("access_token");
    if (token) {
      getUserInfo(token);
      setIsAuthenticated(true)
    } else {
      setIsAuthenticated(false)
    }
    setLoading(false);
  }, []);

  const getUserInfo = async (token: string) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_USERS_URL!}me`, {
        method: "GET",
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      setUser(data)
    } catch (error) {
      console.error("Failed to fetch user:", error);
    }
  };

  const createUser = async (name: string, email: string, password: string) => {
    try {
      await fetch(process.env.REACT_APP_USERS_URL!, {
        method: "POST",
        headers: {
          'Content-Type': "application/json"
        },
        body: JSON.stringify({ name: name, email: email, password: password })
      })
    } catch (error) {
      throw Error("Failed to register")
    }
  };

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await fetch(process.env.REACT_APP_OAUTH!, {
        method: "POST",
        headers: {
          'Content-Type': "application/x-www-form-urlencoded"
        },
        body: formData
      })
      const data = await response.json()

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      setUser(data)
      setIsAuthenticated(true)
    } catch (error) {
      console.error("Failed to login:", error);
    }
  };

  const logout = async () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated, loading, createUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
