// src/components/AuthRoute.tsx
import React, { type ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface AuthRouteProps {
  children: ReactNode;
}

/**
 * ProtectedRoute ensures only authenticated users
 * can access the wrapped content.
 *
 * Usage:
 *   <ProtectedRoute>
 *     <Dashboard />
 *   </ProtectedRoute>
 */
const AuthRoute: React.FC<AuthRouteProps> = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access-token");
    if (token) {
      navigate("/", { replace: true });
    }
  }, [navigate]);

  return (
    <div className="">
      {children}
    </div>
  );
};

export default AuthRoute;
