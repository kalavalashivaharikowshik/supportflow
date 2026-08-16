import {
  Navigate,
  Outlet,
  useLocation,
} from "react-router";

import {
  ROUTES,
} from "../constants/routes";

import useAuth from "../hooks/useAuth";

import LoadingSpinner from "../components/common/LoadingSpinner";


function ProtectedRoute() {
  const {
    isAuthenticated,
    loading,
  } = useAuth();

  const location =
    useLocation();


  if (loading) {
    return (
      <div
        className="
          flex min-h-screen
          items-center justify-center
          bg-slate-50
        "
      >
        <LoadingSpinner
          label="Checking session..."
        />
      </div>
    );
  }


  if (!isAuthenticated) {
    return (
      <Navigate
        to={ROUTES.LOGIN}
        replace
        state={{
          from: location.pathname,
        }}
      />
    );
  }


  return <Outlet />;
}


export default ProtectedRoute;