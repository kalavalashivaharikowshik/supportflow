import {
  Navigate,
  Route,
  Routes,
} from "react-router";

import {
  ROLES,
} from "../constants/roles";

import {
  ROUTES,
} from "../constants/routes";

import AuthLayout from "../layouts/AuthLayout";
import DashboardLayout from "../layouts/DashboardLayout";

import AdminDashboard from "../pages/admin/AdminDashboard";

import AgentDashboard from "../pages/agent/AgentDashboard";
import AssignedTickets from "../pages/agent/AssignedTickets";
import EscalatedTickets from "../pages/agent/EscalatedTickets";

import AdminConfiguration from "../pages/admin/AdminConfiguration";
import AllTickets from "../pages/admin/AllTickets";
import Reports from "../pages/admin/Reports";
import SLASettings from "../pages/admin/SLASettings";
import UserManagement from "../pages/admin/UserManagement";

import ForgotPassword from "../pages/auth/ForgotPassword";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import ResetPassword from "../pages/auth/ResetPassword";
import VerifyOTP from "../pages/auth/VerifyOTP";

import Notifications from "../pages/notifications/Notifications";

import NotFound from "../pages/NotFound";
import Profile from "../pages/Profile";

import CreateTicket from "../pages/requester/CreateTicket";
import MyTickets from "../pages/requester/MyTickets";
import RequesterDashboard from "../pages/requester/RequesterDashboard";

import TicketDetails from "../pages/tickets/TicketDetails";

import Unauthorized from "../pages/Unauthorized";

import ProtectedRoute from "./ProtectedRoute";
import RoleRoute from "./RoleRoute";


function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <Navigate
            to={ROUTES.LOGIN}
            replace
          />
        }
      />

      <Route
        element={
          <AuthLayout />
        }
      >
        <Route
          path={ROUTES.LOGIN}
          element={<Login />}
        />

        <Route
          path={ROUTES.REGISTER}
          element={<Register />}
        />

        <Route
          path={
            ROUTES.FORGOT_PASSWORD
          }
          element={
            <ForgotPassword />
          }
        />

        <Route
          path={
            ROUTES.VERIFY_OTP
          }
          element={
            <VerifyOTP />
          }
        />

        <Route
          path={
            ROUTES.RESET_PASSWORD
          }
          element={
            <ResetPassword />
          }
        />
      </Route>


      <Route
        element={
          <ProtectedRoute />
        }
      >
        <Route
          element={
            <DashboardLayout />
          }
        >
          <Route
            path={ROUTES.PROFILE}
            element={<Profile />}
          />

          <Route
            path={ROUTES.NOTIFICATIONS}
            element={
                <Notifications />
            }
          />


          {/* REQUESTER ROUTES */}
          <Route
            element={
              <RoleRoute
                allowedRoles={[
                  ROLES.REQUESTER,
                ]}
              />
            }
          >
            <Route
              path={
                ROUTES.REQUESTER_DASHBOARD
              }
              element={
                <RequesterDashboard />
              }
            />

            <Route
              path={
                ROUTES.REQUESTER_TICKETS
              }
              element={
                <MyTickets />
              }
            />

            <Route
              path={
                ROUTES.CREATE_TICKET
              }
              element={
                <CreateTicket />
              }
            />
          </Route>


          {/* SHARED REQUESTER + AGENT TICKET DETAILS */}
          <Route
            element={
              <RoleRoute
                allowedRoles={[
                  ROLES.REQUESTER,
                  ROLES.AGENT,
                  ROLES.ADMIN,
                ]}
              />
            }
          >
            <Route
              path={
                ROUTES.TICKET_DETAILS
              }
              element={
                <TicketDetails />
              }
            />
          </Route>


          {/* AGENT ROUTES */}
          <Route
            element={
              <RoleRoute
                allowedRoles={[
                  ROLES.AGENT,
                ]}
              />
            }
          >
            <Route
              path={
                ROUTES.AGENT_DASHBOARD
              }
              element={
                <AgentDashboard />
              }
            />

            <Route
              path={
                ROUTES.AGENT_TICKETS
              }
              element={
                <AssignedTickets />
              }
            />

            <Route
              path={
                ROUTES.AGENT_ESCALATED
              }
              element={
                <EscalatedTickets />
              }
            />
          </Route>


          {/* ADMIN ROUTES */}
          <Route
            element={
                <RoleRoute
                allowedRoles={[
                    ROLES.ADMIN,
                ]}
                />
            }
            >
            <Route
                path={
                ROUTES.ADMIN_DASHBOARD
                }
                element={
                <AdminDashboard />
                }
            />

            <Route
                path={
                ROUTES.ADMIN_TICKETS
                }
                element={
                <AllTickets />
                }
            />

            <Route
                path={
                ROUTES.ADMIN_USERS
                }
                element={
                <UserManagement />
                }
            />

            <Route
                path={
                ROUTES.ADMIN_SLA
                }
                element={
                <SLASettings />
                }
            />

            <Route
                path={
                ROUTES.ADMIN_CONFIG
                }
                element={
                <AdminConfiguration />
                }
            />

            <Route
                path={
                ROUTES.ADMIN_REPORTS
                }
                element={
                <Reports />
                }
            />
            </Route>
        </Route>
      </Route>


      <Route
        path={
          ROUTES.UNAUTHORIZED
        }
        element={
          <Unauthorized />
        }
      />

      <Route
        path="*"
        element={
          <NotFound />
        }
      />
    </Routes>
  );
}



export default AppRoutes;