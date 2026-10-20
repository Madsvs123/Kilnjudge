import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../store";

export function RequireAuth() {
  const access = useAuth((state) => state.access);
  if (!access) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
}
