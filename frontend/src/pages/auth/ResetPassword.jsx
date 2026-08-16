import {
  useState,
} from "react";

import {
  Navigate,
  useLocation,
  useNavigate,
} from "react-router";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import Input from "../../components/common/Input";

import {
  ROUTES,
} from "../../constants/routes";

import {
  resetPassword,
} from "../../services/authService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";

import {
  validatePassword,
} from "../../utils/validation";


function ResetPassword() {
  const location =
    useLocation();

  const navigate =
    useNavigate();

  const email =
    location.state?.email;

  const resetToken =
    location.state?.resetToken;

  const [password, setPassword] =
    useState("");

  const [
    confirmPassword,
    setConfirmPassword,
  ] = useState("");

  const [errors, setErrors] =
    useState({});

  const [loading, setLoading] =
    useState(false);


  if (!email || !resetToken) {
    return (
      <Navigate
        to={ROUTES.FORGOT_PASSWORD}
        replace
      />
    );
  }


  const handleSubmit =
    async (event) => {
      event.preventDefault();

      const nextErrors = {};

      const passwordError =
        validatePassword(
          password
        );

      if (passwordError) {
        nextErrors.password =
          passwordError;
      }

      if (
        password !==
        confirmPassword
      ) {
        nextErrors.confirmPassword =
          "Passwords do not match.";
      }

      setErrors(nextErrors);

      if (
        Object.keys(nextErrors)
          .length > 0
      ) {
        return;
      }

      setLoading(true);

      try {
        await resetPassword({
          email,
          reset_token:
            resetToken,
          new_password:
            password,
        });

        toast.success(
          "Password reset successfully."
        );

        navigate(
          ROUTES.LOGIN,
          {
            replace: true,
          }
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to reset password."
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
        Reset password
      </h1>

      <p
        className="
          mt-2 text-sm
          text-slate-500
        "
      >
        Create a new password for
        your SupportFlow account.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4"
      >
        <Input
          id="password"
          type="password"
          label="New password"
          autoComplete="new-password"
          value={password}
          onChange={
            (event) => {
              setPassword(
                event.target.value
              );

              setErrors(
                (current) => ({
                  ...current,
                  password: "",
                })
              );
            }
          }
          error={
            errors.password
          }
        />

        <Input
          id="confirmPassword"
          type="password"
          label="Confirm password"
          autoComplete="new-password"
          value={
            confirmPassword
          }
          onChange={
            (event) => {
              setConfirmPassword(
                event.target.value
              );

              setErrors(
                (current) => ({
                  ...current,
                  confirmPassword: "",
                })
              );
            }
          }
          error={
            errors.confirmPassword
          }
        />

        <Button
          type="submit"
          loading={loading}
          className="w-full"
        >
          Reset password
        </Button>
      </form>
    </div>
  );
}


export default ResetPassword;