import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

import { useAuth } from "./store";

export const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

type RetriableConfig = InternalAxiosRequestConfig & { _retry?: boolean };

export const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
  const access = useAuth.getState().access;
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetriableConfig | undefined;
    const url = config?.url ?? "";
    const refresh = useAuth.getState().refresh;
    const isCredentialCall = url.includes("/api/auth/token/") || url.includes("/api/auth/register/");

    if (error.response?.status === 401 && config && !config._retry && refresh && !isCredentialCall) {
      config._retry = true;
      try {
        const { data } = await axios.post<{ access: string }>(`${API_URL}/api/auth/token/refresh/`, {
          refresh,
        });
        useAuth.getState().setAccess(data.access);
        config.headers.Authorization = `Bearer ${data.access}`;
        return api.request(config);
      } catch (refreshError) {
        useAuth.getState().clear();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);

export function formatApiError(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return "Something went wrong.";
  }
  if (!error.response) {
    return "The kiln could not be reached. Start the Django server on port 8000.";
  }
  const data: unknown = error.response.data;
  if (typeof data === "string" && data.trim()) {
    return data;
  }
  if (data && typeof data === "object") {
    if ("detail" in data && typeof data.detail === "string") {
      return data.detail;
    }
    const parts: string[] = [];
    for (const [key, value] of Object.entries(data)) {
      if (Array.isArray(value)) {
        parts.push(`${key}: ${value.join(" ")}`);
      } else if (typeof value === "string") {
        parts.push(`${key}: ${value}`);
      }
    }
    if (parts.length) {
      return parts.join(" ");
    }
  }
  return "The request failed.";
}
