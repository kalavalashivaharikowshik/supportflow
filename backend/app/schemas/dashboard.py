from datetime import datetime

from pydantic import BaseModel


class StatusCount(BaseModel):
    status: str
    count: int


class PriorityCount(BaseModel):
    priority: str
    count: int


class DashboardTicketItem(BaseModel):
    id: int
    ticket_number: str
    title: str
    priority: str
    status: str
    requester_id: int
    assigned_agent_id: int | None
    sla_deadline: datetime
    is_escalated: bool
    created_at: datetime


class RequesterDashboardResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    active_tickets: int
    resolved_tickets: int
    closed_tickets: int
    escalated_tickets: int
    sla_at_risk_tickets: int

    status_counts: list[StatusCount]
    priority_counts: list[PriorityCount]

    recent_tickets: list[DashboardTicketItem]


class AgentDashboardResponse(BaseModel):
    total_assigned_tickets: int
    active_tickets: int
    assigned_tickets: int
    in_progress_tickets: int
    escalated_tickets: int
    resolved_tickets: int
    sla_at_risk_tickets: int

    status_counts: list[StatusCount]
    priority_counts: list[PriorityCount]

    average_first_response_minutes: float | None
    average_resolution_minutes: float | None

    recent_tickets: list[DashboardTicketItem]


class AgentWorkloadItem(BaseModel):
    agent_id: int
    full_name: str
    email: str

    total_assigned: int
    active_tickets: int
    escalated_tickets: int


class AdminDashboardResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    active_tickets: int
    resolved_tickets: int
    closed_tickets: int

    unassigned_tickets: int
    escalated_tickets: int
    sla_at_risk_tickets: int

    total_requesters: int
    total_agents: int
    active_agents: int

    status_counts: list[StatusCount]
    priority_counts: list[PriorityCount]

    average_first_response_minutes: float | None
    average_resolution_minutes: float | None

    recent_tickets: list[DashboardTicketItem]
    recent_escalations: list[DashboardTicketItem]
    agent_workload: list[AgentWorkloadItem]