SupportFlow — AI-Assisted Support Ticket Escalation System

""SupportFlow CI" (https://github.com/kalavalashivaharikowshik/supportflow/actions/workflows/ci.yml/badge.svg)" (https://github.com/kalavalashivaharikowshik/supportflow/actions/workflows/ci.yml)

SupportFlow is a full-stack support ticket management platform designed to prevent high-priority support requests from silently exceeding their service-level agreement (SLA) deadlines.

The platform provides dedicated workflows for Requesters, Agents, and Administrators, automatically monitors SLA deadlines, escalates overdue tickets, maintains a structured audit trail, and delivers both persistent and real-time WebSocket notifications.

SupportFlow also includes an AI-assisted Stage-3 enhancement for SLA-based automatic ticket reassignment. When an assigned ticket breaches its SLA, the system can automatically move it to the least-loaded eligible Agent while preserving escalation, audit, notification, workload-capacity, and idempotency rules.

---

Problem Statement

In many organizations, customer or internal support requests are managed through ticket queues. A common operational problem is that high-priority tickets can remain unattended or unresolved beyond their expected response window.

Without automated SLA enforcement, urgent tickets may depend entirely on someone manually noticing that they are overdue.

This creates several business problems:

- SLA commitments may be breached.
- High-priority tickets may remain with overloaded Agents.
- Supervisors must manually monitor overdue work.
- Priority labels may have no enforced operational consequence.
- Assignment, escalation, response, and resolution history may not be consistently auditable.
- Internal support information may accidentally be exposed to Requesters if access boundaries are poorly enforced.

SupportFlow addresses these problems by making SLA enforcement part of the application itself.

Each ticket receives an SLA deadline based on its configured priority. The system monitors active tickets, detects SLA breaches, escalates overdue tickets, records audit events, creates notifications, and can automatically reassign breached tickets to a more suitable Agent.

---

Project Goals

SupportFlow was designed around the following goals:

1. Allow Requesters to create and track support tickets.
2. Allow Agents to manage assigned support work.
3. Allow Administrators to supervise tickets, users, SLA configuration, workload, and reports.
4. Enforce role-based authorization at both API and frontend levels.
5. Calculate and enforce SLA deadlines based on ticket priority.
6. Automatically detect and escalate overdue tickets.
7. Maintain a structured audit trail of important ticket events.
8. Support public ticket conversations and private internal support notes.
9. Deliver persistent notifications and real-time WebSocket notifications.
10. Support configurable operational behavior through Admin settings.
11. Automatically reassign SLA-breached tickets to eligible Agents when configured.
12. Validate the application through backend regression tests and real browser E2E tests.
13. Run automated verification through GitHub Actions CI.
14. Demonstrate an AI-assisted build → test → diagnose → fix engineering workflow.

---

Key Features

Requester

- Secure registration and login.
- Email OTP-based forgot-password and reset-password workflow.
- Create support tickets with category and priority.
- View personal tickets only.
- Search, filter, sort, and paginate personal tickets.
- View ticket status, priority, assignment, and SLA information.
- View SLA deadline and SLA-risk information.
- Participate in public ticket conversations.
- View permitted ticket audit activity.
- Close resolved tickets.
- Reopen resolved tickets when enabled by Admin configuration.
- Receive persistent notifications.
- Receive real-time WebSocket notifications.
- View and update profile information.
- Change password securely.

Agent

- Secure Agent authentication.
- View Agent dashboard and workload metrics.
- View assigned tickets.
- View escalated tickets.
- Search, filter, sort, and paginate assigned work.
- Start work on assigned tickets.
- Send public responses to Requesters.
- Add internal notes visible only to support staff.
- View internal ticket activity.
- Resolve active and escalated tickets.
- Provide a resolution summary.
- View SLA status and ticket history.
- Receive ticket assignment and reassignment notifications.
- Receive Requester-response notifications.
- Receive reopen and close notifications.
- Receive SLA warning and escalation notifications.

Administrator

- View system-wide dashboard metrics.
- Monitor total, active, unassigned, resolved, at-risk, and escalated tickets.
- Monitor Agent workload.
- View all tickets.
- Search by ticket information, Requester name, and Requester email.
- Filter tickets by priority, status, assignment state, and SLA state.
- Assign tickets to Agents.
- Reassign tickets between Agents.
- Change ticket priority.
- View complete ticket audit history.
- Add public responses when allowed by configuration.
- Add internal support notes.
- Manage users.
- Activate and deactivate users.
- Create Agent accounts.
- Configure SLA durations.
- Configure operational application settings.
- Enable or disable Requester reopen behavior.
- Enable or disable Admin public responses.
- Enable or disable persistent notifications.
- Enable or disable WebSocket notifications.
- Configure Agent workload capacity.
- Enable or disable automatic SLA reassignment.
- View reports.
- Export ticket, SLA, and Agent-performance CSV reports.

Platform Capabilities

- JWT-based authentication.
- Secure password hashing.
- Role-based access control.
- SQLAlchemy ORM.
- Alembic database migrations.
- Database-backed SLA configuration.
- Automatic SLA monitoring.
- Automatic SLA escalation.
- Automatic least-loaded Agent reassignment.
- Deterministic Agent selection.
- Workload-capacity enforcement.
- Escalation idempotency.
- Ticket lifecycle validation.
- Structured audit-event generation.
- Persistent database notifications.
- Live WebSocket notifications.
- Search, filtering, sorting, and pagination.
- Centralized error handling.
- Structured logging.
- Responsive React interface.
- Mobile navigation.
- Automated backend testing with pytest.
- Browser E2E testing with Playwright.
- Python linting with Ruff.
- Frontend linting with ESLint.
- Production frontend build verification.
- GitHub Actions continuous integration.

---

Technology Stack

Layer| Technology
Frontend| React + Vite
Styling| Tailwind CSS
Backend| FastAPI
ORM| SQLAlchemy
Database Migrations| Alembic
Development Database| SQLite
Authentication| JWT
Password Security| Passlib / bcrypt
Configuration| Pydantic Settings / environment variables
API Communication| REST
Real-Time Communication| WebSockets
Backend Testing| pytest
Browser E2E Testing| Playwright
Python Code Quality| Ruff
Frontend Code Quality| ESLint
CI/CD Verification| GitHub Actions
AI-Assisted Development| ChatGPT

---

System Architecture

SupportFlow follows a layered full-stack architecture.

┌───────────────────────────────────────────────────────┐
│                    React + Vite                       │
│                                                       │
│  Requester UI │ Agent UI │ Admin UI │ Notifications  │
└──────────────────────────┬────────────────────────────┘
                           │
                  REST API │ WebSocket
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                       FastAPI                         │
│                                                       │
│ Auth │ Users │ Tickets │ Responses │ SLA │ Reports    │
│ Assignment │ Escalation │ Audit │ Notifications      │
│ Dashboard │ Admin Configuration │ WebSocket          │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                 SQLAlchemy ORM                        │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                       SQLite                          │
│                                                       │
│ Users │ Roles │ Tickets │ Responses │ Audit Events    │
│ SLA Config │ Notifications │ Password OTP │ App Config│
└───────────────────────────────────────────────────────┘

Backend Layering

The backend separates HTTP handling, business logic, persistence, scheduling, and shared utilities.

API Routes
    ↓
Services
    ↓
Repositories
    ↓
SQLAlchemy Models
    ↓
Database

Examples:

Ticket API
    ↓
Ticket Service
    ↓
Ticket Repository
    ↓
Ticket Model

and:

Scheduler
    ↓
Escalation Service
    ↓
Assignment Service
    ↓
Audit / Notification Services
    ↓
Database

Frontend Layering

The React frontend separates pages, reusable components, API services, shared contexts, hooks, and routing.

Pages
    ↓
Reusable Components
    ↓
Services
    ↓
Shared API Client
    ↓
FastAPI

Authentication and notification state are managed using React Context, while reusable hooks manage authentication, WebSocket connectivity, notifications, and debounced search behavior.

---

User Roles and Permissions

SupportFlow uses three primary roles.

Capability| Requester| Agent| Admin
Register publicly| ✅| ❌| ❌
Create ticket| ✅| ❌| ❌
View own tickets| ✅| ❌| ❌
View assigned tickets| ❌| ✅| ✅
View all tickets| ❌| ❌| ✅
Start work| ❌| ✅| ❌
Public response| ✅| ✅| Configurable
Internal note| ❌| ✅| ✅
Resolve ticket| ❌| ✅| ❌
Close resolved ticket| ✅| ❌| ❌
Reopen resolved ticket| Configurable| ❌| ❌
Assign ticket| ❌| ❌| ✅
Reassign ticket| ❌| ❌| ✅
Change priority| ❌| ❌| ✅
Manage users| ❌| ❌| ✅
Configure SLA| ❌| ❌| ✅
Configure application| ❌| ❌| ✅
View reports| ❌| ❌| ✅
Export reports| ❌| ❌| ✅
Receive notifications| ✅| ✅| ✅

Authorization is enforced by the backend even when the frontend hides an action.

Examples:

- A Requester cannot access another Requester's ticket by manually changing the URL.
- An unassigned Agent cannot interact with another Agent's assigned ticket.
- A Requester cannot create an internal note through a direct API call.
- Requesters and Agents cannot access Admin APIs.
- Internal notes are filtered by the backend before Requester conversation data is returned.

The frontend also uses protected and role-specific routes, but backend authorization remains the primary security boundary.

---

Ticket Lifecycle

SupportFlow enforces controlled ticket status transitions rather than allowing arbitrary status changes.

Standard Workflow

OPEN
  │
  │ Admin assigns Agent
  ▼
ASSIGNED
  │
  │ Agent starts work
  ▼
IN_PROGRESS
  │
  │ Agent resolves ticket
  ▼
RESOLVED
  │
  ├── Requester closes ─────────► CLOSED
  │
  └── Requester reopens ────────► REOPENED
                                      │
                                      │ Agent continues work
                                      ▼
                                  IN_PROGRESS

Backend business rules validate status changes.

Examples:

- A ticket cannot be resolved through an invalid lifecycle transition.
- Closed tickets cannot receive new responses.
- Only appropriate roles can perform workflow actions.
- A resolved ticket can be closed by its Requester.
- Requester reopen behavior can be controlled through Admin configuration.

SLA Escalation Path

Active tickets can also move through the escalation flow:

ASSIGNED / IN_PROGRESS / REOPENED
              │
              │ SLA deadline reached
              ▼
          ESCALATED
              │
              │ Agent resolves
              ▼
           RESOLVED
              │
              ▼
            CLOSED

Escalation identifies that an active ticket has violated its configured SLA and requires additional operational attention.

---

SLA and Escalation Engine

SLA enforcement is one of the core business features of SupportFlow.

Priority-Based SLA Configuration

SLA durations are stored in the database and managed through the Admin interface instead of being permanently hardcoded into application logic.

Ticket Created
      │
      ├── Priority
      │
      ▼
SLA Configuration
      │
      ▼
SLA Deadline

SLA Boundary Rule

SupportFlow treats the deadline as an inclusive boundary.

current_time >= sla_deadline

Therefore:

Time| Result
Before deadline| Not breached
Exactly at deadline| Breached
After deadline| Breached

This behavior is explicitly protected by automated regression tests.

Automatic Escalation

Active Ticket
     │
     ▼
Check SLA Deadline
     │
     ├── Not overdue ─────────► No action
     │
     └── Overdue
             │
             ▼
         ESCALATED
             │
             ├── Audit event
             ├── Notification
             └── Optional automatic reassignment

Escalation Safety Rules

SupportFlow verifies that:

- Tickets before the SLA deadline are not escalated.
- Tickets exactly at the SLA deadline are considered breached.
- Tickets after the SLA deadline are escalated.
- Resolved tickets are not escalated.
- Closed tickets are not escalated.
- Already-escalated tickets are not repeatedly escalated.
- Repeated escalation processing remains idempotent.

---

SLA-Based Automatic Reassignment

SupportFlow extends normal SLA escalation with configurable automatic Agent reassignment.

When an assigned ticket breaches its SLA, the system may attempt to move it to another eligible Agent.

Reassignment Flow

Ticket breaches SLA
        │
        ▼
Ticket becomes ESCALATED
        │
        ▼
Is automatic reassignment enabled?
        │
        ├── No ───────────────► Keep current Agent
        │
        └── Yes
              │
              ▼
      Find eligible Agents
              │
              ▼
      Exclude current Agent
              │
              ▼
      Exclude inactive Agents
              │
              ▼
      Apply workload capacity
              │
              ▼
      Rank by active workload
              │
              ▼
      Lowest workload wins
              │
              ▼
      Agent ID breaks ties
              │
        ┌─────┴─────┐
        │           │
   Candidate     No candidate
        │           │
        ▼           ▼
    Reassign     Keep current
      ticket        Agent
        │           │
        └─────┬─────┘
              ▼
      Escalation succeeds

Agent Eligibility Rules

A replacement Agent must:

- Have the Agent role.
- Be active.
- Not be the ticket's current assigned Agent.
- Be below the configured maximum active-ticket capacity.

Among eligible Agents, SupportFlow chooses the Agent with the lowest active workload.

If multiple Agents have the same workload, the lowest Agent ID is used as a deterministic tie-breaker.

No-Replacement Fallback

Automatic reassignment is an enhancement to escalation, not a requirement for escalation to succeed.

If no eligible replacement exists:

Ticket status         → ESCALATED
Assigned Agent        → unchanged
Escalation processing → successful

Configuration

Administrators can control this behavior with:

auto_reassign_on_escalation

When disabled, the ticket is escalated normally without changing its Agent.

Idempotency

Once a ticket has already been escalated and processed, repeated scheduler checks do not continuously reassign it.

---

Audit Trail

SupportFlow maintains a structured audit history for important ticket events.

Examples include:

- Ticket creation.
- Assignment.
- Reassignment.
- Status transitions.
- Public responses where applicable.
- Internal support activity where applicable.
- Priority changes.
- SLA escalation.
- Automatic SLA reassignment.
- Resolution.
- Reopen activity.
- Close activity.

Example Audit History

Ticket created
      ↓
Assigned to Agent A
      ↓
Agent started work
      ↓
SLA breached
      ↓
Ticket escalated
      ↓
Automatically reassigned
Agent A → Agent B

Automatic Reassignment Auditing

A successful automatic SLA reassignment preserves both events:

SLA_ESCALATED
TICKET_AUTO_REASSIGNED

The reassignment event does not replace the escalation event.

Automated tests verify that both audit events are created.

---

Notifications and Real-Time WebSockets

SupportFlow combines:

Persistent Database Notifications
              +
      Real-Time WebSocket Delivery

This means notifications remain available after refresh or reconnect, while connected users also receive updates immediately.

Notification Architecture

Business Event
     │
     ▼
Notification Service
     │
     ├──────────────► Database
     │                 │
     │                 ▼
     │           Notification History
     │
     ▼
WebSocket Service
     │
     ▼
Connected Browser
     │
     ▼
React Notification Context
     │
     ▼
Notification UI

Example: Ticket Assignment

Admin assigns ticket
        │
        ▼
Assignment Service
        │
        ▼
Agent notification created
        │
        ├── Stored in database
        │
        └── Pushed through WebSocket
                         │
                         ▼
                Agent receives update
                without page refresh

The Playwright E2E suite verifies:

agent receives live assignment notification without refresh

Automatic Reassignment Notifications

When automatic SLA reassignment succeeds:

Previous Agent

Receives a notification that the overdue ticket was reassigned.

New Agent

Receives a notification that an escalated ticket was assigned to them.

Unrelated Agent

Receives no reassignment notification.

Dedicated backend tests verify these cases.

Internal Note Privacy

Internal support notes must never be exposed to Requesters.

SupportFlow enforces this in backend authorization and response filtering rather than relying only on frontend hiding.

Backend tests and Playwright browser tests verify internal-note privacy.

WebSocket Authentication

WebSocket connections require authentication so that live events are delivered to the correct application user.

Dedicated backend tests cover WebSocket authentication.

---

Project Structure

supportflow/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── websocket/
│   │   ├── scheduler/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── admin/
│   │   ├── audit/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── escalation/
│   │   ├── notifications/
│   │   ├── reports/
│   │   ├── security/
│   │   ├── sla/
│   │   ├── tickets/
│   │   ├── users/
│   │   └── websocket/
│   │
│   ├── alembic.ini
│   ├── pytest.ini
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── constants/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── e2e/
│   │   ├── admin/
│   │   ├── agent/
│   │   ├── auth/
│   │   ├── notifications/
│   │   ├── requester/
│   │   ├── responsive/
│   │   └── security/
│   │
│   ├── package.json
│   ├── playwright.config.js
│   ├── eslint.config.js
│   └── vite.config.js
│
├── docs/
│   └── screenshots/
│
└── README.md

The structure keeps API handling, business logic, persistence, UI code, automated testing, and CI configuration separated.

---

Environment Configuration

SupportFlow uses environment variables instead of hardcoding environment-specific values or secrets.
Example files are provided through:
backend/.env.example
frontend/.env.example
Actual .env files should not be committed.
Backend
Create:
backend/.env
from:
backend/.env.example
The backend environment includes settings such as:
Database connection.
JWT/security configuration.
CORS configuration.
Frontend URL.
Email/SMTP configuration.
Use the exact variable names from the committed .env.example and backend settings model.
Frontend
Create:
frontend/.env
from:
frontend/.env.example
The frontend environment defines the API/WebSocket locations used by Vite.
Never Commit
.env
Production JWT secrets.
SMTP passwords.
Database credentials.
Private API secrets.
Runtime SQLite databases.
Local Development Setup
Prerequisites
Install:
Python 3.11+
Node.js and npm
Git
1. Clone the Repository
git clone https://github.com/kalavalashivaharikowshik/supportflow.git
cd supportflow
2. Create the Backend Virtual Environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install Backend Dependencies
pip install -r requirements.txt
4. Configure Backend Environment
Copy-Item .env.example .env
Review .env and provide the required local values.
5. Apply Database Migrations
alembic upgrade head
Check the active migration:
alembic current
View migration history:
alembic history
Schema evolution should be represented through Alembic migrations.
6. Start the Backend
From:
supportflow/backend
run:
python -m uvicorn app.main:app --reload
Backend:
http://127.0.0.1:8000
Swagger:
http://127.0.0.1:8000/docs
7. Install Frontend Dependencies
Open a second terminal:
cd frontend
npm install
8. Start the Frontend
npm run dev
For the host used by browser tests:
npm run dev -- --host 127.0.0.1
Frontend:
http://127.0.0.1:5173
Local Architecture
Browser
   │
   ▼
React / Vite :5173
   │
   │ REST + WebSocket
   ▼
FastAPI :8000
   │
   ▼
SQLite
Database Isolation
SupportFlow separates databases by purpose.
SupportFlow
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
 supportflow.db   test_supportflow.db   supportflow_e2e.db
       │                │                │
       ▼                ▼                ▼
 Development         pytest          Playwright E2E
Development Database
supportflow.db
Used for:
Normal local application use.
Swagger testing.
Postman testing.
Manual frontend/backend development.
Backend Test Database
test_supportflow.db
Used only by pytest.
This keeps automated backend tests isolated from development data.
Browser E2E Database
supportflow_e2e.db
Used by the running FastAPI server during Playwright browser tests.
It contains deterministic E2E users and state required for browser workflows.
Keeping pytest and Playwright databases separate prevents fixture-level backend test behavior from interfering with persistent browser-test workflows.
Runtime SQLite files should not be committed to Git.
API Verification
Swagger
FastAPI interactive API documentation is available at:
http://127.0.0.1:8000/docs
Swagger was used during development to inspect endpoint schemas, authorization requirements, requests, and responses.
Postman
Backend APIs were also verified incrementally through Postman.
The development workflow followed:
Implement API
     ↓
Start FastAPI
     ↓
Verify through Swagger / Postman
     ↓
Check status and response
     ↓
Add automated regression coverage
Automated Testing
SupportFlow uses separate backend and browser test layers.
Backend Regression Testing — pytest
From:
supportflow/backend
activate the virtual environment and run:
pytest -v
Current verified result:
98 passed
The backend suite covers:
Registration.
Authentication.
JWT-protected endpoints.
Role-based access control.
User management.
Dashboard authorization.
Ticket creation.
Ticket ownership.
Assignment.
Public responses.
Internal-note privacy.
Ticket lifecycle.
SLA configuration.
SLA boundary behavior.
Escalation.
Escalation idempotency.
Automatic SLA reassignment.
Current-Agent exclusion.
Inactive-Agent exclusion.
Agent workload capacity.
No-replacement fallback.
Reassignment configuration.
Reassignment idempotency.
Reassignment audit behavior.
Old/new Agent notifications.
Unrelated-Agent notification isolation.
Reports.
CSV export.
WebSocket authentication.
Backend Linting
Run:
ruff check app
Current verified result:
All checks passed!                Browser E2E Testing — Playwright
Playwright exercises the application through a real Chromium browser while the frontend and backend run together.
From:
supportflow/frontend
run:
npx playwright test
Current verified result:
24 passed
The browser suite covers workflows including:
Successful Requester login.
Invalid password handling.
Unauthenticated protected-route redirection.
Public Requester registration.
Critical-ticket creation.
Ticket search and filtering.
Admin ticket assignment.
Admin application configuration.
Admin SLA configuration.
Admin user activation/deactivation.
Agent start-work workflow.
Agent ticket resolution.
Requester closure of a resolved ticket.
Complete cross-role ticket lifecycle.
Live WebSocket assignment notification without refresh.
Internal-note privacy.
Requester/Admin/Agent route isolation.
Cross-Requester ticket access protection.
Mobile navigation behavior.
Playwright runs with one worker for deterministic database-mutating E2E workflows.
Frontend Quality Verification
Run ESLint:
npm run lint
Create a production build:
npm run build
Current verified local baseline:
Backend pytest       98 / 98 passed
Backend Ruff         passed
Frontend ESLint      passed
Frontend Vite build  passed
Playwright E2E       24 / 24 passed
Full Local E2E Verification
Playwright must run against the dedicated E2E database rather than the pytest database.
Terminal 1 — Backend
cd backend
.\venv\Scripts\Activate.ps1

$env:DATABASE_URL="sqlite:///./supportflow_e2e.db"
$env:CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
$env:FRONTEND_URL="http://127.0.0.1:5173"

python -m uvicorn app.main:app
Terminal 2 — Frontend
cd frontend
npm run dev -- --host 127.0.0.1
Terminal 3 — Playwright
cd frontend
npx playwright test
Expected:
24 passed
Do not run Playwright against:
test_supportflow.db
because that database belongs to the isolated backend pytest suite.
Deliberate RED → GREEN Regression Demonstration
SupportFlow includes a deliberate regression exercise to prove that the automated suite can detect a genuine business-rule defect.
Business Rule
A ticket becomes SLA-breached when the current time is equal to or later than its deadline.
Correct rule:
current_time >= sla_deadline
The regression suite explicitly verifies:
Before deadline       → must NOT escalate
Exactly at deadline   → MUST escalate
After deadline        → MUST escalate
Deliberate Defect
For the RED run, the inclusive comparison was intentionally changed from:
current_time >= sla_deadline
to:
current_time > sla_deadline
At the exact SLA deadline this incorrectly evaluates to false.
RED Result
The existing regression suite detected the defect:
test_ticket_exactly_at_sla_deadline_escalates FAILED
This demonstrated that the suite was capable of failing when an important business rule was violated.
Correction
The correct inclusive comparison was restored:
current_time >= sla_deadline
The focused test, escalation tests, and complete regression suites were executed again.
Final Verification
Targeted SLA boundary test     PASS
Escalation tests               PASS
Backend regression             98 passed
Playwright browser regression  24 passed
Why This Regression Matters
The change was only one character:
>=   correct
>    incorrect at the exact deadline
Yet it changes SLA enforcement.
This demonstrates the value of:
Boundary-value testing.
Business-rule-focused regression testing.
Failure reproduction.
Root-cause isolation.
Targeted correction.
Full regression verification.
Stage-3 AI-Assisted Change Loop
After establishing a stable application and automated test baseline, SupportFlow was extended through an AI-assisted engineering change.
Baseline Before the Change
Before the Stage-3 enhancement:
Backend regression suite   82 passed
Playwright E2E suite       24 passed
The application already supported SLA detection and escalation.
New Feature Requirement
The new requirement was:
When an assigned ticket breaches its SLA, automatically attempt to reassign it to the least-loaded eligible Agent without breaking the existing escalation behavior.
This requirement interacted with existing:
SLA logic.
Escalation.
Assignment.
Agent capacity.
Audit events.
Notifications.
Configuration.
Idempotency.
Change Analysis
The implementation had to preserve several existing invariants.
SLA breach
    │
    ├── escalation must still occur
    ├── existing escalation audit must remain
    ├── existing notifications must remain
    ├── processing must remain idempotent
    │
    └── optional automatic reassignment
            │
            ├── exclude current Agent
            ├── exclude inactive Agents
            ├── enforce Agent capacity
            ├── calculate active workload
            ├── choose least-loaded Agent
            ├── deterministic tie-breaking
            ├── preserve no-candidate fallback
            ├── create reassignment audit
            └── notify affected Agents
AI-Assisted Engineering Workflow
Stable application
        ↓
New requirement
        ↓
AI-assisted impact analysis
        ↓
Identify affected modules
        ↓
Implement feature
        ↓
Add focused automated tests
        ↓
Run tests
        ↓
Analyze failures
        ↓
Apply targeted corrections
        ↓
Run focused regression
        ↓
Run complete backend regression
        ↓
Run browser regression
        ↓
Run CI on clean GitHub environment
AI assistance accelerated implementation and reasoning, while automated tests remained the source of verification.
New Regression Coverage
The Stage-3 change added tests for:
Least-loaded Agent selection.
Current Agent exclusion.
Inactive Agent exclusion.
Agent capacity enforcement.
No-replacement fallback.
Configuration toggle behavior.
Reassignment idempotency.
Reassignment audit creation.
Old Agent notification.
New Agent notification.
Unrelated Agent notification isolation.
Preservation of existing escalation auditing.
Result
The backend suite increased from:
82 tests
to:
98 tests
The browser suite remained:
24 tests
and continued to pass.
Final result:
Existing functionality   preserved
New functionality        covered
Backend regression       98 / 98 passed
Browser E2E regression   24 / 24 passed
Continuous Integration with GitHub Actions
SupportFlow uses GitHub Actions to reproduce the verification process on a clean CI runner.
Workflow:
.github/workflows/ci.yml
CI Architecture
Git Push / Pull Request
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Backend Tests             Frontend Checks
              │                         │
        Python 3.11                  Node.js
        Dependencies                 npm ci
        Ruff                         ESLint
        pytest                       Vite build
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                    Playwright E2E
                           │
                           ├── Fresh E2E database
                           ├── Alembic migrations
                           ├── Deterministic E2E seed
                           ├── FastAPI startup
                           ├── React/Vite startup
                           ├── Chromium installation
                           ├── 24 browser tests
                           └── Playwright report artifact
Backend CI
The backend CI job performs:
Install dependencies
        ↓
Ruff
        ↓
pytest
        ↓
98 tests
Frontend CI
The frontend job performs:
npm ci
   ↓
ESLint
   ↓
Vite production build
E2E CI
The E2E job:
Creates a clean E2E SQLite database.
Applies Alembic migrations.
Seeds deterministic E2E accounts.
Starts FastAPI.
Starts React/Vite.
Waits for both applications to become available.
Installs Playwright Chromium.
Runs all 24 browser tests.
Uploads the Playwright HTML report as an artifact.
Current verified CI result:
Backend Tests             PASS
Frontend Lint and Build   PASS
Playwright E2E            24 / 24 PASS
The successful CI run demonstrates that the application works on a clean GitHub-hosted environment rather than only on the original development machine.          Security Engineering
SupportFlow applies security controls primarily at the backend boundary.
Authentication
Protected APIs require authenticated JWT credentials.
Missing or invalid authentication is rejected by the backend.
Password Security
Passwords are hashed and are not stored as plaintext.
Role-Based Access Control
Backend authorization distinguishes:
REQUESTER
AGENT
ADMIN
Role boundaries are independently tested.
Registration Protection
Public registration creates Requester accounts.
Clients cannot inject an Agent or Admin role through public registration.
Automated regression tests verify this behavior.
Resource-Level Authorization
Authorization applies to individual resources.
Requester A
     │
     ├── Own ticket             → allowed
     │
     └── Requester B's ticket   → denied
This protects against horizontal privilege escalation.
Agent Assignment Boundaries
Assigned-ticket access is restricted so that an unrelated Agent cannot operate on another Agent's ticket.
Internal Note Privacy
Internal support notes are filtered by the backend and are not exposed to Requesters.
This behavior is verified at both backend and browser-test levels.
Administrative Boundaries
Requester and Agent accounts cannot access protected Admin functionality such as:
User management.
SLA configuration.
Application configuration.
Administrative reporting.
Secrets
Runtime secrets belong in environment variables or deployment secret stores.
The repository should contain only safe .env.example files.
Never commit:
JWT production secrets.
SMTP passwords.
Database credentials.
Private API keys.
Runtime .env files.
Known Limitations and Future Improvements
SupportFlow is designed as a complete assessment/demo application. A larger production deployment could extend several areas.
PostgreSQL
SQLite simplifies local execution and assessment.
A production system with higher concurrency could migrate persistence to PostgreSQL while retaining SQLAlchemy and Alembic.
Distributed SLA Processing
The current scheduler is appropriate for the project's deployment model.
At larger scale, SLA processing could move to dedicated workers with distributed locking.
Multi-Instance WebSockets
A horizontally scaled deployment could introduce Redis or another pub/sub layer so WebSocket notifications propagate between multiple backend instances.
Production Email Delivery
A production system could integrate a managed transactional email provider with delivery tracking, retry behavior, bounce handling, and monitoring.
Observability
Production observability could be extended with:
Centralized structured logging.
Application metrics.
Distributed tracing.
SLA-processing metrics.
Alerting.
Error aggregation.
Database Concurrency
SQLite is intentionally convenient for development and assessment. PostgreSQL would provide stronger concurrency characteristics for larger multi-user deployments.
E2E Demo Accounts
The dedicated Playwright E2E environment uses deterministic accounts:
Requester
requester.e2e@example.com

Agent
agent.e2e@example.com

Secondary Agent
agent2.e2e@example.com

Administrator
admin.e2e@example.com
These accounts are intended for the isolated E2E environment only.
Do not commit production credentials or private passwords.         Recommended Demo Flow
1. Requester
Login
  ↓
Create HIGH / CRITICAL ticket
  ↓
View SLA information
  ↓
View ticket in My Tickets
2. Administrator
Login
  ↓
Open All Tickets
  ↓
Locate ticket
  ↓
Assign Agent
3. Real-Time Notification
Keep the Agent browser session open while the Admin performs the assignment.
Expected:
Agent receives live notification
without page refresh
4. Agent
Open Assigned Tickets
  ↓
Open ticket
  ↓
Start work
  ↓
Add public response
  ↓
Add internal note
5. Privacy Verification
Return to the Requester account.
Expected:
Public response   → visible
Internal note     → not visible
6. Resolution
Agent
  ↓
Resolve ticket
  ↓
Provide resolution summary
Then:
Requester
  ↓
View resolved ticket
  ↓
Close ticket
7. Admin Features
Demonstrate:
Dashboard metrics.
User management.
SLA settings.
Application configuration.
Reports and CSV export.
Agent workload.
8. Engineering Evidence
Finish with:
pytest -v
Expected:
98 passed
Then:
npx playwright test
Expected:
24 passed
Finally show the successful GitHub Actions workflow.
AI Tool Usage
AI tooling was used as an engineering assistant during the assessment.
ChatGPT
Used for:
Requirement decomposition.
Architecture planning.
Implementation guidance.
Test-case generation.
Regression-test planning.
Failure analysis.
Stage-3 change-loop reasoning.
Documentation assistance.
CI workflow planning.
AI-generated or AI-assisted output was verified through execution, automated tests, linting, build checks, and CI rather than being accepted without validation.
Engineering Evidence
The following evidence can be stored under:
docs/screenshots/
Recommended evidence includes:
## Screenshots

### Authentication

#### Register Account

![Register Account](docs/screenshots/register-account.png)

#### Login

![Login Account](docs/screenshots/login-account.png)

#### Forgot Password

![Forgot Password](docs/screenshots/forgot-password.png)

### Requester Experience

#### Requester Dashboard

![Requester Dashboard](docs/screenshots/requester-dashboard.png)

#### Create Ticket

![Create Ticket](docs/screenshots/create-ticket.png)

### Agent Experience

#### Agent Dashboard

![Agent Dashboard](docs/screenshots/agent-dashboard.png)

#### Ticket Details and Conversation

![Ticket Details](docs/screenshots/ticket-details.png)

### Administrator Experience

#### Admin Dashboard

![Admin Dashboard](docs/screenshots/admin-dashboard.png)

#### SLA Settings

![SLA Settings](docs/screenshots/sla-settings.png)

#### User Management

![User Management](docs/screenshots/user-management.png)

### Real-Time Notifications

![Live WebSocket Notification](docs/screenshots/live-notification.png)

### Automated Testing Evidence

#### Backend pytest — 98 Tests Passed

![98 Backend Tests Passed](docs/screenshots/pytest-98-passed.png)

#### Playwright E2E — 24 Tests Passed

![24 Playwright Tests Passed](docs/screenshots/playwright-24-passed.png)

### Deliberate RED → GREEN Evidence

#### Deliberate RED Run

![Deliberate RED Run](docs/screenshots/deliberate-red-run.png)

#### Corrected GREEN Run

![RED to GREEN Verification](docs/screenshots/red-green-fixed.png)

### GitHub Actions CI

![GitHub Actions CI](docs/screenshots/github-actions-green.png)

Once screenshots are available, they can be referenced from this README using repository-relative paths.
Additional Assessment Documentation
The assessment documentation set can be maintained under:
docs/
├── architecture/
│   └── ARCHITECTURE.md
├── design/
│   └── DESIGN.md
├── user-guide/
│   └── USER_GUIDE.md
├── ai-evidence/
│   └── AI_CHANGE_LOOP.md
├── testing/
│   └── TEST_EVIDENCE.md
└── screenshots/
These documents complement the README:
ARCHITECTURE.md — system components, data flow, technology decisions, and architecture reasoning.
DESIGN.md — data model, APIs, core business workflows, error handling, and security design.
USER_GUIDE.md — non-technical instructions for Requesters, Agents, and Administrators.
AI_CHANGE_LOOP.md — prompts, implementation changes, failures, corrections, attempts, and manual intervention.
TEST_EVIDENCE.md — backend tests, Playwright tests, deliberate RED run, GREEN recovery, and CI evidence.
Final Verification Status
Backend pytest
98 / 98 passed

Backend Ruff
PASS

Frontend ESLint
PASS

Frontend production build
PASS

Playwright E2E
24 / 24 passed

GitHub Actions
PASS

Playwright report artifact
Uploaded successfully
SupportFlow therefore demonstrates a complete:
Design
  ↓
Build
  ↓
Secure
  ↓
Test
  ↓
Break deliberately
  ↓
Detect
  ↓
Fix
  ↓
Extend through AI-assisted change
  ↓
Regression test
  ↓
Verify in CI
  ↓
Document
engineering workflow.
