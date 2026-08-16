import { ROLES } from "./roles";


export const ROUTES = Object.freeze({
  LOGIN: "/login",
  REGISTER: "/register",

  FORGOT_PASSWORD:
    "/forgot-password",

  VERIFY_OTP:
    "/verify-otp",

  RESET_PASSWORD:
    "/reset-password",

  PROFILE:
    "/profile",

  REQUESTER_DASHBOARD:
    "/requester",

  REQUESTER_TICKETS:
    "/requester/tickets",

  CREATE_TICKET:
    "/requester/tickets/create",

  TICKET_DETAILS:
    "/tickets/:ticketId",

  AGENT_DASHBOARD:
    "/agent",

  AGENT_TICKETS:
    "/agent/tickets",

  AGENT_ESCALATED:
    "/agent/escalated",

  ADMIN_DASHBOARD:
    "/admin",

  ADMIN_TICKETS:
    "/admin/tickets",

  ADMIN_USERS:
    "/admin/users",

  ADMIN_SLA:
    "/admin/sla",

  ADMIN_CONFIG:
    "/admin/config",

  ADMIN_REPORTS:
    "/admin/reports",

  NOTIFICATIONS:
    "/notifications",

  UNAUTHORIZED:
    "/unauthorized",
});


export const getDashboardRoute = (role) => {
  switch (role) {
    case ROLES.REQUESTER:
      return ROUTES.REQUESTER_DASHBOARD;

    case ROLES.AGENT:
      return ROUTES.AGENT_DASHBOARD;

    case ROLES.ADMIN:
      return ROUTES.ADMIN_DASHBOARD;

    default:
      return ROUTES.LOGIN;
  }
};

export const getTicketDetailsRoute = (
  ticketId
) => {
  return `/tickets/${ticketId}`;
};