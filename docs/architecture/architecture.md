# SupportFlow Architecture

## 1. Overview

SupportFlow is a full-stack support ticket escalation system built around clear separation of concerns, role-based workflows, SLA enforcement, background escalation processing, real-time notifications, and automated verification.

The architecture is designed so that:

- React handles the user interface.
- FastAPI exposes REST and WebSocket endpoints.
- Service classes contain business rules.
- Repository classes isolate persistence operations.
- SQLAlchemy manages ORM behavior.
- Alembic manages schema migrations.
- SQLite is used for local development and automated assessment environments.
- Background scheduler jobs process SLA conditions.
- Persistent notifications are combined with WebSocket delivery.
- pytest and Playwright verify backend and browser behavior.
- GitHub Actions executes the regression workflow in CI.

---

## 2. High-Level Architecture

```text
┌───────────────────────────────────────────────────────┐
│                    React Frontend                     │
│                                                       │
│ Requester │ Agent │ Admin │ Notifications │ Reports   │
│                                                       │
│ React Context │ Hooks │ Services │ Shared Components  │
└──────────────────────────┬────────────────────────────┘
                           │
                   REST API│WebSocket
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                    FastAPI Backend                    │
│                                                       │
│ Auth │ Users │ Tickets │ Responses │ SLA │ Reports    │
│ Assignment │ Escalation │ Audit │ Notifications      │
│ Dashboard │ Configuration │ WebSocket │ Health       │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                   Service Layer                       │
│                                                       │
│ Auth Service            Ticket Service                │
│ Assignment Service      SLA Service                   │
│ Escalation Service      Audit Service                 │
│ Notification Service    Dashboard Service             │
│ Report Service          Email / OTP Services          │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                 Repository Layer                      │
│                                                       │
│ Users │ Tickets │ SLA │ Audit │ Notifications         │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│              SQLAlchemy ORM + Alembic                 │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                       SQLite                          │
│                                                       │
│ Users │ Roles │ Tickets │ Responses │ Audit           │
│ SLA Config │ Notifications │ OTP │ App Config         │
└───────────────────────────────────────────────────────┘
```

---

## 3. Frontend Architecture

The frontend is built with React and Vite.

The application is divided into reusable UI components, page-level modules, services, context providers, hooks, constants, routing, and utility functions.

```text
frontend/src/
│
├── api/
│   └── apiClient.js
│
├── components/
│   ├── common/
│   ├── auth/
│   ├── tickets/
│   ├── users/
│   ├── dashboard/
│   ├── notifications/
│   ├── audit/
│   └── sla/
│
├── constants/
├── contexts/
├── hooks/
├── layouts/
├── pages/
├── routes/
├── services/
├── utils/
├── App.jsx
├── main.jsx
└── index.css
```

### Frontend Request Flow

```text
User Action
    ↓
React Page / Component
    ↓
Frontend Service
    ↓
Shared apiClient
    ↓
FastAPI endpoint
    ↓
Response
    ↓
React state update
```

The shared API client centralizes HTTP behavior such as authentication headers and base URL configuration.

### Frontend Role Separation

Frontend routes are separated into:

```text
Requester Pages
Agent Pages
Admin Pages
Shared Ticket Pages
Notifications
Profile
```

Protected routes prevent unauthenticated navigation, while role-specific routes prevent users from opening inappropriate role modules.

The frontend route guard is a user-experience layer only. Backend authorization remains the authoritative security boundary.

---

## 4. Backend Architecture

The backend uses a layered structure.

```text
API Routes
    ↓
Services
    ↓
Repositories
    ↓
Models
    ↓
Database
```

### API Layer

Routes are responsible for:

- HTTP request handling.
- Request validation.
- Authentication dependencies.
- Role authorization.
- Calling application services.
- Returning response schemas.

Typical route modules include:

```text
auth.py
users.py
tickets.py
ticket_responses.py
ticket_audit.py
sla.py
notifications.py
reports.py
dashboard.py
websocket.py
health.py
```

### Service Layer

Services contain application and business rules.

Important services include:

```text
auth_service.py
email_service.py
otp_service.py
user_service.py
ticket_service.py
assignment_service.py
ticket_response_service.py
status_service.py
sla_service.py
escalation_service.py
audit_service.py
notification_service.py
websocket_service.py
dashboard_service.py
report_service.py
```

Examples of business rules that belong in services include:

- Who can respond to a ticket.
- Which status transitions are valid.
- How SLA deadlines are evaluated.
- Which Agent is eligible for automatic reassignment.
- How capacity is enforced.
- When audit events should be created.
- Which users should receive notifications.

### Repository Layer

Repositories isolate database access from higher-level business logic.

Examples:

```text
user_repository.py
ticket_repository.py
audit_repository.py
notification_repository.py
sla_repository.py
```

This allows services to focus on business behavior instead of repeated SQLAlchemy query code.

---

## 5. Database Architecture

SupportFlow uses SQLAlchemy ORM.

Primary application entities include:

```text
Role
User
PasswordOTP
Ticket
TicketResponse
TicketAudit
SLAConfig
Notification
Application Configuration
```

### Database Relationship Concept

```text
Role
 │
 └────────► User
              │
              ├────────► Ticket as Requester
              │
              ├────────► Ticket as Assigned Agent
              │
              ├────────► TicketResponse
              │
              ├────────► TicketAudit actor
              │
              └────────► Notification

Ticket
 │
 ├────────► TicketResponse
 ├────────► TicketAudit
 └────────► Notification
```

SLA configuration is stored separately from individual tickets so SLA rules can be changed administratively without editing application code.

Application-level operational settings are also database-backed.

---

## 6. Database Migration Architecture

Alembic manages schema evolution.

```text
SQLAlchemy Model Change
        ↓
Alembic Revision
        ↓
Migration Script
        ↓
alembic upgrade head
        ↓
Database Schema Updated
```

This includes the later Stage-3 configuration extension:

```text
auto_reassign_on_escalation
```

Schema changes should be represented through migrations rather than manual database edits.

---

## 7. Authentication Architecture

SupportFlow uses JWT authentication for protected HTTP APIs.

```text
Login
  ↓
Validate email/password
  ↓
Generate JWT
  ↓
Frontend stores authenticated session
  ↓
apiClient attaches token
  ↓
FastAPI authentication dependency
  ↓
Current user resolved
```

The backend validates the current user's role and access to the requested resource.

### Password Security

Passwords are not stored in plaintext.

The authentication layer hashes passwords before persistence and verifies hashes during login.

### Forgot Password Architecture

```text
Forgot Password Request
        ↓
Generate OTP
        ↓
Store OTP record
        ↓
Send email
        ↓
User verifies OTP
        ↓
Reset password
```

The frontend provides dedicated Forgot Password, Verify OTP, and Reset Password pages.

---

## 8. Authorization Architecture

Authorization happens at two levels.

### Role-Level Authorization

```text
REQUESTER
AGENT
ADMIN
```

Examples:

```text
Requester → cannot manage users
Agent     → cannot change SLA configuration
Admin     → can manage system configuration
```

### Resource-Level Authorization

Role alone is not sufficient.

For example:

```text
Requester A
   ├── own ticket       → allowed
   └── Requester B ticket → denied
```

Similarly:

```text
Assigned Agent
   ├── assigned ticket        → allowed
   └── another Agent's ticket → denied
```

Backend tests and browser E2E tests verify both categories of authorization.

---

## 9. Ticket Processing Architecture

A simplified ticket lifecycle is:

```text
OPEN
  ↓
ASSIGNED
  ↓
IN_PROGRESS
  ↓
RESOLVED
  ↓
CLOSED
```

Additional lifecycle states include:

```text
REOPENED
ESCALATED
```

The backend status service validates permitted transitions.

The frontend only exposes actions appropriate to the current ticket status and current user's role.

---

## 10. SLA Architecture

SLA durations are database-backed.

Conceptually:

```text
Ticket Priority
      ↓
SLA Configuration
      ↓
Resolution Duration
      ↓
Ticket SLA Deadline
```

The critical boundary rule is:

```text
current_time >= sla_deadline
```

Therefore:

```text
Before deadline  → no escalation
At deadline      → escalation
After deadline   → escalation
```

Resolved and closed tickets are excluded.

Already-escalated tickets are also excluded from duplicate processing.

---

## 11. Scheduler Architecture

SupportFlow includes a background scheduler layer:

```text
scheduler/
├── scheduler.py
└── jobs.py
```

The scheduler periodically invokes SLA-related processing.

Conceptually:

```text
Scheduler
   ↓
Escalation Job
   ↓
Escalation Service
   ↓
Find overdue tickets
   ↓
Apply escalation rules
   ↓
Audit / Notification / Reassignment
```

Business logic remains in application services rather than inside the scheduling mechanism.

This keeps background execution thin and testable.

---

## 12. Escalation Architecture

The escalation service processes tickets that have crossed their SLA deadline.

```text
Active Ticket
      ↓
Deadline Check
      ↓
Overdue?
 ┌────┴────┐
 │         │
No        Yes
 │         │
Stop      ▼
       ESCALATED
           │
           ├── Audit
           ├── Notifications
           └── Auto-Reassignment Attempt
```

The service is designed to be idempotent.

Repeated scheduler execution must not repeatedly escalate the same ticket.

---

## 13. Automatic Reassignment Architecture

The Stage-3 enhancement introduces automatic SLA-based reassignment.

```text
SLA Breach
   ↓
ESCALATED
   ↓
auto_reassign_on_escalation ?
   ↓
Find replacement Agent
```

Candidate filtering:

```text
All users
   ↓
Role = AGENT
   ↓
Active only
   ↓
Exclude current Agent
   ↓
Below workload capacity
   ↓
Calculate active workload
   ↓
Sort workload ASC
   ↓
Sort Agent ID ASC
   ↓
Choose first candidate
```

If a candidate exists:

```text
Current Agent
    ↓
Ticket reassigned
    ↓
Replacement Agent
```

The process also records appropriate audit events and notifications.

If no candidate exists, the ticket remains assigned to its original Agent while escalation still succeeds.

This preserves the core SLA guarantee.

---

## 14. Audit Architecture

Important business actions generate audit records.

```text
Business Event
     ↓
Audit Service
     ↓
TicketAudit
     ↓
Audit Timeline
```

Examples include:

```text
Ticket creation
Assignment
Reassignment
Start work
Priority change
SLA escalation
Automatic reassignment
Resolution
Reopen
Close
```

The audit trail allows the current ticket state to be explained through historical actions.

---

## 15. Notification Architecture

Persistent notifications are stored in the database.

```text
Business Event
      ↓
Notification Service
      ↓
Notification Record
```

This ensures notifications remain available even if the user is offline.

The frontend retrieves persisted notifications through REST endpoints.

---

## 16. WebSocket Architecture

WebSockets add real-time delivery on top of persistent notifications.

```text
Business Event
       ↓
Notification Service
       ↓
Database Notification
       ↓
WebSocket Manager
       ↓
Authenticated Browser
       ↓
React Notification Context
       ↓
Toast / Bell / Unread Counter
```

If the browser is disconnected:

```text
Notification still stored
        ↓
Browser reconnects
        ↓
REST refresh recovers notification
```

This architecture combines reliability with live user experience.

---

## 17. WebSocket Connection Management

The frontend maintains an authenticated WebSocket connection after login.

It supports:

- Connection establishment.
- PING/PONG health messages.
- Reconnect attempts.
- Logout cleanup.
- Unread-count refresh after reconnect.

The backend WebSocket manager supports active user connections and routes notifications to the intended user.

---

## 18. Reporting Architecture

Reports are exposed through backend report APIs.

The frontend can request operational summaries and download CSV exports.

```text
Admin
  ↓
Report Page
  ↓
reportService.js
  ↓
FastAPI Reports API
  ↓
Report Service
  ↓
Database Queries
  ↓
Summary / CSV
```

Report access is restricted to Admin users.

---

## 19. Error Handling Architecture

SupportFlow centralizes backend exception handling and frontend API error parsing.

Conceptually:

```text
Application Error
      ↓
FastAPI Exception Handler
      ↓
Consistent HTTP Response
      ↓
apiClient / apiError utility
      ↓
Toast / ErrorState
```

The frontend does not expose backend stack traces to end users.

---

## 20. Test Architecture

SupportFlow uses multiple testing layers.

```text
                 Application
                     │
       ┌─────────────┴─────────────┐
       │                           │
       ▼                           ▼
Backend Tests                 Browser Tests
pytest                        Playwright
       │                           │
       ▼                           ▼
Business Rules              Real User Workflows
Security                    React + FastAPI
SLA Boundaries              WebSockets
Services                    Role Navigation
APIs                        Privacy
```

### Backend Suite

Current verified result:

```text
98 passed
```

### Browser E2E Suite

Current verified result:

```text
24 passed
```

---

## 21. Test Database Architecture

Three SQLite files are intentionally separated.

```text
supportflow.db
      │
      ▼
Development / Swagger / Postman


test_supportflow.db
      │
      ▼
pytest


supportflow_e2e.db
      │
      ▼
FastAPI + Playwright
```

This prevents automated backend fixtures from corrupting or resetting browser E2E state.

---

## 22. CI Architecture

GitHub Actions verifies the application in a clean environment.

```text
Push / Pull Request
        │
        ├──────────────────────┐
        │                      │
        ▼                      ▼
Backend Tests            Frontend Checks
Python 3.11              Node.js
Dependencies             npm ci
Ruff                     ESLint
pytest                    Vite Build
        │                      │
        └──────────┬───────────┘
                   ▼
              Playwright E2E
                   │
                   ├── Fresh E2E DB
                   ├── Alembic migrations
                   ├── E2E seed
                   ├── FastAPI
                   ├── Vite
                   ├── Chromium
                   └── 24 tests
```

Playwright reports are uploaded as GitHub Actions artifacts.

---

## 23. Deployment Considerations

The current architecture is intentionally simple for assessment and local reproducibility.

For larger production environments, the architecture could evolve toward:

```text
React static hosting

FastAPI container instances

PostgreSQL

Redis pub/sub for WebSocket scaling

Distributed task workers

Managed email provider

Centralized logs / metrics / tracing
```

The current service and repository separation makes these changes easier because application business logic is not tightly coupled to SQLite or a single deployment environment.

---

## 24. Architecture Summary

SupportFlow follows several key architectural principles:

- Clear frontend/backend separation.
- Layered backend design.
- Centralized business-rule services.
- Repository-based persistence access.
- Database-backed operational configuration.
- Backend-enforced RBAC.
- Resource-level authorization.
- Idempotent SLA escalation.
- Reusable assignment logic.
- Persistent plus real-time notifications.
- Separate test databases.
- Multi-layer automated verification.
- CI verification on clean infrastructure.

The architecture supports both the original support-ticket requirements and the later AI-assisted Stage-3 automatic-reassignment enhancement without requiring major structural changes.
