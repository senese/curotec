import { Navigate } from "react-router";
import { useAuth } from "./contexts/AuthProvider";

export const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading)
    return null;

  return isAuthenticated ? children : <Navigate to="/auth" />;
};