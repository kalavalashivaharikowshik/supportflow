import {
  Outlet,
} from "react-router";


function AuthLayout() {
  return (
    <main
      className="
        min-h-screen bg-slate-50
        px-4 py-10
      "
    >
      <div
        className="
          mx-auto flex min-h-[80vh]
          max-w-6xl items-center
          justify-center
        "
      >
        <div className="w-full max-w-md">
          <div className="mb-8 text-center">
            <div
              className="
                text-2xl font-bold
                tracking-tight text-slate-900
              "
            >
              SupportFlow
            </div>

            <p
              className="
                mt-2 text-sm
                text-slate-500
              "
            >
              SLA-driven support ticket
              management
            </p>
          </div>

          <Outlet />
        </div>
      </div>
    </main>
  );
}


export default AuthLayout;