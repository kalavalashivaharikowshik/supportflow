import {
  LogOut,
  Menu,
  UserRound,
} from "lucide-react";

import {
  Link,
  Outlet,
  useNavigate,
} from "react-router";

import {
  useState,
} from "react";

import toast from "react-hot-toast";

import Button from "../components/common/Button";
import Sidebar from "../components/common/Sidebar";
import NotificationBell from "../components/notifications/NotificationBell";

import {
  ROUTES,
} from "../constants/routes";

import useAuth from "../hooks/useAuth";


function DashboardLayout() {
  const navigate =
    useNavigate();

  const {
    user,
    logout,
  } = useAuth();

  const [
    mobileMenuOpen,
    setMobileMenuOpen,
  ] = useState(false);


  const handleLogout =
    async () => {
      await logout();

      toast.success(
        "Signed out successfully."
      );

      navigate(
        ROUTES.LOGIN,
        {
          replace: true,
        }
      );
    };


  return (
    <div
      className="
        min-h-screen
        bg-slate-50
      "
    >
      <Sidebar
        role={user?.role}
        mobileOpen={
          mobileMenuOpen
        }
        onMobileClose={
          () =>
            setMobileMenuOpen(
              false
            )
        }
      />

      <div
        className="
          min-h-screen
          lg:pl-64
        "
      >
        <header
          className="
            sticky top-0
            z-30
            border-b
            border-slate-200
            bg-white/95
            backdrop-blur
          "
        >
          <div
            className="
              flex h-16
              items-center
              justify-between
              gap-4 px-4
              sm:px-6
              lg:px-8
            "
          >
            <div
              className="
                flex min-w-0
                items-center
                gap-3
              "
            >
              <button
                type="button"
                onClick={
                  () =>
                    setMobileMenuOpen(
                      true
                    )
                }
                className="
                  shrink-0
                  rounded-lg p-2
                  text-slate-600
                  transition
                  hover:bg-slate-100
                  hover:text-slate-900
                  focus-visible:outline-none
                  focus-visible:ring-2
                  focus-visible:ring-slate-400
                  focus-visible:ring-offset-2
                  lg:hidden
                "
                aria-label="Open navigation"
                aria-expanded={
                  mobileMenuOpen
                }
              >
                <Menu
                  className="h-5 w-5"
                />
              </button>

              <div
                className="
                  min-w-0
                "
              >
                <p
                  className="
                    truncate text-sm
                    font-semibold
                    text-slate-900
                  "
                >
                  Welcome,{" "}
                  {user?.full_name}
                </p>

                <p
                  className="
                    hidden truncate
                    text-xs
                    text-slate-500
                    sm:block
                  "
                >
                  Support ticket operations
                </p>
              </div>
            </div>

            <div
              className="
                flex shrink-0
                items-center
                gap-1 sm:gap-2
              "
            >
              <NotificationBell />

              <Link
                to={
                  ROUTES.PROFILE
                }
                className="
                  inline-flex
                  h-10 items-center
                  gap-2 rounded-lg
                  px-2 text-sm
                  font-medium
                  text-slate-700
                  transition
                  hover:bg-slate-100
                  hover:text-slate-900
                  focus-visible:outline-none
                  focus-visible:ring-2
                  focus-visible:ring-slate-400
                  focus-visible:ring-offset-2
                  sm:px-3
                "
              >
                <UserRound
                  className="
                    h-4 w-4
                    shrink-0
                  "
                />

                <span
                  className="
                    hidden md:inline
                  "
                >
                  Profile
                </span>
              </Link>

              <Button
                variant="ghost"
                onClick={
                  handleLogout
                }
                className="
                  px-2 sm:px-3
                "
              >
                <LogOut
                  className="
                    h-4 w-4
                    shrink-0
                  "
                />

                <span
                  className="
                    hidden md:inline
                  "
                >
                  Logout
                </span>
              </Button>
            </div>
          </div>
        </header>

        <main
          className="
            mx-auto
            max-w-[1600px]
            px-4 py-6
            sm:px-6
            lg:px-8
          "
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}


export default DashboardLayout;