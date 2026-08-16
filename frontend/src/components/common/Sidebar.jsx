import {
  AlertTriangle,
  BarChart3,
  FilePlus2,
  Gauge,
  LayoutDashboard,
  ListChecks,
  Settings,
  Ticket,
  Users,
  X,
} from "lucide-react";

import {
  NavLink,
} from "react-router";

import {
  ROLES,
} from "../../constants/roles";

import {
  ROUTES,
} from "../../constants/routes";


const requesterItems = [
  {
    label: "Dashboard",
    to:
      ROUTES.REQUESTER_DASHBOARD,
    icon: LayoutDashboard,
    end: true,
  },
  {
    label: "My Tickets",
    to:
      ROUTES.REQUESTER_TICKETS,
    icon: Ticket,
  },
  {
    label: "Create Ticket",
    to:
      ROUTES.CREATE_TICKET,
    icon: FilePlus2,
  },
];


const agentItems = [
  {
    label: "Dashboard",
    to:
      ROUTES.AGENT_DASHBOARD,
    icon: LayoutDashboard,
    end: true,
  },
  {
    label: "Assigned Tickets",
    to:
      ROUTES.AGENT_TICKETS,
    icon: ListChecks,
  },
  {
    label: "Escalated",
    to:
      ROUTES.AGENT_ESCALATED,
    icon: AlertTriangle,
  },
];


const adminItems = [
  {
    label: "Dashboard",
    to:
      ROUTES.ADMIN_DASHBOARD,
    icon: LayoutDashboard,
    end: true,
  },
  {
    label: "Tickets",
    to:
      ROUTES.ADMIN_TICKETS,
    icon: Ticket,
  },
  {
    label: "Users",
    to:
      ROUTES.ADMIN_USERS,
    icon: Users,
  },
  {
    label: "SLA Settings",
    to:
      ROUTES.ADMIN_SLA,
    icon: Gauge,
  },
  {
    label: "Configuration",
    to:
      ROUTES.ADMIN_CONFIG,
    icon: Settings,
  },
  {
    label: "Reports",
    to:
      ROUTES.ADMIN_REPORTS,
    icon: BarChart3,
  },
];


function getItems(
  role
) {
  if (
    role ===
    ROLES.REQUESTER
  ) {
    return requesterItems;
  }

  if (
    role ===
    ROLES.AGENT
  ) {
    return agentItems;
  }

  if (
    role ===
    ROLES.ADMIN
  ) {
    return adminItems;
  }

  return [];
}


function getRoleLabel(
  role
) {
  if (!role) {
    return "";
  }

  return role
    .replaceAll(
      "_",
      " "
    )
    .toLowerCase()
    .replace(
      /\b\w/g,
      (character) =>
        character.toUpperCase()
    );
}


function Sidebar({
  role,
  mobileOpen,
  onMobileClose,
}) {
  const items =
    getItems(role);

  const roleLabel =
    getRoleLabel(role);


  const renderSidebarContent =
    (isMobile = false) => (
      <>
        <div
          className="
            flex h-16
            items-center
            justify-between
            border-b
            border-slate-800
            px-5
          "
        >
          <div
            className="min-w-0"
          >
            <p
              className="
                truncate text-lg
                font-bold
                text-white
              "
            >
              SupportFlow
            </p>

            <p
              className="
                truncate text-xs
                text-slate-400
              "
            >
              {roleLabel}
            </p>
          </div>

          {isMobile && (
            <button
              type="button"
              onClick={
                onMobileClose
              }
              className="
                shrink-0
                rounded-lg p-2
                text-slate-400
                transition
                hover:bg-slate-800
                hover:text-white
                focus-visible:outline-none
                focus-visible:ring-2
                focus-visible:ring-slate-500
                focus-visible:ring-offset-2
                focus-visible:ring-offset-slate-900
              "
              aria-label="Close navigation"
            >
              <X
                className="h-5 w-5"
              />
            </button>
          )}
        </div>

        <nav
          className="
            flex-1 space-y-1
            overflow-y-auto
            p-3
          "
          aria-label="Primary navigation"
        >
          {items.map(
            ({
              label,
              to,
              icon: Icon,
              end = false,
            }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                onClick={
                  isMobile
                    ? onMobileClose
                    : undefined
                }
                className={
                  ({
                    isActive,
                  }) => `
                    flex items-center
                    gap-3 rounded-lg
                    px-3 py-2.5
                    text-sm font-medium
                    transition

                    focus-visible:outline-none
                    focus-visible:ring-2
                    focus-visible:ring-slate-500
                    focus-visible:ring-offset-2
                    focus-visible:ring-offset-slate-900

                    ${
                      isActive
                        ? "bg-slate-800 text-white"
                        : "text-slate-300 hover:bg-slate-800 hover:text-white"
                    }
                  `
                }
              >
                <Icon
                  className="
                    h-4 w-4
                    shrink-0
                  "
                  aria-hidden="true"
                />

                <span>
                  {label}
                </span>
              </NavLink>
            )
          )}
        </nav>
      </>
    );


  return (
    <>
      <aside
        className="
          fixed inset-y-0
          left-0 z-40
          hidden w-64
          flex-col
          bg-slate-900
          lg:flex
        "
        aria-label="Desktop sidebar"
      >
        {renderSidebarContent()}
      </aside>

      {mobileOpen && (
        <div
          className="
            fixed inset-0
            z-50
            lg:hidden
          "
        >
          <button
            type="button"
            className="
              absolute inset-0
              bg-slate-950/50
            "
            aria-label="Close navigation"
            onClick={
              onMobileClose
            }
          />

          <aside
            className="
              relative z-10
              flex h-full
              w-72
              max-w-[85vw]
              flex-col
              bg-slate-900
              shadow-2xl
            "
            aria-label="Mobile navigation"
          >
            {renderSidebarContent(
              true
            )}
          </aside>
        </div>
      )}
    </>
  );
}


export default Sidebar;