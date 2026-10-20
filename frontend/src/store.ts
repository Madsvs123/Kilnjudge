import { create } from "zustand";
import { persist } from "zustand/middleware";

type AuthState = {
  access: string | null;
  refresh: string | null;
  username: string | null;
  setSession: (access: string, refresh: string, username: string) => void;
  setAccess: (access: string) => void;
  setUsername: (username: string) => void;
  clear: () => void;
};

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      access: null,
      refresh: null,
      username: null,
      setSession: (access, refresh, username) => set({ access, refresh, username }),
      setAccess: (access) => set({ access }),
      setUsername: (username) => set({ username }),
      clear: () => set({ access: null, refresh: null, username: null }),
    }),
    { name: "kilnjudge-auth" },
  ),
);
