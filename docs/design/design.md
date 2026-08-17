# SupportFlow System Design

## 1. Purpose

SupportFlow is designed to solve a specific operational problem: high-priority support tickets should not remain unattended simply because nobody manually noticed that their response or resolution window had expired.

The system therefore treats ticket priority as an enforceable business rule rather than only a visual label.

The design combines:

- Role-based ticket workflows.
- Configurable SLA rules.
- Automatic SLA breach detection.
- Escalation processing.
- Automatic Agent reassignment.
- Persistent audit history.
- Persistent and real-time notifications.
- Administrative configuration.
- Automated regression testing.

---

## 2. Core Design Goals

SupportFlow was designed around the following goals.

### 2.1 Enforce Priority

Priority determines an SLA window.

```text
Priority
   ↓
SLA Configuration
   ↓
Deadline
   ↓
Automatic Monitoring
```

A high-priority ticket therefore has actual system behavior associated with its priority.

### 2.2 Minimize Manual Monitoring

Supervisors should not have to continuously inspect tickets to discover SLA breaches.

The scheduler and escalation engine perform this automatically.

### 2.3 Maintain Accountability

Important ticket events are written to an audit trail.

The system can therefore answer:

```text
Who performed the action?
What happened?
When did it happen?
What changed?
```

### 2.4 Enforce Security

Authorization is enforced by the backend.

Hiding a frontend button is not treated as sufficient security.

### 2.5 Preserve Testability

Business rules are placed primarily in services so they can be tested independently from browser behavior.

---

# 3. User Role Design

SupportFlow has three primary application roles.

```text
REQUESTER
AGENT
ADMIN
```

Each role represents a different responsibility within the support process.

---

## 3.1 Requester

The Requester represents the person reporting an issue.

Primary capabilities include:

- Register and authenticate.
- Create support tickets.
- Select ticket priority.
- View owned tickets.
- Search and filter owned tickets.
- View ticket status and SLA information.
- Add public responses.
- Receive notifications.
- View public conversation history.
- Close resolved tickets.
- Manage profile information.

A Requester cannot:

- Manage other users.
- Access another Requester's ticket.
- Create internal notes.
- Assign Agents.
- Change SLA configuration.
- Access administrative reports.
- Access administrative configuration.

---

## 3.2 Agent

The Agent represents the person responsible for resolving assigned support issues.

Primary capabilities include:

- View assigned tickets.
- View escalated tickets.
- Start work.
- Add public responses.
- Add internal notes.
- Resolve tickets.
- Receive assignment notifications.
- Receive escalation/reassignment notifications.
- View relevant ticket history.

An Agent cannot perform administrative operations simply because they are responsible for ticket resolution.

---

## 3.3 Administrator

The Administrator controls operational configuration and support management.

Primary capabilities include:

- View system-wide ticket information.
- Assign and reassign tickets.
- Manage users.
- Activate/deactivate Agents.
- Configure SLA rules.
- Configure application behavior.
- Access reports.
- Export ticket information.
- Monitor dashboards and operational metrics.

Administrative capabilities are protected by backend role checks.

---

# 4. Authentication Design

SupportFlow uses JWT-based authentication.

The login process is:

```text
Email + Password
       ↓
Credential Validation
       ↓
JWT Generated
       ↓
Authenticated Session
       ↓
JWT Sent with Protected Requests
       ↓
Backend Resolves Current User
```

Authentication and authorization are intentionally separated.

Authentication answers:

> Who is the user?

Authorization answers:

> Is this user allowed to perform this operation?

---

# 5. Registration Design

Public registration is intentionally restricted.

A user registering through the public registration flow becomes a Requester.

The client is not trusted to choose a privileged role.

Incorrect design:

```json
{
  "email": "user@example.com",
  "role": "ADMIN"
}
```

A malicious client should not be able to become an Administrator by modifying a request payload.

Therefore, privileged account creation remains under administrative control.

This behavior is protected by automated regression testing.

---

# 6. Forgot Password Design

Password recovery uses email OTP verification.

```text
User enters email
        ↓
Forgot-password request
        ↓
OTP generated
        ↓
OTP record stored
        ↓
OTP delivered by email
        ↓
User enters OTP
        ↓
OTP verification
        ↓
Password reset allowed
        ↓
New password stored securely
```

Separating OTP verification from password reset prevents the reset page alone from being sufficient authorization to change a password.

---

# 7. Ticket Design

A ticket represents a support issue raised by a Requester.

Important ticket information includes concepts such as:

- Ticket number.
- Requester.
- Assigned Agent.
- Title.
- Description.
- Priority.
- Status.
- SLA deadline.
- Escalation state.
- Creation/update timestamps.
- Resolution information.

Ticket numbers provide a human-readable identifier in addition to internal database IDs.

---

# 8. Ticket Priority Design

Ticket priority determines operational urgency.

Priority is connected to SLA configuration rather than being only a display badge.

Conceptually:

```text
LOW
MEDIUM
HIGH
CRITICAL
   │
   ▼
SLA Configuration
   │
   ▼
Deadline
```

This allows administrators to control the SLA duration associated with each supported priority.

---

# 9. Ticket Lifecycle Design

The primary lifecycle is:

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

Additional states/flows include escalation and reopening where supported by the workflow.

The lifecycle is controlled rather than allowing arbitrary status changes.

For example:

```text
ASSIGNED
    ↓
IN_PROGRESS
    ↓
RESOLVED
```

An assigned ticket should not bypass required workflow rules simply because a client sends a different status value.

---

# 10. Why Status Transitions Are Controlled

Allowing unrestricted status modification would create inconsistent operational history.

For example, this would be problematic:

```text
OPEN
 ↓
CLOSED
```

without assignment, work, or resolution behavior where the business workflow requires those stages.

Therefore, status transitions are implemented through business operations rather than unrestricted generic updates.

This improves:

- Data integrity.
- Auditability.
- Testability.
- User-interface consistency.

---

# 11. Ticket Assignment Design

Administrators can assign tickets to eligible Agents.

Assignment affects several parts of the system:

```text
Admin Assignment
       ↓
Ticket assigned_agent changes
       ↓
Ticket status/workflow updated
       ↓
Audit event
       ↓
Agent notification
       ↓
Live WebSocket delivery
```

Assignment is therefore a business operation, not merely a database field update.

---

# 12. Ticket Response Design

SupportFlow distinguishes between two communication types.

```text
PUBLIC RESPONSE
INTERNAL NOTE
```

### Public Response

A public response participates in the Requester-Agent conversation.

It can be visible to the Requester and authorized support personnel.

### Internal Note

An internal note is for internal support collaboration.

It must not be exposed to the Requester.

This privacy rule is enforced by the backend rather than relying only on frontend filtering.

---

# 13. Internal Note Privacy Design

The important security rule is:

```text
Agent/Admin Internal Note
           │
           ├────────► Authorized Support View
           │
           └──── X ─► Requester
```

This prevents accidental information disclosure.

The rule is covered by both backend and browser-level automated tests.

---

# 14. SLA Design

SLA behavior is one of the central business rules in SupportFlow.

For a ticket:

```text
Ticket Created
      ↓
Priority
      ↓
SLA Configuration
      ↓
SLA Deadline
```

The system later compares the current time against this deadline.

---

# 15. SLA Boundary Rule

The SLA breach rule uses an inclusive deadline.

Correct behavior:

```python
current_time >= sla_deadline
```

Therefore:

```text
current_time < deadline   → not breached

current_time = deadline   → breached

current_time > deadline   → breached
```

The exact-deadline case is intentionally covered by a regression test because boundary comparisons are a common source of subtle defects.

---

# 16. Why the Deadline Is Inclusive

If an SLA promises resolution within a specific window, the ticket has exhausted that window when the deadline itself is reached.

Using:

```python
current_time > sla_deadline
```

would incorrectly create a gap at the exact deadline.

Therefore:

```python
>=
```

is the intended business behavior.

---

# 17. SLA Configuration Design

SLA values are database-backed rather than hardcoded throughout the application.

This means administrators can modify SLA configuration without changing source code.

Conceptually:

```text
Admin
  ↓
SLA Settings
  ↓
Database Configuration
  ↓
Future Ticket SLA Calculation
```

Validation prevents invalid SLA values from being accepted.

Automated tests cover:

- Valid administrative updates.
- Unauthorized access.
- Invalid durations.
- Invalid priorities.
- Disabled SLA behavior.
- Database-backed SLA usage.

---

# 18. Escalation Design

The scheduler periodically evaluates eligible tickets.

Conceptually:

```text
Scheduled SLA Check
        ↓
Find Candidate Tickets
        ↓
Evaluate Deadline
        ↓
Breached?
    ┌───┴───┐
    │       │
   No      Yes
    │       │
  Stop      ▼
         Escalate
```

Escalation triggers additional business behavior such as audit recording and notification.

---

# 19. Escalation Eligibility

Not every ticket should be escalated.

Examples of tickets excluded from normal escalation processing include:

```text
Resolved tickets
Closed tickets
Already escalated tickets
Tickets that have not reached the deadline
```

These exclusions prevent invalid or duplicate escalation.

---

# 20. Idempotency Design

Background jobs can run repeatedly.

Therefore, escalation must be idempotent.

Meaning:

```text
First processing
      ↓
Ticket escalated

Second processing
      ↓
No duplicate escalation

Third processing
      ↓
No duplicate escalation
```

Without idempotency, repeated scheduler execution could produce:

- Duplicate audit events.
- Duplicate notifications.
- Repeated reassignment.
- Incorrect ticket history.

Automated tests explicitly verify this property.

---

# 21. Stage-3 Automatic Reassignment Design

The Stage-3 extension adds a new requirement:

> When an assigned ticket breaches its SLA, the system should attempt to move it to another eligible Agent rather than only flagging it as escalated.

However, the feature must not break the original escalation behavior.

Therefore:

```text
SLA breach
    ↓
Escalation ALWAYS remains valid
    ↓
Automatic reassignment is an additional action
```

This distinction is important.

---

# 22. Automatic Reassignment Configuration

Automatic reassignment can be controlled through application configuration.

Conceptually:

```text
auto_reassign_on_escalation = true
            ↓
Attempt reassignment


auto_reassign_on_escalation = false
            ↓
Escalate only
```

This allows the organization to change operational behavior without removing the underlying feature.

---

# 23. Agent Eligibility Design

A replacement Agent must satisfy eligibility rules.

Candidate selection conceptually performs:

```text
All Agents
    ↓
Active?
    ↓
Not current Agent?
    ↓
Within capacity?
    ↓
Eligible
```

This prevents reassignment to:

- The same Agent.
- Inactive Agents.
- Agents who have reached the defined workload capacity.

---

# 24. Least-Loaded Agent Design

Eligible Agents are compared by active workload.

Conceptually:

```text
Agent A → 5 active tickets
Agent B → 2 active tickets
Agent C → 4 active tickets
```

The preferred replacement is:

```text
Agent B
```

because Agent B has the smallest active workload.

This creates a simple workload-aware reassignment strategy.

---

# 25. Deterministic Tie-Breaking

Suppose:

```text
Agent A → 2 active tickets
Agent B → 2 active tickets
```

The system should not make unpredictable choices between equally loaded Agents.

A deterministic secondary ordering is therefore used.

Conceptually:

```text
ORDER BY
    active_workload ASC,
    agent_id ASC
```

This makes behavior repeatable and easier to test.

---

# 26. Capacity Design

Least-loaded does not automatically mean available.

For example:

```text
Agent A → 10 / 10 active tickets
Agent B → 10 / 10 active tickets
```

Neither Agent should receive another ticket merely because one is technically tied for the lowest workload.

Capacity rules are therefore considered during candidate selection.

This prevents automatic reassignment from simply moving SLA problems between overloaded Agents.

---

# 27. No-Replacement Fallback

A critical design requirement is that reassignment failure must not cancel escalation.

If no replacement Agent exists:

```text
SLA Breach
     ↓
Escalated
     ↓
Search replacement
     ↓
None available
     ↓
Keep current Agent
```

The ticket remains escalated.

This preserves the original SLA business guarantee.

---

# 28. Automatic Reassignment Side Effects

Successful automatic reassignment affects multiple modules.

```text
Automatic Reassignment
         │
         ├── Ticket assignment
         ├── Audit history
         ├── Old Agent notification
         └── New Agent notification
```

Unrelated Agents should not receive reassignment notifications.

These behaviors are individually covered by automated tests.

---

# 29. Audit Trail Design

SupportFlow uses append-oriented audit events to record significant ticket activity.

An audit entry provides historical evidence rather than representing only the current ticket state.

Conceptually:

```text
Ticket Current State
        +
Historical Audit Events
        =
Explainable Ticket History
```

Important events include assignment, workflow changes, escalation, and automatic reassignment.

---

# 30. Why Audit Records Are Separate

If only the current ticket record were stored:

```text
assigned_agent_id = 5
```

we would know the current Agent but not necessarily:

```text
Who assigned the Agent?
Who was assigned previously?
When did reassignment occur?
Was the change caused by SLA escalation?
```

Separate audit records preserve that history.

---

# 31. Notification Design

Notifications are event-driven.

Examples:

```text
Ticket Assigned
      ↓
Notify Agent


SLA Reassignment
      ↓
Notify Old Agent
      ↓
Notify New Agent
```

Notifications are persisted before/alongside live delivery.

This ensures that real-time delivery is an enhancement rather than the only record of the notification.

---

# 32. WebSocket Design

REST and WebSockets solve different problems.

REST is used for:

```text
Fetching tickets
Creating tickets
Updating workflow
Reading notifications
Configuration
Reports
```

WebSockets are used for:

```text
Immediate live notification delivery
```

The combination provides both reliability and responsiveness.

---

# 33. Why Notifications Are Persisted

A WebSocket-only design would lose notifications when the recipient is offline.

SupportFlow instead uses:

```text
Business Event
     ↓
Persistent Notification
     ↓
WebSocket Attempt
```

If the WebSocket connection is unavailable, the notification still exists and can be retrieved later.

---

# 34. Dashboard Design

Each role receives dashboard information appropriate to its responsibilities.

```text
Requester Dashboard
→ personal ticket information


Agent Dashboard
→ assigned/escalated workload


Admin Dashboard
→ system-wide operational information
```

Backend role checks prevent a user from obtaining another role's dashboard merely by manually calling its API.

---

# 35. Reports Design

Reports are administrative operational tools.

Report access is restricted because reports can expose system-wide information.

SupportFlow provides report summary functionality and CSV export.

The export response uses appropriate attachment behavior so the frontend can download the generated report.

---

# 36. Search, Filter, Sort and Pagination Design

Ticket lists can grow over time.

Therefore list views support operational navigation features such as:

```text
Search
Filters
Sorting
Pagination
```

These features improve usability while preventing the UI from becoming dependent on rendering an unrestricted number of records.

---

# 37. Error Handling Design

Errors should be predictable for both frontend code and users.

The backend therefore maps failures to appropriate HTTP responses.

Examples include:

```text
400 → invalid business request
401 → unauthenticated
403 → authenticated but forbidden
404 → resource not found
409 → conflicting resource/state
422 → request validation failure
```

The frontend converts API failures into user-facing error states or notifications instead of exposing raw stack traces.

---

# 38. Security Boundary Design

The backend is the authoritative security layer.

Correct model:

```text
Frontend restriction
       +
Backend authorization
       =
Protected operation
```

Incorrect model:

```text
Hide button
    ↓
Assume secure
```

A malicious or technically knowledgeable client can call APIs directly, so every sensitive backend operation must enforce authorization independently.

---

# 39. Horizontal Access Protection

SupportFlow prevents users with the same role from automatically accessing each other's resources.

Example:

```text
Requester A ──► Ticket A  ✓

Requester A ──► Ticket B  ✗
Requester B ──► Ticket B  ✓
```

This protects against horizontal privilege escalation.

---

# 40. Testability Design

The application separates business rules from presentation logic so important behaviors can be verified at multiple levels.

```text
Business Rule
    ↓
pytest
    ↓
API / Service Verification
```

and:

```text
Real User Workflow
    ↓
Playwright
    ↓
Browser Verification
```

The two layers complement rather than replace one another.

---

# 41. Deliberate Regression Design

The assessment includes a deliberate RED run around the SLA boundary.

Correct:

```python
current_time >= sla_deadline
```

Deliberately broken:

```python
current_time > sla_deadline
```

Expected consequence:

```text
Before deadline        PASS
Exactly at deadline    FAIL
After deadline         PASS
```

The purpose was to prove that the regression suite protects a real business rule.

The correct implementation was then restored and the complete regression suite returned to GREEN.

---

# 42. Test Data Isolation Design

Backend tests and browser E2E tests intentionally use different SQLite databases.

```text
Development
supportflow.db


Backend pytest
test_supportflow.db


Browser E2E
supportflow_e2e.db
```

pytest can aggressively control its test data without affecting the persistent seeded users required by Playwright.

---

# 43. CI Design

Local success alone is not treated as sufficient verification.

GitHub Actions reproduces automated verification on a clean runner.

The CI workflow verifies:

```text
Backend dependencies
Ruff
pytest

Frontend dependencies
ESLint
Vite production build

E2E database setup
Backend startup
Frontend startup
Playwright Chromium
24 E2E tests
Playwright report artifact
```

This reduces dependence on local machine state.

---

# 44. Design Tradeoffs

## SQLite vs PostgreSQL

SQLite was selected for the assessment implementation because it provides:

- Minimal setup.
- Simple reviewer execution.
- Easy test database isolation.
- No external database service requirement.

For larger production deployments, PostgreSQL would provide stronger concurrency and operational characteristics.

---

## Direct Scheduler vs Distributed Workers

The current scheduler keeps the assessment environment easy to run.

A larger deployment could move SLA jobs to distributed workers with locking and retry infrastructure.

---

## Direct WebSocket Management vs Shared Pub/Sub

Direct connection management is appropriate for the current application architecture.

Multiple backend replicas would benefit from a shared pub/sub system such as Redis.

---

## Simple Workload Balancing vs Advanced Routing

Least-loaded eligible Agent selection is understandable, deterministic, and testable.

A larger support organization could later incorporate:

- Agent skills.
- Ticket category.
- Time zone.
- Shift availability.
- Historical resolution performance.
- Customer tier.

These are future routing enhancements rather than requirements of the current system.

---

# 45. Design Principles Summary

SupportFlow follows these core design principles:

1. Priority must affect system behavior.
2. SLA enforcement must be automatic.
3. Background processing must be idempotent.
4. Escalation must succeed even when reassignment cannot.
5. Automatic reassignment must respect eligibility and capacity.
6. Security must be enforced by the backend.
7. Internal information must remain private.
8. Important actions must be auditable.
9. Real-time notifications must not replace persistence.
10. Business rules must have automated regression coverage.
11. New AI-assisted changes must preserve existing behavior.
12. CI must independently reproduce verification.

These decisions allow SupportFlow to operate as more than a CRUD ticket application: its behavior is driven by explicit, testable business rules.
