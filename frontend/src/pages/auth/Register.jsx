import {
  useState,
} from "react";

import {
  Link,
  useNavigate,
} from "react-router";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import Input from "../../components/common/Input";

import {
  ROUTES,
} from "../../constants/routes";

import {
  register,
} from "../../services/authService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";

import {
  isValidEmail,
  required,
  validatePassword,
} from "../../utils/validation";


function Register() {
  const navigate =
    useNavigate();

  const [form, setForm] =
    useState({
      full_name: "",
      email: "",
      password: "",
      confirmPassword: "",
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

    nextErrors.full_name =
      required(
        form.full_name,
        "Full name"
      );

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
      ) ||
      validatePassword(
        form.password
      );

    if (
      form.password !==
      form.confirmPassword
    ) {
      nextErrors.confirmPassword =
        "Passwords do not match.";
    }

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
        await register({
          full_name:
            form.full_name.trim(),
          email:
            form.email.trim(),
          password:
            form.password,
        });

        toast.success(
          "Account created successfully."
        );

        navigate(
          ROUTES.LOGIN,
          {
            replace: true,
          }
        );
      } catch (error) {
        toast.error(
          getApiErrorMessage(
            error,
            "Unable to create account."
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
      <h1
        className="
          text-2xl font-bold
          text-slate-900
        "
      >
        Create an account
      </h1>

      <p
        className="
          mt-2 text-sm
          text-slate-500
        "
      >
        Register as a requester to
        submit and track support
        tickets.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4"
      >
        <Input
          id="full_name"
          name="full_name"
          label="Full name"
          value={
            form.full_name
          }
          onChange={handleChange}
          error={
            errors.full_name
          }
        />

        <Input
          id="email"
          name="email"
          type="email"
          label="Email"
          autoComplete="email"
          value={form.email}
          onChange={handleChange}
          error={errors.email}
        />

        <Input
          id="password"
          name="password"
          type="password"
          label="Password"
          autoComplete="new-password"
          value={
            form.password
          }
          onChange={handleChange}
          error={
            errors.password
          }
        />

        <Input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          label="Confirm password"
          autoComplete="new-password"
          value={
            form.confirmPassword
          }
          onChange={handleChange}
          error={
            errors.confirmPassword
          }
        />

        <Button
          type="submit"
          loading={loading}
          className="w-full"
        >
          Create account
        </Button>
      </form>

      <p
        className="
          mt-6 text-center
          text-sm text-slate-500
        "
      >
        Already registered?{" "}
        <Link
          to={ROUTES.LOGIN}
          className="
            font-semibold
            text-slate-900
          "
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}


export default Register;