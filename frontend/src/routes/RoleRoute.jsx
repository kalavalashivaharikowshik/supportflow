import {
  Navigate,
  Outlet,
} from "react-router";

import {
  ROUTES,
} from "../constants/routes";

import useAuth from "../hooks/useAuth";


function RoleRoute({
  allowedRoles,
}) {
  const {
    user,
  } = useAuth();


  if (
    !user ||
    !allowedRoles.includes(
      user.role
    )
  ) {
    return (
      <Navigate
        to={ROUTES.UNAUTHORIZED}
        replace
      />
    );
  }


  return <Outlet />;
}


export default RoleRoute;