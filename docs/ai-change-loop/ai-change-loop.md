# SupportFlow AI-Assisted Change Loop

## 1. Purpose

This document records the AI-assisted engineering workflow used to evolve SupportFlow after the baseline application and automated regression suites were already stable.

The goal was not simply to demonstrate that AI could generate code.

The goal was to demonstrate a controlled engineering loop:

```text
Stable System
    ↓
New Requirement
    ↓
AI-Assisted Analysis
    ↓
Implementation
    ↓
Automated Test
    ↓
Failure / Regression Detection
    ↓
Diagnosis
    ↓
Targeted Fix
    ↓
Focused Regression
    ↓
Full Regression
    ↓
CI Verification
```

Automated tests, rather than AI output alone, were used to determine correctness.

---

# 2. Baseline Before the AI-Assisted Change

Before the Stage-3 feature extension, SupportFlow already contained the core application modules.

These included:

- Authentication.
- Email OTP password reset.
- Role-based access control.
- User management.
- Ticket creation.
- Ticket assignment.
- Ticket responses.
- Internal notes.
- Ticket lifecycle.
- SLA calculation.
- SLA escalation.
- Audit trail.
- Notifications.
- WebSocket delivery.
- Search/filter/sort/pagination.
- Dashboards.
- Reports.
- Admin configuration.
- Full Requester UI.
- Full Agent UI.
- Full Admin UI.

The backend regression suite at this point contained:

```text
82 tests
```

Current browser E2E coverage contained:

```text
24 Playwright tests
```

The baseline was fully GREEN before the Stage-3 extension was introduced.

---

# 3. Why a Stable Baseline Was Important

A new feature is difficult to evaluate if the existing system is already failing.

Therefore the change loop started only after the original regression baseline was verified.

```text
pytest
→ 82 / 82 passed

Playwright
→ 24 / 24 passed

Ruff
→ passed

ESLint
→ passed

Vite production build
→ passed
```

This made later failures attributable to the new change rather than unresolved earlier defects.

---

# 4. Deliberate RED Run

Before implementing the larger Stage-3 feature, a deliberate regression exercise was performed to demonstrate that the test suite could detect a subtle business-rule defect.

The target was the SLA deadline boundary.

---

# 5. SLA Boundary Business Rule

The intended SLA rule is:

```python
current_time >= sla_deadline
```

Meaning:

```text
Before deadline
→ not breached

Exactly at deadline
→ breached

After deadline
→ breached
```

The exact-deadline boundary was protected by an existing test:

```text
test_ticket_exactly_at_sla_deadline_escalates
```

---

# 6. Deliberate Regression

The correct condition was temporarily changed from:

```python
current_time >= sla_deadline
```

to:

```python
current_time > sla_deadline
```

This created a realistic boundary defect.

At the exact deadline:

```text
current_time == sla_deadline
```

the expression:

```python
current_time > sla_deadline
```

evaluates to:

```text
False
```

Therefore the ticket incorrectly remains un-escalated at the exact SLA boundary.

---

# 7. RED Result

The focused regression test was executed.

Expected outcome:

```text
test_ticket_exactly_at_sla_deadline_escalates
FAILED
```

The surrounding boundary behavior remained valid:

```text
Before deadline       PASS
Exactly at deadline   FAIL
After deadline        PASS
```

This demonstrated that the failure was a precise SLA boundary defect rather than a general escalation failure.

---

# 8. Diagnosis

The failure was traced to the difference between:

```python
>
```

and:

```python
>=
```

The implementation was incorrectly excluding equality from the breach condition.

This type of bug is easy to miss through normal manual testing because the application behaves correctly both immediately before and immediately after the deadline.

Automated boundary testing exposed it directly.

---

# 9. Fix

The intended condition was restored:

```python
current_time >= sla_deadline
```

The focused test was rerun and returned to GREEN.

Then:

```text
SLA boundary tests
→ passed

Escalation tests
→ passed

Full backend regression
→ passed

Playwright E2E regression
→ passed
```

The broken implementation was not kept as the final application behavior.

---

# 10. Why the Deliberate RED Run Was Meaningful

The RED run demonstrated several engineering principles:

- Boundary-value testing.
- Business-rule-focused regression coverage.
- Failure reproduction.
- Root-cause isolation.
- Small targeted correction.
- Regression verification after the fix.

The defect was intentionally subtle rather than a trivial syntax error.

---

# 11. Stage-3 New Requirement

After the deliberate RED → GREEN exercise, a new business requirement was introduced.

The existing system already escalated overdue tickets.

The new requirement was:

> When an assigned ticket breaches its SLA, SupportFlow should automatically attempt to reassign it to another eligible Agent with lower workload while preserving the existing escalation behavior.

The feature was called:

```text
SLA-Based Automatic Reassignment
```

---

# 12. Why This Requirement Was Chosen

The new requirement was intentionally selected because it interacts with multiple existing modules.

It affects:

```text
SLA
Escalation
Assignment
Agent workload
Capacity rules
Audit
Notifications
Configuration
Idempotency
```

This makes it a meaningful engineering change rather than an isolated CRUD addition.

---

# 13. Requirement Rules

The feature was defined using explicit business rules.

```text
1. Trigger only when SLA breach occurs.

2. The ticket must still become ESCALATED.

3. Automatic reassignment only applies when:
   - the ticket currently has an Agent
   - automatic reassignment is enabled

4. A replacement Agent must:
   - have role AGENT
   - be active
   - not be the current Agent
   - be below configured active-ticket capacity

5. Eligible Agents are ranked by:
   lowest active workload

6. Equal workloads use:
   lowest Agent ID

7. If a replacement exists:
   assigned_agent_id changes

8. If no replacement exists:
   keep the current Agent

9. Escalation must still succeed.

10. Successful reassignment creates:
    - audit history
    - old Agent notification
    - new Agent notification

11. Existing SLA escalation audit behavior remains.

12. Reprocessing must remain idempotent.

13. Resolved and closed tickets remain excluded.

14. Existing Admin assignment/reassignment behavior must continue to work.
```

The requirements were frozen before implementation.

---

# 14. Configuration Extension

A new application configuration setting was added:

```text
auto_reassign_on_escalation
```

This allows Administrators to enable or disable automatic SLA reassignment without removing the underlying feature.

Conceptually:

```text
true
→ escalation + reassignment attempt

false
→ normal escalation only
```

The setting was integrated into the existing application configuration rather than creating a separate configuration system.

---

# 15. Database Change

The configuration extension required a schema change.

Alembic migration support was used so the new configuration property became part of managed database history.

Conceptually:

```text
Application Config Model
        ↓
Alembic Migration
        ↓
Database Column
        ↓
Admin API
        ↓
Admin UI
```

This preserved the project's migration-based schema-management approach.

---

# 16. Tests Added Before/Alongside Implementation

Dedicated regression coverage was added for automatic reassignment.

Important cases included:

```text
Least-loaded Agent selected
Current Agent excluded
Inactive Agent excluded
Capacity respected
No replacement fallback
Feature toggle disabled
Idempotent processing
Audit event generated
Old Agent notified
New Agent notified
Unrelated Agent not notified
```

The purpose of these tests was to define expected behavior rather than relying on manual inspection.

---

# 17. Least-Loaded Agent Rule

Example:

```text
Current Agent A

Agent B
Active tickets = 0

Agent C
Active tickets = 2
```

Expected replacement:

```text
Agent B
```

The selection is workload-aware rather than random.

---

# 18. Current Agent Exclusion

The existing assignee must never be selected as the replacement.

Incorrect behavior:

```text
Agent A owns ticket
        ↓
Agent A has lowest workload
        ↓
System selects Agent A again
```

Correct behavior:

```text
Current Agent removed from candidate set
        ↓
Remaining eligible Agents ranked
```

This prevents a no-op reassignment from being treated as successful reassignment.

---

# 19. Inactive Agent Exclusion

An inactive Agent cannot receive an automatically reassigned ticket.

Example:

```text
Agent B
Active = false
Workload = 0

Agent C
Active = true
Workload = 1
```

Expected result:

```text
Agent C
```

even though Agent B has the numerically smaller workload.

Eligibility is evaluated before workload ranking.

---

# 20. Capacity Enforcement

Automatic reassignment must respect the same operational capacity concept used elsewhere in the system.

Example:

```text
Maximum active tickets = 2

Agent B
Active tickets = 2

Agent C
Active tickets = 1
```

Expected result:

```text
Agent C
```

Agent B is not eligible because capacity has already been reached.

---

# 21. Deterministic Tie-Breaking

Suppose:

```text
Agent B
Active tickets = 1

Agent C
Active tickets = 1
```

The application uses Agent ID as a deterministic secondary sort key.

Conceptually:

```text
ORDER BY
active_workload ASC,
agent_id ASC
```

This ensures repeatable behavior and stable tests.

---

# 22. No-Replacement Fallback

A major invariant was:

> Failure to find a replacement must never prevent SLA escalation.

Example:

```text
Current Agent A

No alternative Agent is eligible.
```

Expected:

```text
Ticket status
→ ESCALATED

Assigned Agent
→ Agent A
```

The feature therefore extends escalation without weakening it.

---

# 23. Audit Behavior

A successful automatic reassignment records the SLA breach and the reassignment as separate facts.

Conceptually:

```text
SLA_ESCALATED

TICKET_AUTO_REASSIGNED
```

The reassignment event does not replace the original escalation event.

This preserves accountability.

---

# 24. Notification Behavior

Successful auto-reassignment affects two Agents.

### Previous Agent

Receives notification that the SLA-breached ticket was reassigned.

### New Agent

Receives notification that the escalated ticket has been assigned to them.

### Unrelated Agent

Receives no notification.

Dedicated regression tests verify this routing.

---

# 25. Idempotency Preservation

The escalation scheduler may process the system repeatedly.

Therefore the new feature was required to preserve idempotency.

Expected:

```text
First scheduler run
→ escalate
→ optionally reassign

Second scheduler run
→ no duplicate escalation
→ no duplicate reassignment

Third scheduler run
→ still no duplicate processing
```

This protects audit history and notifications from duplication.

---

# 26. AI-Assisted Implementation Approach

AI assistance was used to accelerate:

- Impact analysis.
- Identification of affected modules.
- Test-case generation.
- Service-layer implementation planning.
- Candidate-selection logic.
- Regression analysis.
- Documentation.

However, AI output was not accepted solely because it appeared reasonable.

Every important behavior was verified through tests.

---

# 27. A Representative AI Implementation Prompt

The implementation request was structured around explicit business rules rather than a vague request such as "add auto reassignment."

A representative prompt was:

> Implement SLA-based automatic reassignment for escalated tickets. Reuse the existing assignment and capacity logic rather than duplicating business rules. When an assigned ticket first breaches SLA and auto-reassignment is enabled, choose the least-loaded active Agent below configured capacity, exclude the current assignee, use Agent ID as the deterministic tie-breaker, reassign if possible, and preserve existing escalation audit, notification, and idempotency behavior. If no replacement exists, escalate normally without reassignment.

This provided AI with clear acceptance criteria.

---

# 28. Why Tests Were Still Required

Even a plausible AI-generated implementation could contain mistakes such as:

- Selecting the existing Agent again.
- Ignoring Agent capacity.
- Selecting inactive Agents.
- Failing escalation when no replacement exists.
- Creating duplicate notifications.
- Reassigning repeatedly on scheduler retries.
- Replacing the existing escalation audit event.
- Not respecting the feature toggle.

These cases are difficult to validate safely through manual happy-path testing alone.

---

# 29. Focused Regression Strategy

After implementation, focused tests were used first.

For example:

```text
tests/escalation/test_auto_reassignment.py
```

This made it easier to isolate feature-specific failures before running the full suite.

Then related areas were checked:

```text
Escalation tests
SLA boundary tests
Notification tests
Audit tests
Configuration tests
```

Only after those passed was the entire backend regression suite executed.

---

# 30. Final Backend Result

After completing the Stage-3 change, the backend suite grew from:

```text
82 tests
```

to:

```text
98 tests
```

Final result:

```text
98 passed
```

This means the new behavior was added while preserving previous regression coverage.

---

# 31. Browser Regression Result

The existing Playwright suite was rerun after the backend feature change.

Result:

```text
24 passed
```

Important browser workflows remained functional, including:

- Authentication.
- Ticket creation.
- Assignment.
- Agent workflow.
- Resolution.
- Requester close flow.
- Internal-note privacy.
- Role routing.
- WebSocket notification.
- Admin configuration.
- Responsive navigation.

---

# 32. Code Quality Verification

Backend:

```text
ruff check app
→ All checks passed
```

Frontend:

```text
npm run lint
→ passed
```

Production build:

```text
npm run build
→ passed
```

The change was therefore checked beyond functional tests alone.

---

# 33. GitHub Actions Verification

The complete application was then verified through GitHub Actions.

CI includes:

```text
Backend Tests
Frontend Lint and Build
Playwright E2E
```

The browser job:

- Creates a clean E2E database.
- Runs Alembic migrations.
- Seeds deterministic E2E accounts.
- Starts FastAPI.
- Starts Vite.
- Installs Chromium.
- Executes all Playwright tests.
- Uploads the Playwright HTML report.

The workflow completed successfully.

---

# 34. Final Verification State

The final engineering baseline is:

```text
Backend pytest
98 / 98 passed

Backend Ruff
passed

Frontend ESLint
passed

Frontend production build
passed

Playwright
24 / 24 passed

GitHub Actions
passed
```

---

# 35. Evidence Chain

The complete assessment evidence can be summarized as:

```text
1. Stable baseline
   82 backend tests
   24 E2E tests

2. Deliberate SLA regression
   >= changed to >

3. Existing exact-boundary test
   RED

4. Root cause identified
   equality excluded

5. Correct rule restored
   GREEN

6. New Stage-3 requirement
   SLA auto-reassignment

7. AI-assisted impact analysis
   assignment + SLA + audit + notifications + configuration

8. New focused tests
   eligibility + capacity + fallback + idempotency

9. Feature implemented

10. Related regressions verified

11. Backend suite expanded
    82 → 98 tests

12. Playwright suite
    24 / 24 passed

13. GitHub Actions
    clean-environment verification passed
```

---

# 36. Engineering Lessons

Several engineering lessons came from the change loop.

## AI Is an Accelerator, Not a Test Oracle

AI can generate plausible code quickly, but plausible code is not the same as verified code.

Tests determine whether the implementation satisfies the business requirement.

## Business Rules Need Boundary Tests

The deliberate `>=` versus `>` regression demonstrated how a one-character change can violate SLA behavior while remaining difficult to detect manually.

## New Features Can Break Existing Behavior Indirectly

Automatic reassignment touches multiple modules even though the visible requirement sounds simple.

Impact analysis is therefore important before implementation.

## Idempotency Matters for Background Jobs

Scheduler-driven workflows must expect repeated execution.

Operations should not create duplicate side effects when the same condition is processed more than once.

## Security and Privacy Need Dedicated Tests

Features such as internal notes and cross-ticket access should be verified explicitly rather than inferred from the UI.

## CI Reduces Machine-Specific Confidence

A clean GitHub runner provides stronger evidence than a successful local run alone.

---

# 37. Final AI-Assisted Development Model

The final SupportFlow engineering model is:

```text
Define Requirement
       ↓
Identify Business Rules
       ↓
Identify Affected Modules
       ↓
Add / Update Tests
       ↓
AI-Assisted Implementation
       ↓
Run Focused Tests
       ↓
Failure?
   ┌───┴───┐
   │       │
  Yes      No
   │       │
   ▼       │
Analyze    │
   ↓       │
Fix        │
   └───┬───┘
       ▼
Related Regression Tests
       ↓
Full pytest Suite
       ↓
Frontend Lint / Build
       ↓
Playwright E2E
       ↓
GitHub Actions
       ↓
Verified Change
```

This workflow makes AI-assisted development controlled, explainable, and test-driven rather than relying on unverified generated code.
