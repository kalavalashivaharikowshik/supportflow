import Badge from "../common/Badge";

import {
  TICKET_STATUS,
} from "../../constants/ticketStatus";


const STATUS_VARIANTS = {
  [TICKET_STATUS.OPEN]:
    "info",

  [TICKET_STATUS.ASSIGNED]:
    "default",

  [TICKET_STATUS.IN_PROGRESS]:
    "warning",

  [TICKET_STATUS.ESCALATED]:
    "danger",

  [TICKET_STATUS.RESOLVED]:
    "success",

  [TICKET_STATUS.CLOSED]:
    "default",

  [TICKET_STATUS.REOPENED]:
    "warning",
};


const STATUS_LABELS = {
  [TICKET_STATUS.OPEN]:
    "Open",

  [TICKET_STATUS.ASSIGNED]:
    "Assigned",

  [TICKET_STATUS.IN_PROGRESS]:
    "In Progress",

  [TICKET_STATUS.ESCALATED]:
    "Escalated",

  [TICKET_STATUS.RESOLVED]:
    "Resolved",

  [TICKET_STATUS.CLOSED]:
    "Closed",

  [TICKET_STATUS.REOPENED]:
    "Reopened",
};


function TicketStatusBadge({
  status,
}) {
  const label =
    STATUS_LABELS[
      status
    ] ?? "Unknown";

  return (
    <Badge
      variant={
        STATUS_VARIANTS[
          status
        ] ?? "default"
      }
    >
      {label}
    </Badge>
  );
}


export default TicketStatusBadge;