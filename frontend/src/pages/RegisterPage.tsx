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
  username: z
    .string()
    .regex(/^[A-Za-z0-9_]{3,150}$/, "Use 3–150 letters, numbers, or underscores."),
  password: z.string().min(8, "Use at least 8 characters.").max(128),
});

type RegisterValues = z.infer<typeof schema>;

export function RegisterPage() {
  const navigate = useNavigate();
  const access = useAuth((state) => state.access);
  const setSession = useAuth((state) => state.setSession);
  usePageTitle("Create account");
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<RegisterValues>({ resolver: zodResolver(schema) });

  if (access) {
    return <Navigate to="/" replace />;
  }

  async function onSubmit(values: RegisterValues) {
    try {
      await api.post("/api/auth/register/", values);
      const { data } = await api.post<{ access: string; refresh: string }>("/api/auth/token/", values);
      setSession(data.access, data.refresh, values.username);
      navigate("/");
    } catch (error) {
      setError("root", { message: formatApiError(error) });
    }
  }

  return (
    <Gate
      title="Create the owner account"
      lede="This judge keeps one history: yours. Register on this machine, then submit Python you wrote."
      alternate={{ href: "/login", text: "Already registered? Sign in" }}
    >
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <Field label="Username" error={errors.username?.message}>
          <input autoComplete="username" {...register("username")} />
        </Field>
        <Field label="Password" error={errors.password?.message}>
          <input type="password" autoComplete="new-password" {...register("password")} />
        </Field>
        {errors.root?.message ? <p className="form-error">{errors.root.message}</p> : null}
        <button type="submit" className="primary" disabled={isSubmitting}>
          {isSubmitting ? "Creating account…" : "Create account"}
        </button>
      </form>
    </Gate>
  );
}
