import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Navigate, useNavigate } from "react-router-dom";
import { z } from "zod";

import { api, formatApiError } from "../api";
import { Field } from "../components/Field";
import { Gate } from "../components/Gate";
import { useAuth } from "../store";
import { usePageTitle } from "../usePageTitle";

const schema = z.object({
  username: z.string().min(1, "Enter your username."),
  password: z.string().min(1, "Enter your password."),
});

type LoginValues = z.infer<typeof schema>;

export function LoginPage() {
  const navigate = useNavigate();
  const access = useAuth((state) => state.access);
  const setSession = useAuth((state) => state.setSession);
  usePageTitle("Sign in");
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<LoginValues>({ resolver: zodResolver(schema) });

  if (access) {
    return <Navigate to="/" replace />;
  }

  async function onSubmit(values: LoginValues) {
    try {
      const { data } = await api.post<{ access: string; refresh: string }>("/api/auth/token/", values);
      setSession(data.access, data.refresh, values.username);
      navigate("/");
    } catch (error) {
      setError("root", { message: formatApiError(error) });
    }
  }

  return (
    <Gate
      title="Sign in"
      lede="Open the kiln and run a solution you wrote."
      alternate={{ href: "/register", text: "Create the owner account" }}
    >
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <Field label="Username" error={errors.username?.message}>
          <input autoComplete="username" {...register("username")} />
        </Field>
        <Field label="Password" error={errors.password?.message}>
          <input type="password" autoComplete="current-password" {...register("password")} />
        </Field>
        {errors.root?.message ? <p className="form-error">{errors.root.message}</p> : null}
        <button type="submit" className="primary" disabled={isSubmitting}>
          {isSubmitting ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </Gate>
  );
}
