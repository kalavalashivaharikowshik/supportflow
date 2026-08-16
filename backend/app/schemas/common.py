from datetime import datetime

from pydantic import BaseModel


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int

class TicketReportSummary(BaseModel):
    total_tickets: int
    active_tickets: int
    resolved_tickets: int
    closed_tickets: int
    escalated_tickets: int
    sla_breached_tickets: int


class AgentPerformanceReportItem(BaseModel):
    agent_id: int
    full_name: str
    email: str

    total_assigned: int
    active_tickets: int
    resolved_tickets: int
    escalated_tickets: int

    average_first_response_minutes: float | None
    average_resolution_minutes: float | None


class SLAReportItem(BaseModel):
    ticket_id: int
    ticket_number: str
    title: str
    priority: str
    status: str

    requester_id: int
    assigned_agent_id: int | None

    created_at: datetime
    sla_deadline: datetime
    escalated_at: datetime | None
    resolved_at: datetime | None

    is_escalated: bool