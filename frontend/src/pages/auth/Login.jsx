import {
  useState,
} from "react";

import {
  Link,
  useLocation,
  useNavigate,
} from "react-router";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import Input from "../../components/common/Input";

import {
  getDashboardRoute,
  ROUTES,
} from "../../constants/routes";

import useAuth from "../../hooks/useAuth";

import {
  getApiErrorMessage,
} from "../../utils/apiError";

import {
  isValidEmail,
  required,
} from "../../utils/validation";


function Login() {
  const navigate =
    useNavigate();

  const location =
    useLocation();

  const {
    login,
  } = useAuth();


  const [form, setForm] =
    useState({
      email: "",
      password: "",
    });

  const [errors, setErrors] =
    useState({});

  const [loading, setLoading] =
    useState(false);


  const handleChange = (
    event
  ) => {
    const {
      name,
      value,
    } = event.target;

    setForm(
      (current) => ({
        ...current,
        [name]: value,
      })
    );

    setErrors(
      (current) => ({
        ...current,
        [name]: "",
      })
    );
  };


  const validate = () => {
    const nextErrors = {};

    const emailRequired =
      required(
        form.email,
        "Email"
      );

    if (emailRequired) {
      nextErrors.email =
        emailRequired;
    } else if (
      !isValidEmail(
        form.email
      )
    ) {
      nextErrors.email =
        "Enter a valid email address.";
    }

    nextErrors.password =
      required(
        form.password,
        "Password"
      );

    Object.keys(
      nextErrors
    ).forEach(
      (key) => {
        if (!nextErrors[key]) {
          delete nextErrors[key];
        }
      }
    );

    setErrors(nextErrors);

    return (
      Object.keys(nextErrors)
        .length === 0
    );
  };


  const handleSubmit =
    async (event) => {
      event.preventDefault();

      if (!validate()) {
        return;
      }

      setLoading(true);

      try {
        const user =
          await login({
            email:
              form.email.trim(),
            password:
              form.password,
          });

        toast.success(
          "Login successful."
        );

        const requestedPath =
          location.state?.from;

        navigate(
          requestedPath ||
            getDashboardRoute(
              user.role
            ),
          {
            replace: true,
          }
        );
      } catch (error) {
        toast.error(
          getApiErrorMessage(
            error,
            "Unable to sign in."
          )
        );
      } finally {
        setLoading(false);
      }
    };


  return (
    <div
      className="
        rounded-2xl border
        border-slate-200 bg-white
        p-6 shadow-sm sm:p-8
      "
    >
      <div>
        <h1
          className="
            text-2xl font-bold
            text-slate-900
          "
        >
          Welcome back
        </h1>

        <p
          className="
            mt-2 text-sm
            text-slate-500
          "
        >
          Sign in to continue to
          SupportFlow.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4"
      >
        <Input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          label="Email"
          placeholder="you@example.com"
          value={form.email}
          onChange={handleChange}
          error={errors.email}
        />

        <Input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          label="Password"
          placeholder="Enter your password"
          value={form.password}
          onChange={handleChange}
          error={errors.password}
        />

        <div
          className="
            flex justify-end
          "
        >
          <Link
            to={
              ROUTES.FORGOT_PASSWORD
            }
            className="
              text-sm font-medium
              text-slate-700
              hover:text-slate-950
            "
          >
            Forgot password?
          </Link>
        </div>

        <Button
          type="submit"
          loading={loading}
          className="w-full"
        >
          Sign in
        </Button>
      </form>

      <p
        className="
          mt-6 text-center
          text-sm text-slate-500
        "
      >
        Don&apos;t have an account?{" "}
        <Link
          to={ROUTES.REGISTER}
          className="
            font-semibold
            text-slate-900
          "
        >
          Create account
        </Link>
      </p>
    </div>
  );
}


export default Login;