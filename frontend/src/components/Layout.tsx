import { useQuery, useQueryClient } from "@tanstack/react-query";
import clsx from "clsx";
import { Flame, GitCompare, History, Library, LogOut } from "lucide-react";
import { useEffect } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { api } from "../api";
import { useAuth } from "../store";

export function Layout() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const username = useAuth((state) => state.username);
  const setUsername = useAuth((state) => state.setUsername);
  const clear = useAuth((state) => state.clear);
  const me = useQuery({
    queryKey: ["me"],
    queryFn: async () => (await api.get<{ username: string }>("/api/auth/me/")).data,
  });

  useEffect(() => {
    if (me.data?.username) {
      setUsername(me.data.username);
    }
  }, [me.data, setUsername]);

  function signOut() {
    clear();
    queryClient.clear();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <NavLink to="/" className="brand" end>
            <span className="mark" aria-hidden="true">
              <Flame size={18} />
            </span>
            <span>Kilnjudge</span>
          </NavLink>
          <nav className="nav" aria-label="Primary">
            <NavLink to="/" end className={({ isActive }) => clsx("nav-link", isActive && "is-active")}>
              <Library size={16} aria-hidden="true" />
              Problems
            </NavLink>
            <NavLink
              to="/history"
              className={({ isActive }) => clsx("nav-link", isActive && "is-active")}
            >
              <History size={16} aria-hidden="true" />
              History
            </NavLink>
            <NavLink
              to="/compare"
              className={({ isActive }) => clsx("nav-link", isActive && "is-active")}
            >
              <GitCompare size={16} aria-hidden="true" />
              Compare
            </NavLink>
          </nav>
          <div className="session">
            <span>{username ? `Signed in as ${username}` : "Signed in"}</span>
            <button type="button" className="ghost" onClick={signOut}>
              <LogOut size={16} aria-hidden="true" />
              Sign out
            </button>
          </div>
        </div>
      </header>
      <Outlet />
    </div>
  );
}
