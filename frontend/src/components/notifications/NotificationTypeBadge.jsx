import Badge from "../common/Badge";


const TYPE_VARIANTS = {
  TICKET_ASSIGNED:
    "info",

  TICKET_REASSIGNED:
    "warning",

  TICKET_RESPONSE:
    "info",

  TICKET_RESOLVED:
    "success",

  TICKET_REOPENED:
    "warning",

  TICKET_CLOSED:
    "default",

  SLA_AT_RISK:
    "warning",

  SLA_ESCALATED:
    "danger",
};


function NotificationTypeBadge({
  type,
}) {
  if (!type) {
    return null;
  }

  return (
    <Badge
      variant={
        TYPE_VARIANTS[type] ??
        "default"
      }
    >
      {type.replaceAll(
        "_",
        " "
      )}
    </Badge>
  );
}


export default NotificationTypeBadge;