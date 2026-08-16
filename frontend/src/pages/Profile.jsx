import {
  useEffect,
  useState,
} from "react";

import toast from "react-hot-toast";

import Button from "../components/common/Button";
import Input from "../components/common/Input";
import PageHeader from "../components/common/PageHeader";

import useAuth from "../hooks/useAuth";

import {
  changePassword,
  updateProfile,
} from "../services/authService";

import {
  getApiErrorMessage,
} from "../utils/apiError";

import {
  required,
  validatePassword,
} from "../utils/validation";


function Profile() {
  const {
    user,
    refreshUser,
  } = useAuth();

  const [profile, setProfile] =
    useState({
      full_name: "",
      email: "",
    });

  const [passwordForm, setPasswordForm] =
    useState({
      current_password: "",
      new_password: "",
      confirm_password: "",
    });

  const [
    profileLoading,
    setProfileLoading,
  ] = useState(false);

  const [
    passwordLoading,
    setPasswordLoading,
  ] = useState(false);


  useEffect(() => {
    if (user) {
      setProfile({
        full_name:
          user.full_name ?? "",
        email:
          user.email ?? "",
      });
    }
  }, [user]);


  const saveProfile =
    async (event) => {
      event.preventDefault();

      const fullNameError =
        required(
          profile.full_name,
          "Full name"
        );

      if (fullNameError) {
        toast.error(
          fullNameError
        );
        return;
      }

      setProfileLoading(true);

      try {
        await updateProfile({
          full_name:
            profile.full_name.trim(),
        });

        await refreshUser();

        toast.success(
          "Profile updated."
        );
      } catch (error) {
        toast.error(
          getApiErrorMessage(
            error,
            "Unable to update profile."
          )
        );
      } finally {
        setProfileLoading(false);
      }
    };


  const savePassword =
    async (event) => {
      event.preventDefault();

      const passwordError =
        validatePassword(
          passwordForm.new_password
        );

      if (passwordError) {
        toast.error(
          passwordError
        );
        return;
      }

      if (
        passwordForm.new_password !==
        passwordForm.confirm_password
      ) {
        toast.error(
          "New passwords do not match."
        );
        return;
      }

      setPasswordLoading(true);

      try {
        await changePassword({
          current_password:
            passwordForm.current_password,
          new_password:
            passwordForm.new_password,
        });

        setPasswordForm({
          current_password: "",
          new_password: "",
          confirm_password: "",
        });

        toast.success(
          "Password changed successfully."
        );
      } catch (error) {
        toast.error(
          getApiErrorMessage(
            error,
            "Unable to change password."
          )
        );
      } finally {
        setPasswordLoading(false);
      }
    };


  return (
    <div className="space-y-6">
      <PageHeader
        title="Profile"
        description="Manage your account information and password."
      />

      <div
        className="
          grid gap-6 lg:grid-cols-2
        "
      >
        <form
          onSubmit={saveProfile}
          className="
            rounded-xl border
            border-slate-200
            bg-white p-6 shadow-sm
          "
        >
          <h2
            className="
              text-lg font-semibold
              text-slate-900
            "
          >
            Account information
          </h2>

          <div className="mt-5 space-y-4">
            <Input
              id="full_name"
              label="Full name"
              value={
                profile.full_name
              }
              onChange={
                (event) =>
                  setProfile(
                    (current) => ({
                      ...current,
                      full_name:
                        event.target.value,
                    })
                  )
              }
            />

            <Input
              id="email"
              type="email"
              label="Email"
              value={profile.email}
              disabled
            />

            <Input
              id="role"
              label="Role"
              value={
                user?.role ?? ""
              }
              disabled
            />

            <Button
              type="submit"
              loading={
                profileLoading
              }
            >
              Save profile
            </Button>
          </div>
        </form>

        <form
          onSubmit={savePassword}
          className="
            rounded-xl border
            border-slate-200
            bg-white p-6 shadow-sm
          "
        >
          <h2
            className="
              text-lg font-semibold
              text-slate-900
            "
          >
            Change password
          </h2>

          <div className="mt-5 space-y-4">
            <Input
              id="current_password"
              type="password"
              label="Current password"
              autoComplete="current-password"
              value={
                passwordForm
                  .current_password
              }
              onChange={
                (event) =>
                  setPasswordForm(
                    (current) => ({
                      ...current,
                      current_password:
                        event.target.value,
                    })
                  )
              }
            />

            <Input
              id="new_password"
              type="password"
              label="New password"
              autoComplete="new-password"
              value={
                passwordForm
                  .new_password
              }
              onChange={
                (event) =>
                  setPasswordForm(
                    (current) => ({
                      ...current,
                      new_password:
                        event.target.value,
                    })
                  )
              }
            />

            <Input
              id="confirm_password"
              type="password"
              label="Confirm new password"
              autoComplete="new-password"
              value={
                passwordForm
                  .confirm_password
              }
              onChange={
                (event) =>
                  setPasswordForm(
                    (current) => ({
                      ...current,
                      confirm_password:
                        event.target.value,
                    })
                  )
              }
            />

            <Button
              type="submit"
              loading={
                passwordLoading
              }
            >
              Change password
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}


export default Profile;