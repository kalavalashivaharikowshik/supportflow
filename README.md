SupportFlow — AI-Assisted Support Ticket Escalation System

A production-style full-stack support ticket management application with SLA enforcement, automatic escalation, workload-aware ticket reassignment, role-based access control, audit trails, real-time WebSocket notifications, automated testing, and continuous integration.

SupportFlow was developed as part of the AI-Powered QA Automation, Documentation & Software Engineering Assessment. The project demonstrates not only application development, but also an AI-assisted build → test → fail → diagnose → fix → verify engineering workflow.

---

1. Overview

Support teams commonly classify tickets as Low, Medium, High, or Critical priority. However, simply attaching a priority label to a ticket does not guarantee that it receives timely attention.

A high-priority ticket may remain assigned but unattended until someone manually notices it.

SupportFlow addresses this problem by making priority operationally meaningful.

The application:

- allows Requesters to create support tickets;
- allows Administrators to assign tickets to Agents;
- allows Agents to work on and resolve assigned tickets;
- calculates SLA deadlines based on ticket priority;
- automatically detects SLA breaches;
- escalates overdue tickets;
- optionally reassigns breached tickets to a less-loaded eligible Agent;
- records important actions in an audit trail;
- sends persistent notifications;
- delivers live notifications through WebSockets;
- enforces role and ownership security;
- provides dashboards, reports, search, filters, sorting, and pagination;
- verifies critical behavior through automated backend and browser tests.

---

2. Problem Statement

In many organizations, customer or internal support requests are managed through ticket queues.

A common operational failure occurs when high-priority tickets silently remain unattended.

Without automated SLA enforcement, urgent tickets depend on somebody manually monitoring the queue and noticing that action is overdue.

This creates several problems:

- SLA breaches — urgent requests exceed their expected response or resolution window.
- Manual monitoring overhead — supervisors must continuously inspect ticket queues.
- Weak accountability — it becomes difficult to determine exactly what happened to a ticket and when.
- Inconsistent prioritization — a High or Critical priority label may have no actual operational consequence.
- Agent overload — breached tickets may remain with an already overloaded Agent even when another Agent has capacity.

SupportFlow solves this by enforcing ticket lifecycle and SLA rules directly within the application.

A ticket receives an SLA deadline based on its priority. The system monitors active tickets and automatically escalates tickets that reach or exceed their deadline.

As an additional Stage-3 enhancement, an escalated ticket can automatically move to the least-loaded eligible Agent.

---

3. Project Goals

The primary goals of SupportFlow are to:

1. Provide secure Requester, Agent, and Administrator workflows.
2. Enforce ticket lifecycle rules rather than treating tickets as simple CRUD records.
3. Associate SLA deadlines with ticket priority.
4. Automatically detect overdue tickets.
5. Escalate breached tickets without manual intervention.
6. Preserve a complete audit trail of important ticket events.
7. Provide persistent and live notifications.
8. Prevent unauthorized ticket and administrative access.
9. Automatically redistribute breached tickets when another Agent has capacity.
10. Verify business rules through automated tests.
11. Demonstrate a genuine AI-assisted build → test → fix engineering loop.
12. Run automated verification through GitHub Actions.

---

4. Key Features

4.1 Authentication

SupportFlow provides:

- user registration;
- secure login;
- JWT-based authentication;
- authenticated "/me" functionality;
- password hashing;
- logout/session handling;
- protected frontend routes;
- backend authentication dependencies;
- role-aware authorization.

Public registration creates Requester accounts only, preventing role injection during registration.

---

4.2 Forgot Password with Email OTP

The password recovery workflow uses email verification.

Flow:

Forgot Password
      ↓
Enter registered email
      ↓
OTP generated
      ↓
OTP sent by email
      ↓
User enters OTP
      ↓
OTP verified
      ↓
Password reset allowed
      ↓
New password stored securely

OTP handling is implemented across both the backend and frontend.

---

5. User Roles

SupportFlow contains three primary roles:

REQUESTER
AGENT
ADMIN

5.1 Requester

A Requester can:

- register;
- log in;
- create tickets;
- select ticket priority;
- view personal tickets;
- search personal tickets;
- filter and sort tickets;
- view ticket details;
- add public responses to owned tickets;
- view the permitted conversation;
- track ticket status;
- track SLA information;
- close resolved tickets;
- reopen tickets when permitted by configuration;
- receive persistent notifications;
- receive real-time notifications;
- manage profile information.

A Requester cannot:

- view another Requester's private ticket;
- create internal notes;
- access Agent pages;
- access Administrator pages;
- assign tickets;
- manage users;
- modify SLA configuration;
- access administrative reports.

---

5.2 Agent

An Agent can:

- log in;
- view assigned tickets;
- view escalated tickets;
- view ticket details for permitted tickets;
- start work on assigned tickets;
- add public responses;
- add internal notes;
- resolve tickets;
- provide resolution information;
- receive assignment notifications;
- receive SLA/escalation notifications;
- receive automatic reassignment notifications;
- receive real-time WebSocket notifications.

An Agent cannot:

- access Requester-only routes;
- access Administrator-only routes;
- manage users;
- modify global SLA settings;
- view unauthorized tickets.

---

5.3 Administrator

An Administrator can:

- view the Administrator dashboard;
- view system-wide tickets;
- search, filter, sort, and paginate tickets;
- assign tickets to Agents;
- manually reassign tickets;
- manage users;
- activate and deactivate users;
- create Agent accounts;
- monitor Agent workloads;
- configure SLA durations;
- configure application behavior;
- enable or disable automatic SLA reassignment;
- access reports;
- export ticket data;
- review operational information;
- manage permitted ticket actions.

---

6. Technology Stack

Layer| Technology
Frontend| React
Frontend Build Tool| Vite
Styling| Tailwind CSS
Backend| FastAPI
Language| Python 3.11
ORM| SQLAlchemy
Database Migrations| Alembic
Database| SQLite
Authentication| JWT
Password Security| Passlib / bcrypt
Configuration| Environment Variables / Pydantic Settings
Real-Time Communication| WebSockets
Backend Testing| pytest
Browser E2E Testing| Playwright
Python Code Quality| Ruff
Frontend Code Quality| ESLint
Frontend Production Build| Vite
CI| GitHub Actions
AI Assistance| ChatGPT / AI-assisted engineering workflow

SQLite was intentionally used to make the assessment easy to start and review without requiring an external database server.

The architecture remains structured so that a production relational database such as PostgreSQL could be introduced later.

---

7. High-Level Architecture

┌───────────────────────────────────────────────────────────┐
│                    React + Vite Frontend                  │
│                                                           │
│  Requester UI        Agent UI           Administrator UI  │
│                                                           │
│  Auth │ Tickets │ Dashboard │ Notifications │ Reports     │
└────────────────────────────┬──────────────────────────────┘
                             │
                        REST API
                             │
                             │ WebSocket
                             ▼
┌───────────────────────────────────────────────────────────┐
│                         FastAPI                           │
│                                                           │
│ Auth / RBAC                                               │
│ Ticket Management                                         │
│ Assignment                                                │
│ Responses                                                 │
│ Status Workflow                                           │
│ SLA Engine                                                │
│ Escalation Engine                                         │
│ Automatic Reassignment                                    │
│ Audit Trail                                               │
│ Notifications                                             │
│ WebSocket Manager                                         │
│ Dashboard                                                 │
│ Reports                                                   │
│ Administration                                            │
└────────────────────────────┬──────────────────────────────┘
                             │
                         SQLAlchemy
                             │
                             ▼
┌───────────────────────────────────────────────────────────┐
│                          SQLite                           │
│                                                           │
│ Users                                                     │
│ Roles                                                     │
│ Tickets                                                   │
│ Ticket Responses                                          │
│ Ticket Audit Events                                       │
│ SLA Configuration                                         │
│ Application Configuration                                 │
│ Notifications                                             │
│ Password OTP                                              │
└───────────────────────────────────────────────────────────┘

---

8. Backend Architecture

The backend follows a layered architecture.

API Routes
    ↓
Services
    ↓
Repositories
    ↓
SQLAlchemy Models
    ↓
Database

Responsibilities are intentionally separated.

API Layer

Responsible for:

- HTTP endpoints;
- request validation;
- authentication dependencies;
- role authorization;
- response serialization.

Service Layer

Responsible for business rules such as:

- authentication;
- ticket creation;
- assignment;
- ticket responses;
- lifecycle transitions;
- SLA calculations;
- escalation;
- automatic reassignment;
- audit generation;
- notifications;
- dashboards;
- reports.

Repository Layer

Responsible for database access and reusable query operations.

Model Layer

Contains SQLAlchemy database entities.

Schema Layer

Contains API request and response validation models.

This prevents HTTP, business, database, and UI logic from being mixed together.

---

9. Ticket Lifecycle

The primary ticket lifecycle is:

OPEN
  │
  │ Administrator assigns Agent
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
  ├──────── Requester closes ────────► CLOSED
  │
  └──────── Requester reopens ───────► REOPENED

SLA escalation introduces an additional path:

ASSIGNED / IN_PROGRESS / REOPENED
                │
                │ SLA deadline reached
                ▼
            ESCALATED
                │
                │ Agent resolves
                ▼
             RESOLVED

The backend enforces valid transitions.

The frontend only exposes actions appropriate to the authenticated role and current ticket state.

---

10. SLA Engine

SupportFlow uses database-backed SLA configuration.

SLA duration is associated with ticket priority.

Example priority levels include:

LOW
MEDIUM
HIGH
CRITICAL

When a ticket is created, the appropriate SLA configuration is used to determine its deadline.

Conceptually:

ticket creation time
        +
configured SLA duration
        =
SLA deadline

---

10.1 SLA Boundary Rule

The breach condition is intentionally inclusive:

current_time >= sla_deadline

Therefore:

Before SLA deadline
→ NOT breached

Exactly at SLA deadline
→ BREACHED

After SLA deadline
→ BREACHED

This boundary condition is explicitly covered by automated tests.

---

10.2 Escalation Rules

When an eligible active ticket breaches its SLA:

SLA deadline reached
        ↓
Ticket detected by escalation processor
        ↓
Ticket becomes ESCALATED
        ↓
Audit event created
        ↓
Notifications generated
        ↓
Optional automatic reassignment

Resolved and closed tickets do not escalate.

Already-escalated tickets are not escalated repeatedly.

---

11. Escalation Idempotency

The escalation process is designed to be idempotent.

Running the escalation processor multiple times against the same already-escalated ticket must not create repeated escalation actions.

Conceptually:

First processing
→ ESCALATED
→ audit generated
→ notification generated

Second processing
→ already escalated
→ no duplicate escalation

This behavior is verified through automated tests.

---

12. SLA-Based Automatic Reassignment

Automatic reassignment was introduced as the major Stage-3 feature extension.

Previously:

Ticket breaches SLA
        ↓
Ticket becomes ESCALATED
        ↓
Original Agent remains assigned

The enhanced behavior is:

Ticket breaches SLA
        ↓
Ticket becomes ESCALATED
        ↓
Check auto-reassignment configuration
        ↓
Find eligible replacement Agent
        ↓
Choose least-loaded Agent
        ↓
Reassign ticket
        ↓
Audit + notifications

---

12.1 Eligibility Rules

A replacement Agent must:

- have the Agent role;
- be active;
- not be the ticket's existing Agent;
- have active workload below the configured capacity.

---

12.2 Agent Selection

Eligible Agents are ranked by:

1. Lowest active workload
2. Lowest Agent ID

The Agent ID is used as a deterministic tie-breaker.

This ensures that automated tests and production behavior are predictable.

---

12.3 Current Agent Exclusion

The existing assignee is explicitly excluded from replacement selection.

Without this rule, the algorithm could technically "reassign" a ticket to the same Agent when that Agent has the lowest workload.

Automated tests explicitly verify this edge case.

---

12.4 Capacity Enforcement

SupportFlow contains a configurable maximum active-ticket capacity per Agent.

An Agent already at capacity is not eligible for automatic reassignment.

Example:

Maximum active tickets = 2

Agent B workload = 2
Agent C workload = 1

Agent B → not eligible
Agent C → eligible

---

12.5 No Replacement Available

Automatic reassignment must never prevent normal SLA escalation.

If no replacement Agent exists:

Ticket → ESCALATED
Assignment → existing Agent retained

Escalation therefore succeeds independently of reassignment availability.

---

12.6 Feature Toggle

Automatic reassignment can be controlled through application configuration:

auto_reassign_on_escalation

When enabled:

SLA breach
→ escalation
→ replacement search

When disabled:

SLA breach
→ escalation
→ existing Agent retained

---

13. Audit Trail

SupportFlow maintains an audit history for important ticket events.

Examples include:

- ticket creation;
- assignment;
- reassignment;
- status changes;
- escalation;
- automatic SLA reassignment;
- resolution;
- reopen/close actions.

For automatic SLA reassignment, the audit trail preserves both facts:

SLA_ESCALATED
TICKET_AUTO_REASSIGNED

This is important because escalation and reassignment represent different business events.

---

14. Ticket Responses

SupportFlow supports two response types:

PUBLIC RESPONSE
INTERNAL NOTE

Public Response

Visible to permitted participants including the Requester.

Internal Note

Used for internal support collaboration.

Internal notes are hidden from Requesters.

Automated security tests verify that Requesters cannot:

- create internal notes;
- retrieve internal notes;
- access another Requester's ticket conversation.

---

15. Notifications

SupportFlow contains persistent application notifications.

Notifications can be generated for events such as:

- ticket assignment;
- ticket reassignment;
- responses;
- ticket status changes;
- SLA escalation;
- automatic SLA reassignment;
- resolution;
- reopen/close actions.

Automatic reassignment specifically notifies:

Old Agent
→ ticket was reassigned after SLA breach

New Agent
→ escalated ticket was assigned

Unrelated Agents do not receive the notification.

This behavior is covered by automated tests.

---

16. Real-Time WebSocket Notifications

SupportFlow provides live notification delivery through WebSockets.

Architecture:

Backend business event
        ↓
Notification Service
        ↓
Persistent notification stored
        ↓
WebSocket Manager
        ↓
Connected authenticated user
        ↓
React Notification Context
        ↓
UI updates without refresh

This allows an Agent to receive an assignment notification immediately without refreshing the browser.

A Playwright browser test verifies this behavior end to end.

---

17. Search, Filtering, Sorting and Pagination

Ticket lists support production-style data handling rather than loading every record into the UI.

Supported capabilities include:

- text search;
- status filtering;
- priority filtering;
- sorting;
- pagination;
- role-aware ticket visibility.

Requesters only search tickets they are authorized to access.

Administrators can operate on the wider system ticket set.

---

18. Dashboards

SupportFlow provides role-specific dashboards.

Requester Dashboard

Shows information relevant to the Requester's own tickets.

Agent Dashboard

Shows information relevant to assigned and escalated Agent workload.

Administrator Dashboard

Provides system-wide operational information.

Dashboard endpoints are protected by role authorization.

Automated tests verify that one role cannot access another role's dashboard.

---

19. Reports and Export

Administrator reporting functionality includes ticket summary reporting and CSV export.

Security rules ensure that unauthorized roles cannot access administrative reports or exports.

Automated tests verify:

- valid report access;
- invalid date ranges;
- CSV responses;
- attachment headers;
- authentication requirements;
- Requester authorization restrictions.

---

20. Administrator Configuration

Application behavior is database-backed and configurable.

Configuration includes operational settings such as:

- maximum active tickets per Agent;
- escalation behavior;
- notification behavior;
- ticket workflow options;
- automatic SLA reassignment.

The automatic reassignment setting is:

auto_reassign_on_escalation

Only authorized Administrators can modify application configuration.

---

21. Security

Security was treated as a business requirement rather than only a UI concern.

SupportFlow includes:

- JWT authentication;
- password hashing;
- role-based authorization;
- ownership checks;
- protected API routes;
- protected frontend routes;
- role-specific frontend routing;
- registration role-injection prevention;
- internal-note privacy;
- environment-based secrets;
- CORS configuration;
- request validation;
- inactive-user controls;
- restricted Administrator operations.

The backend remains the authoritative security boundary.

Hiding a button in React is never treated as sufficient authorization.

---

22. Project Structure

Backend

backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   ├── routes/
│   │   └── router.py
│   │
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── websocket/
│   ├── scheduler/
│   ├── utils/
│   └── main.py
│
├── tests/
│   ├── admin/
│   ├── audit/
│   ├── auth/
│   ├── dashboard/
│   ├── escalation/
│   ├── notifications/
│   ├── reports/
│   ├security/
│   ├── sla/
│   ├── tickets/
│   ├── users/
│   ├── websocket/
│   └── conftest.py
│
├── .env.example
├── alembic.ini
├── requirements.txt
└── pytest.ini
Frontend
frontend/
│
├── public/
│
├── src/
│   ├── api/
│   ├── assets/
│   ├── components/
│   │   ├── common/
│   │   ├── auth/
│   │   ├── tickets/
│   │   ├── users/
│   │   ├── dashboard/
│   │   ├── notifications/
│   │   ├── audit/
│   │   └── sla/
│   │
│   ├── constants/
│   ├── contexts/
│   ├── hooks/
│   ├── layouts/
│   ├── pages/
│   │   ├── auth/
│   │   ├── requester/
│   │   ├── agent/
│   │   ├── admin/
│   │   ├── tickets/
│   │   └── notifications/
│   │
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── e2e/
├── .env.example
├── eslint.config.js
├── package.json
├── playwright.config.js
└── vite.config.js
23. Local Development Setup
Prerequisites
Install:
Git
Python 3.11+
Node.js
npm
Clone the repository:
git clone <repository-url>
cd supportflow
24. Backend Setup
Move into the backend:
cd backend
Create a Python virtual environment:
Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Create the local environment file from the example:
.env.example
→ .env
Configure the required environment variables.
Do not commit .env.
25. Database Setup
SupportFlow uses Alembic for schema migrations.
From backend/ run:
alembic upgrade head
This creates or upgrades the database to the latest schema.
Start the backend:
python -m uvicorn app.main:app --reload
Backend:
http://127.0.0.1:8000
Swagger/OpenAPI documentation:
http://127.0.0.1:8000/docs
26. Frontend Setup
Open another terminal:
cd frontend
Install dependencies:
npm install
Create the frontend environment configuration from:
.env.example
Start Vite:
npm run dev
Typical frontend address:
http://127.0.0.1:5173
27. API Testing
Backend APIs were verified during development using:
Swagger/OpenAPI;
Postman;
automated pytest integration tests.
Postman testing covered authenticated and unauthorized API behavior during implementation.
Swagger can be accessed while FastAPI is running at:
http://127.0.0.1:8000/docs
28. Automated Testing Strategy
SupportFlow uses multiple testing layers.
Service / API behavior
        ↓
pytest

Browser + API integration
        ↓
Playwright

Code quality
        ↓
Ruff + ESLint

Production frontend compilation
        ↓
Vite build

Repository verification
        ↓
GitHub Actions
29. Backend Automated Tests — pytest
Run from:
backend/
Activate the virtual environment and execute:
pytest -v
Current verified result:
98 passed
The suite verifies functionality including:
authentication;
invalid authentication;
/me;
registration;
role-injection prevention;
role authorization;
dashboards;
ticket ownership;
ticket creation;
assignment;
responses;
internal notes;
lifecycle transitions;
SLA configuration;
SLA boundary conditions;
escalation;
escalation idempotency;
automatic reassignment;
Agent workload selection;
inactive Agent exclusion;
capacity enforcement;
reassignment fallback;
application configuration;
audit events;
notifications;
reports;
CSV export;
WebSocket authentication.
30. SLA Boundary Tests
Critical SLA tests verify:
Before deadline
→ no escalation

Exactly at deadline
→ escalation

After deadline
→ escalation

Resolved ticket
→ no escalation

Closed ticket
→ no escalation

Already escalated ticket
→ no duplicate escalation
This boundary suite played an important role in the deliberate red-run demonstration.
31. Automatic Reassignment Tests
The Stage-3 feature introduced dedicated regression tests.
Verified scenarios include:
Overdue ticket
→ least-loaded Agent selected

Current Agent
→ excluded

Inactive Agent
→ excluded

Agent at capacity
→ excluded

No replacement Agent
→ original Agent retained
→ escalation still succeeds

Feature disabled
→ no automatic reassignment

Repeated processing
→ no duplicate reassignment

Successful reassignment
→ audit event generated

Old Agent
→ notified

New Agent
→ notified

Unrelated Agent
→ not notified
32. Test Database Isolation
SupportFlow deliberately separates databases according to purpose.
backend/supportflow.db
        ↓
Normal local development
Swagger
Postman
Manual frontend usage
backend/test_supportflow.db
        ↓
pytest
        ↓
Backend automated test isolation
backend/supportflow_e2e.db
        ↓
FastAPI + React + Playwright
        ↓
Browser E2E workflows
The pytest and Playwright databases are intentionally separate.
pytest aggressively creates and isolates test data.
Playwright requires persistent seeded users across real browser and API requests.
33. Playwright End-to-End Tests
From:
frontend/
run:
npx playwright test
Current verified result:
24 passed
The suite runs with one worker because several E2E workflows intentionally operate against the same deterministic E2E environment.
33.1 E2E Scenarios
The Playwright suite includes:
Authentication
Requester login.
Invalid password.
Protected-route redirect.
Registration.
Requester
Create Critical ticket.
Search/filter own tickets.
Complete ticket lifecycle.
Agent
Start work.
Resolve ticket.
Requester close after resolution.
Administrator
Assign ticket.
Update application configuration.
Update and restore SLA configuration.
Deactivate and reactivate Agent.
Notifications
Agent receives live assignment notification without page refresh.
Security
Internal note hidden from Requester.
Requester blocked from Administrator route.
Requester blocked from Agent route.
Agent blocked from Administrator route.
Agent blocked from Requester route.
Administrator blocked from Requester route.
Administrator blocked from Agent route.
Requester cannot access another Requester's ticket.
Responsive UI
Requester mobile navigation.

34. Running the Complete Local Verification
Step 1 — Backend Tests
cd backend
.\venv\Scripts\Activate.ps1
pytest -v
Expected:
98 passed
Run Ruff:
ruff check app
Expected:
All checks passed!
Step 2 — Start E2E Backend
Configure the E2E database:
$env:DATABASE_URL="sqlite:///./supportflow_e2e.db"
$env:CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
$env:FRONTEND_URL="http://127.0.0.1:5173"
Start FastAPI:
python -m uvicorn app.main:app
Leave the terminal running.
Step 3 — Start Frontend
Open another terminal:
cd frontend
npm run dev -- --host 127.0.0.1
Leave it running.
Step 4 — Run Browser Tests
Open another terminal:
cd frontend
npx playwright test
Expected:
24 passed
Step 5 — Frontend Quality Verification
Run:
npm run lint
Then:
npm run build
Both commands should complete successfully.
35. Deliberate RED → GREEN Demonstration
A key assessment requirement was proving that the automated suite could detect an actual regression.
The SLA deadline boundary was selected because it represents a meaningful business rule rather than an artificial syntax failure.
Correct behavior:
current_time >= sla_deadline
This means a ticket is considered breached exactly when its SLA deadline is reached.
For the deliberate regression, the comparison was changed to:
current_time > sla_deadline
The consequence was:
Before deadline
→ still correct

After deadline
→ still correct

Exactly at deadline
→ WRONG
The automated boundary test detected the regression.
The implementation was then restored to:
current_time >= sla_deadline
The focused test passed again, followed by the complete backend regression suite.
This demonstrated that the automated tests were capable of detecting a subtle business-rule defect rather than merely producing permanently green results.
36. AI-Assisted Engineering Workflow
AI tools were used as engineering assistants for:
architecture planning;
implementation guidance;
test generation;
edge-case identification;
debugging;
failure analysis;
documentation;
CI planning.
AI-generated or AI-assisted changes were not treated as correct simply because they compiled.
The engineering workflow was:
Business Requirement
        ↓
AI Prompt
        ↓
Implementation
        ↓
Automated Tests
        ↓
Observe Result
        ↓
Failure?
   ┌────┴────┐
  YES        NO
   │          │
Analyze       │
   ↓          │
Correct       │
   ↓          │
Retest ◄──────┘
   ↓
Full Regression
37. Stage-3 AI Change Loop
The major Stage-3 feature request was:
When an assigned ticket breaches its SLA, automatically attempt to reassign it to the least-loaded eligible active Agent while preserving the existing escalation behavior.
The requirement introduced interactions between:
SLA Engine
Escalation Engine
Assignment
Agent Capacity
Application Configuration
Audit Trail
Notifications
Idempotency
Dedicated tests were created for the new business rules.
The final implementation supports:
least-loaded Agent selection;
current-Agent exclusion;
inactive-Agent exclusion;
capacity enforcement;
deterministic tie-breaking;
no-candidate fallback;
configuration toggle;
reassignment auditing;
old/new Agent notifications;
escalation preservation;
idempotency.
After the Stage-3 enhancement, the complete backend regression suite reached:
98 passed
while the existing browser regression suite remained:
24 passed
This demonstrated that the new functionality could be integrated without breaking the previously verified application workflows.
38. Continuous Integration — GitHub Actions
SupportFlow uses GitHub Actions to verify the repository outside the local development environment.
The CI workflow contains three major jobs:
Backend Tests
Frontend Lint and Build
Playwright E2E
38.1 Backend CI
The backend job performs:
Checkout
    ↓
Python setup
    ↓
Install dependencies
    ↓
Ruff
    ↓
pytest
The backend regression suite verifies all 98 tests.
38.2 Frontend CI
The frontend job performs:
Checkout
    ↓
Node setup
    ↓
npm ci
    ↓
ESLint
    ↓
Vite production build
38.3 Playwright CI
The browser job performs:
Checkout
    ↓
Python setup
    ↓
Backend dependencies
    ↓
Fresh E2E database
    ↓
Alembic migrations
    ↓
E2E seed data
    ↓
Start FastAPI
    ↓
Node setup
    ↓
Frontend dependencies
    ↓
Install Chromium
    ↓
Start Vite
    ↓
Wait for services
    ↓
Run Playwright
Current verified browser result in GitHub Actions:
24 passed
38.4 Playwright Artifacts
GitHub Actions uploads the Playwright HTML report as a workflow artifact.
On test failure, diagnostic artifacts can be retained to assist investigation.
This makes CI failures inspectable instead of providing only a pass/fail indicator.
39. Code Quality
Backend:
ruff check app
Current result:
All checks passed!
Frontend:
npm run lint
Production build:
npm run build
The Vite production build completes successfully.

40. API Documentation
FastAPI automatically provides interactive OpenAPI documentation.
With the backend running:
http://127.0.0.1:8000/docs
This can be used to inspect and manually test available API endpoints.
41. Environment and Secret Management
Sensitive configuration is stored using environment variables.
Files such as:
.env
must not be committed.
The repository should contain:
.env.example
with safe placeholder values showing reviewers which variables are required.
Runtime databases, virtual environments, frontend dependencies, test artifacts, and secrets are excluded through .gitignore.
42. Development Database vs Test Databases
The repository uses:
supportflow.db
for normal development.
Automated testing uses separate databases:
test_supportflow.db
supportflow_e2e.db
These files are runtime artifacts and should not be treated as source code.
This separation prevents automated tests from damaging local development data.
43. Why SQLite?
SQLite was chosen because this assessment requires the application to be easy for another reviewer to start from the repository.
Benefits include:
no external database server;
no database account setup;
no Docker requirement;
fast automated tests;
simple local development;
straightforward CI setup.
For a larger production deployment, PostgreSQL would be a natural migration target.
44. Why FastAPI?
FastAPI provides:
Python type-driven validation;
automatic OpenAPI documentation;
dependency-based authentication;
clear REST API organization;
asynchronous/WebSocket support;
strong compatibility with pytest;
concise service integration.
45. Why React + Vite?
React provides a component-oriented frontend architecture, while Vite provides:
fast local development;
straightforward environment configuration;
optimized production builds;
simple integration with Playwright.
46. Why Playwright?
Playwright verifies behavior through a real browser.
This allows SupportFlow to test workflows that unit/API tests alone cannot completely verify, including:
authentication through the UI;
protected routing;
cross-role workflows;
live WebSocket notifications;
internal-note privacy;
mobile navigation;
complete ticket lifecycle behavior.
47. Why pytest?
pytest provides fast and focused verification of backend business rules.
It is particularly valuable for SupportFlow because the most important behavior contains subtle edge cases:
SLA deadline equality;
idempotency;
role boundaries;
ownership;
capacity limits;
automatic reassignment eligibility;
notification targeting.
48. Engineering Decisions
Several design decisions were made intentionally.
Business Logic Lives in the Backend
React does not determine whether an action is authorized.
The backend enforces authorization and workflow rules.
SLA Configuration Is Database-Backed
SLA durations are not scattered as hardcoded constants throughout the application.
Escalation Is Idempotent
Background processing can run repeatedly without repeatedly escalating the same ticket.
Automatic Reassignment Cannot Block Escalation
If no replacement Agent exists, escalation still succeeds.
Internal Notes Are Protected Server-Side
Requesters cannot retrieve internal notes simply by bypassing the frontend.
Notifications Are Persistent First
Notification records are stored before or alongside real-time delivery, preventing WebSocket connectivity from becoming the sole record of an event.
Test Databases Are Isolated
Backend test behavior cannot destroy the persistent E2E test environment.
CI Uses a Fresh Environment
GitHub Actions verifies that the repository works outside the original development machine.
49. Current Automated Verification Status
┌─────────────────────────────────────┐
│       SUPPORTFLOW VERIFICATION      │
├─────────────────────────────────────┤
│ Backend pytest        98 / 98  PASS │
│ Playwright E2E        24 / 24  PASS │
│ Ruff                           PASS │
│ ESLint                         PASS │
│ Vite Production Build         PASS │
│ GitHub Actions CI              PASS │
└─────────────────────────────────────┘
50. Demonstrated End-to-End Workflow
One representative SupportFlow workflow is:
Requester
    ↓
Creates Critical ticket
    ↓
SLA deadline generated
    ↓
Administrator
    ↓
Assigns Agent
    ↓
Agent receives live notification
    ↓
Agent starts work
    ↓
Requester / Agent conversation
    ↓
Agent adds internal notes if required
    ↓
Agent resolves ticket
    ↓
Requester reviews resolution
    ↓
Requester closes ticket
An SLA breach introduces:
Active assigned ticket
        ↓
SLA deadline reached
        ↓
Automatic escalation
        ↓
Audit event
        ↓
Notification
        ↓
Auto-reassignment enabled?
      /                 \
    YES                  NO
     ↓                    ↓
Find eligible Agent    Keep Agent
     ↓                    ↓
Least-loaded Agent        │
     ↓                    │
Reassign                  │
     ↓                    │
Audit + notifications     │
      \                  /
       └──────► Continue workflow

51. Demo Flow
A recommended demonstration sequence is:
1. Introduce the problem
Explain why high-priority tickets need enforced SLA behavior rather than only priority labels.
2. Requester
Log in.
Create a Critical ticket.
Show SLA information.
Show My Tickets.
3. Administrator
Log in.
Locate the ticket.
Assign it to an Agent.
Show Agent workload.
Show SLA configuration.
Show automatic reassignment configuration.
4. Agent
Log in.
Show live assignment notification.
Open the ticket.
Start work.
Add response/internal note.
Resolve the ticket.
5. Requester
Show that internal notes are not visible.
Review the resolution.
Close the ticket.
6. Automated Testing
Show:
pytest -v
→ 98 passed
Then:
npx playwright test
→ 24 passed
7. AI/Test Evidence
Explain:
Deliberate SLA boundary regression
→ test RED
→ fix
→ GREEN
Then explain the Stage-3 automatic reassignment feature.
8. CI
Show the GitHub Actions workflow with successful jobs.
52. Known Limitations
SupportFlow is designed as an assessment-scale production-style application rather than a large distributed support platform.
Current limitations include:
SQLite rather than a production database server;
single application instance;
in-process scheduling rather than a distributed job queue;
WebSocket connection state stored within the running application process;
no distributed cache;
no external message broker;
no file attachment/object-storage subsystem;
no enterprise SSO;
no multi-tenant organization model.
These choices keep the repository straightforward for assessment reviewers while preserving clear extension points.
53. Production Improvements
For a larger production deployment, potential enhancements include:
PostgreSQL;
Redis;
Celery/RQ or another distributed worker system;
message broker;
distributed WebSocket/pub-sub infrastructure;
Docker and Docker Compose;
cloud deployment;
object storage for attachments;
observability and metrics;
centralized structured logging;
tracing;
rate limiting;
refresh-token rotation;
enterprise SSO;
multi-tenant organizations;
advanced SLA calendars and business hours;
escalation policies with multiple levels;
email/SMS notification channels.
54. Assessment Evidence
The repository demonstrates the four major engineering stages.
STAGE 1
Working full-stack application
        ↓
COMPLETE

STAGE 2
AI-assisted automated test generation
+
normal paths
+
edge cases
+
invalid/security cases
+
deliberate RED run
        ↓
COMPLETE

STAGE 3
New feature request
+
AI-assisted implementation
+
automated verification
+
failure analysis
+
correction
+
full regression
        ↓
COMPLETE

STAGE 4
Architecture
+
Design documentation
+
User guide
+
presentation/demo preparation
        ↓
DOCUMENTATION PHASE
55. AI Tools Used
AI assistance was used during the engineering process.
ChatGPT
Used for:
requirements analysis;
architecture planning;
implementation guidance;
business-rule analysis;
test-case generation;
debugging guidance;
regression analysis;
CI planning;
documentation;
presentation preparation.
Any AI-assisted implementation was verified through actual execution and automated tests rather than being assumed correct.
56. Final Project Status
SupportFlow currently provides:
Authentication                         COMPLETE
Email OTP password recovery            COMPLETE
RBAC                                   COMPLETE
User management                        COMPLETE
Ticket management                      COMPLETE
Assignment                             COMPLETE
Responses                              COMPLETE
Internal notes                         COMPLETE
Status workflow                        COMPLETE
SLA engine                             COMPLETE
Automatic escalation                   COMPLETE
Audit trail                            COMPLETE
Persistent notifications               COMPLETE
WebSocket notifications                COMPLETE
Search/filter/sort/pagination           COMPLETE
Dashboards                             COMPLETE
Reports/CSV export                     COMPLETE
Administrator configuration            COMPLETE
Responsive frontend                    COMPLETE
Backend automated tests                COMPLETE
Browser E2E tests                      COMPLETE
Deliberate RED run                     COMPLETE
AI Stage-3 change loop                 COMPLETE
Automatic SLA reassignment             COMPLETE
GitHub Actions CI                      COMPLETE
Documentation                          IN PROGRESS
Presentation                           PENDING
Final recorded demo                    PENDING
57. Verification Summary
At the end of the implementation and Stage-3 enhancement:
Backend
pytest -v
→ 98 passed

Backend quality
ruff check app
→ All checks passed

Frontend
npm run lint
→ passed

Frontend
npm run build
→ production build successful

Browser E2E
npx playwright test
→ 24 passed

GitHub Actions
Backend Tests
→ passed

Frontend Lint and Build
→ passed

Playwright E2E
→ 24 passed

Playwright HTML report
→ uploaded as CI artifact
58. Conclusion
SupportFlow demonstrates a complete software engineering workflow around a business problem with meaningful rules and edge cases.
The project goes beyond basic ticket CRUD by implementing:
role-specific workflows;
strict authorization;
SLA deadline enforcement;
automatic escalation;
workload-aware automatic reassignment;
auditability;
persistent and real-time notifications;
backend and browser automation;
deliberate regression detection;
AI-assisted feature evolution;
continuous integration.
Most importantly, AI assistance is paired with executable verification.
The engineering principle demonstrated throughout the project is:
Do not trust generated code because it looks correct.

Define the expected behavior.
Run it.
Test it.
Observe failures.
Diagnose them.
Correct them.
Run the full regression suite again.
That build → test → fix loop is the core engineering approach behind SupportFlow.
