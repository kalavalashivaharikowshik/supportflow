import {
  Link,
} from "react-router";

import {
  ROUTES,
} from "../constants/routes";


function NotFound() {
  return (
    <div
      className="
        flex min-h-screen items-center
        justify-center bg-slate-50 px-4
      "
    >
      <div className="text-center">
        <p
          className="
            text-sm font-semibold
            text-slate-500
          "
        >
          404
        </p>

        <h1
          className="
            mt-2 text-3xl font-bold
            text-slate-900
          "
        >
          Page not found
        </h1>

        <p className="mt-3 text-slate-500">
          The requested page does not exist.
        </p>

        <Link
          to={ROUTES.LOGIN}
          className="
            mt-6 inline-block
            font-semibold text-slate-900
            underline
          "
        >
          Go to login
        </Link>
      </div>
    </div>
  );
}


export default NotFound;