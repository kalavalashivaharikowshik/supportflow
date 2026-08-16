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
  forgotPassword,
} from "../../services/authService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";

import {
  isValidEmail,
  required,
} from "../../utils/validation";


function ForgotPassword() {
  const navigate =
    useNavigate();

  const [email, setEmail] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  const handleSubmit =
    async (event) => {
      event.preventDefault();

      const requiredError =
        required(
          email,
          "Email"
        );

      if (requiredError) {
        setError(requiredError);
        return;
      }

      if (!isValidEmail(email)) {
        setError(
          "Enter a valid email address."
        );
        return;
      }

      setError("");
      setLoading(true);

      try {
        await forgotPassword({
          email: email.trim(),
        });

        toast.success(
          "Verification code sent."
        );

        navigate(
          ROUTES.VERIFY_OTP,
          {
            state: {
              email:
                email.trim(),
            },
          }
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to send verification code."
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
        Forgot password
      </h1>

      <p
        className="
          mt-2 text-sm
          text-slate-500
        "
      >
        Enter your email and we
        will send you a verification
        code.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4"
      >
        <Input
          id="email"
          type="email"
          label="Email"
          autoComplete="email"
          value={email}
          onChange={
            (event) => {
              setEmail(
                event.target.value
              );
              setError("");
            }
          }
          error={error}
        />

        <Button
          type="submit"
          loading={loading}
          className="w-full"
        >
          Send verification code
        </Button>
      </form>

      <Link
        to={ROUTES.LOGIN}
        className="
          mt-6 block text-center
          text-sm font-semibold
          text-slate-700
        "
      >
        Back to sign in
      </Link>
    </div>
  );
}


export default ForgotPassword;