// src/components/ProtectedRoute.tsx
import React, { type ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface ProtectedRouteProps {
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
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access-token");
    if (!token) {
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      {children}
    </div>
  );
};

export default ProtectedRoute;
