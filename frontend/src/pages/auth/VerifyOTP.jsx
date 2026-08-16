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
  verifyOtp,
} from "../../services/authService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function VerifyOTP() {
  const location =
    useLocation();

  const navigate =
    useNavigate();

  const email =
    location.state?.email;

  const [otp, setOtp] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  if (!email) {
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

      const value =
        otp.trim();

      if (!value) {
        setError(
          "Verification code is required."
        );
        return;
      }

      setLoading(true);

      try {
        const result =
          await verifyOtp({
            email,
            otp: value,
          });

        toast.success(
          "Verification successful."
        );

        navigate(
          ROUTES.RESET_PASSWORD,
          {
            state: {
              email,
              resetToken:
                result.reset_token,
            },
          }
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Invalid verification code."
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
        Verify code
      </h1>

      <p
        className="
          mt-2 text-sm
          text-slate-500
        "
      >
        Enter the verification code
        sent to {email}.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4"
      >
        <Input
          id="otp"
          label="Verification code"
          inputMode="numeric"
          autoComplete="one-time-code"
          value={otp}
          onChange={
            (event) => {
              setOtp(
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
          Verify code
        </Button>
      </form>
    </div>
  );
}


export default VerifyOTP;