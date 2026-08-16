from enum import StrEnum


class UserRole(StrEnum):
    REQUESTER = "REQUESTER"
    AGENT = "AGENT"
    ADMIN = "ADMIN"


class TicketPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketStatus(StrEnum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    REOPENED = "REOPENED"


class TicketCategory(StrEnum):
    TECHNICAL = "TECHNICAL"
    ACCESS = "ACCESS"
    ACCOUNT = "ACCOUNT"
    BILLING = "BILLING"
    GENERAL = "GENERAL"

AGENT_STATUS_TRANSITIONS = {
    TicketStatus.ASSIGNED: {
        TicketStatus.IN_PROGRESS,
    },
    TicketStatus.REOPENED: {
        TicketStatus.IN_PROGRESS,
    },
}


REQUESTER_STATUS_TRANSITIONS = {
    TicketStatus.RESOLVED: {
        TicketStatus.CLOSED,
        TicketStatus.REOPENED,
    },
}

class AuditEventType(StrEnum):
    TICKET_CREATED = "TICKET_CREATED"

    TICKET_ASSIGNED = "TICKET_ASSIGNED"
    TICKET_REASSIGNED = "TICKET_REASSIGNED"

    PRIORITY_CHANGED = "PRIORITY_CHANGED"

    RESPONSE_ADDED = "RESPONSE_ADDED"
    INTERNAL_NOTE_ADDED = "INTERNAL_NOTE_ADDED"

    WORK_STARTED = "WORK_STARTED"

    SLA_ESCALATED = "SLA_ESCALATED"

    TICKET_RESOLVED = "TICKET_RESOLVED"
    TICKET_REOPENED = "TICKET_REOPENED"
    TICKET_CLOSED = "TICKET_CLOSED"

class NotificationType(StrEnum):
    TICKET_ASSIGNED = "TICKET_ASSIGNED"
    TICKET_REASSIGNED = "TICKET_REASSIGNED"

    TICKET_RESPONSE = "TICKET_RESPONSE"

    SLA_AT_RISK = "SLA_AT_RISK"
    SLA_ESCALATED = "SLA_ESCALATED"

    TICKET_RESOLVED = "TICKET_RESOLVED"
    TICKET_REOPENED = "TICKET_REOPENED"
    TICKET_CLOSED = "TICKET_CLOSED"

class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class TicketSortField(StrEnum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    SLA_DEADLINE = "sla_deadline"
    PRIORITY = "priority"
    STATUS = "status"
    TICKET_NUMBER = "ticket_number"