# SupportFlow User Guide

## 1. Overview

SupportFlow is a support ticket management system used by three primary roles:

```text
Requester
Agent
Administrator
```

Each role has a different workflow and level of access.

This guide explains how to use the application from a user's perspective.

---

# 2. Accessing SupportFlow

Start the backend and frontend locally.

Backend:

```text
http://127.0.0.1:8000
```

Frontend:

```text
http://127.0.0.1:5173
```

Open the frontend URL in a browser.

---

# 3. User Roles

## Requester

A Requester raises support tickets and follows their progress.

Typical actions:

- Register.
- Login.
- Create tickets.
- View owned tickets.
- Add public responses.
- Track SLA information.
- Receive notifications.
- Reopen or close resolved tickets.

## Agent

An Agent works on assigned support tickets.

Typical actions:

- View assigned tickets.
- Start work.
- Add public responses.
- Add internal notes.
- View escalated tickets.
- Resolve tickets.
- Receive assignment and SLA notifications.

## Administrator

An Administrator manages support operations.

Typical actions:

- View all tickets.
- Assign and reassign tickets.
- Monitor Agent workload.
- Manage users.
- Configure SLA rules.
- Configure application behavior.
- Access reports and exports.

---

# 4. Registration

Public registration is available for Requesters.

Open:

```text
/register
```

Enter:

- Full name.
- Email address.
- Password.
- Confirm password.

Submit the form.

A successful registration creates a Requester account.

Public users cannot choose Agent or Admin as their role.

---

# 5. Login

Open:

```text
/login
```

Enter:

- Email.
- Password.

Select:

```text
Sign in
```

After successful authentication, SupportFlow redirects the user to the dashboard for their role.

Typical redirects:

```text
Requester → /requester
Agent     → /agent
Admin     → /admin
```

Invalid credentials display an error and do not create an authenticated session.

---

# 6. Forgot Password

If a user forgets their password:

1. Open the login page.
2. Select the Forgot Password option.
3. Enter the account email address.
4. Submit the request.

The backend creates a one-time password verification flow.

---

# 7. OTP Verification

After requesting password recovery:

1. Retrieve the OTP from the configured email account.
2. Open the OTP verification page.
3. Enter the verification code.
4. Submit the OTP.

A valid OTP allows the user to proceed to password reset.

Invalid or expired OTP values are rejected.

---

# 8. Reset Password

After successful OTP verification:

1. Enter the new password.
2. Confirm the new password.
3. Submit the reset request.

After successful reset, return to Login and authenticate with the new password.

---

# 9. Profile

Authenticated users can access:

```text
/profile
```

The Profile page allows users to view account information and supported profile settings.

Password-change functionality is protected and requires an authenticated session.

---

# 10. Requester Dashboard

After Requester login, SupportFlow opens:

```text
/requester
```

The dashboard provides an overview of the Requester's support activity.

Depending on available ticket data, the dashboard can display ticket summary information and recent activity.

Use the sidebar to access:

```text
Dashboard
My Tickets
Create Ticket
Notifications
Profile
```

---

# 11. Create a Ticket

Open:

```text
/requester/tickets/create
```

Complete the ticket form.

Typical information includes:

- Title.
- Description.
- Category.
- Priority.

Select the priority carefully because priority determines the SLA window applied to the ticket.

Submit:

```text
Create Ticket
```

After successful creation, SupportFlow opens the ticket details page.

---

# 12. Ticket Priority

Supported priorities include:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Priority affects the ticket's SLA deadline.

A higher-priority ticket can therefore have a shorter allowed resolution window depending on Admin SLA configuration.

---

# 13. My Tickets

Open:

```text
/requester/tickets
```

The Requester can view only tickets they own.

Available queue functionality includes:

- Search.
- Priority filtering.
- Status filtering where available.
- Sorting.
- Pagination.

A Requester cannot access another Requester's ticket by manually changing the ticket URL.

---

# 14. Ticket Details

Open a ticket from the Requester ticket list.

The page can include:

- Ticket number.
- Title.
- Description.
- Priority.
- Status.
- Assigned Agent information.
- SLA information.
- Conversation history.
- Audit timeline.
- Resolution summary when available.

---

# 15. SLA Information

SupportFlow calculates an SLA deadline according to the ticket priority and current SLA configuration.

A ticket may show information indicating:

- SLA deadline.
- SLA usage.
- SLA risk.
- Escalated state.

The Requester does not manually escalate the ticket.

Escalation is handled automatically by backend SLA processing.

---

# 16. Requester Public Response

A Requester can participate in the ticket conversation.

Open the Ticket Details page and enter a response in the conversation form.

Submit the message.

Requester responses are public responses.

Requesters cannot create internal support notes.

---

# 17. Internal Notes

Internal notes are reserved for authorized support personnel.

A Requester will not see Agent/Admin internal notes in the conversation.

This privacy rule is enforced by the backend.

---

# 18. Resolved Ticket

After an Agent resolves the issue, the ticket enters:

```text
RESOLVED
```

The Requester can view the resolution summary provided by the Agent.

Depending on application configuration, the Requester can then:

```text
Close Ticket
```

or:

```text
Reopen
```

---

# 19. Closing a Ticket

For a resolved ticket:

1. Select `Close Ticket`.
2. Review the confirmation dialog.
3. Confirm the action.

The ticket moves to:

```text
CLOSED
```

Closed tickets cannot receive additional conversation responses.

---

# 20. Reopening a Ticket

If Requester reopen behavior is enabled:

1. Open a resolved ticket.
2. Select `Reopen`.
3. Confirm the action.

The ticket returns to the active support workflow.

The assigned Agent can then continue working on it.

If reopen behavior is disabled through Admin Configuration, this operation is not available.

---

# 21. Requester Notifications

Select the notification bell in the application header.

The bell shows the number of unread notifications.

Requester notifications can include ticket activity such as:

- Public support responses.
- Ticket resolution.
- Other permitted workflow updates.

Select a ticket notification to open the associated ticket.

---

# 22. Notifications Page

Open:

```text
/notifications
```

Users can:

- View notification history.
- Filter read/unread notifications.
- Mark individual notifications as read.
- Mark all notifications as read.

Notifications are persisted in the database.

---

# 23. Real-Time Notifications

When WebSocket notifications are enabled and the browser is connected, new notifications can arrive without page refresh.

The notification bell updates immediately.

If WebSocket connectivity is temporarily lost, persistent notifications remain available and can be recovered after reconnect.

---

# 24. Agent Dashboard

After Agent login, SupportFlow opens:

```text
/agent
```

The Agent Dashboard can display information such as:

- Total assigned tickets.
- Active tickets.
- Assigned tickets.
- In-progress tickets.
- Escalated tickets.
- Resolved tickets.
- SLA-at-risk tickets.
- Response/resolution metrics where available.

Use the sidebar to access:

```text
Dashboard
Assigned Tickets
Escalated
Notifications
Profile
```

---

# 25. Assigned Tickets

Open:

```text
/agent/tickets
```

This page shows tickets assigned to the current Agent.

The Agent can use:

- Search.
- Priority filtering.
- Status filtering.
- Sorting.
- Pagination.

The assigned queue can be sorted using SLA deadline so tickets closest to deadline can be prioritized.

---

# 26. Agent Ticket Access

An Agent can work only on tickets they are authorized to access.

An Agent cannot open another Agent's ticket by manually changing the URL.

Backend authorization protects this boundary.

---

# 27. Start Work

For an assigned ticket in the appropriate state:

1. Open Ticket Details.
2. Select `Start Work`.

The ticket moves from:

```text
ASSIGNED
```

to:

```text
IN_PROGRESS
```

The Start Work action is not shown for states where the transition is invalid.

---

# 28. Agent Public Response

On Ticket Details:

1. Enter a response.
2. Leave `Internal note` unchecked.
3. Submit the response.

The Requester can see this message.

The first public Agent response can also contribute to response-time metrics.

---

# 29. Agent Internal Note

To create a support-only note:

1. Open Ticket Details.
2. Enter the note.
3. Check `Internal note`.
4. Submit.

The note is visible to authorized support users but hidden from the Requester.

Use internal notes for information that should not appear in the customer-facing conversation.

---

# 30. Escalated Tickets

Open:

```text
/agent/escalated
```

This queue displays tickets assigned to the Agent that have entered an escalated state.

Escalated tickets require immediate operational attention.

The Agent can continue working and can resolve an escalated ticket according to the ticket workflow.

---

# 31. Resolve a Ticket

For an eligible active ticket:

1. Open Ticket Details.
2. Enter a clear resolution summary.
3. Select `Resolve Ticket`.
4. Review the confirmation dialog.
5. Confirm.

The ticket moves to:

```text
RESOLVED
```

The resolution summary is saved and becomes visible on the ticket.

---

# 32. Agent Notifications

Agents can receive notifications for events such as:

- Ticket assignment.
- Ticket reassignment.
- Requester public response.
- Ticket reopen.
- Ticket close.
- SLA warning.
- SLA escalation.
- Automatic SLA reassignment.

When real-time delivery is enabled, these notifications can appear without refreshing the browser.

---

# 33. Administrator Dashboard

After Admin login, SupportFlow opens:

```text
/admin
```

The dashboard provides system-wide operational visibility.

Metrics can include:

- Total tickets.
- Active tickets.
- Unassigned tickets.
- Escalated tickets.
- SLA-at-risk tickets.
- Resolved tickets.
- Requester count.
- Active Agent count.
- Agent workload.

---

# 34. All Tickets

Open:

```text
/admin/tickets
```

Administrators can view the complete support queue.

Available tools include:

- Search.
- Priority filtering.
- Status filtering.
- Assigned/unassigned filtering.
- SLA-at-risk filtering.
- SLA-breached filtering.
- Sorting.
- Pagination.

Admin search can include Requester information where supported by the backend.

---

# 35. Assign a Ticket

For an unassigned ticket:

1. Open Ticket Details.
2. Locate `Admin Actions`.
3. Select an eligible Agent.
4. Select `Assign Ticket`.

The ticket becomes assigned to that Agent.

The operation also creates audit and notification behavior.

---

# 36. Reassign a Ticket

For an already assigned ticket:

1. Open Ticket Details.
2. Select another eligible Agent.
3. Select `Reassign Ticket`.

The existing Agent assignment is replaced.

The affected Agents receive the appropriate notification behavior.

---

# 37. Agent Capacity

SupportFlow can limit how many active tickets an Agent may have.

If an Agent has reached the configured workload capacity, assignment can be rejected.

The Admin should select another eligible Agent.

---

# 38. Change Ticket Priority

Administrators can change ticket priority from the ticket's Admin Actions area where supported.

After selecting the new priority:

1. Save the priority change.
2. Confirm the updated ticket information.
3. Review the audit timeline if needed.

Priority changes are business actions and are auditable.

---

# 39. Admin Responses and Internal Notes

Administrators can participate in support conversations where application configuration permits.

### Public Response

Visible to the Requester.

### Internal Note

Visible only to authorized support staff.

Admin public responses can be controlled through application configuration.

---

# 40. User Management

Open:

```text
/admin/users
```

Administrators can:

- Search users.
- Filter by role.
- View account status.
- Activate users.
- Deactivate users.

Agent accounts can also be created through the supported administrative user-management flow.

---

# 41. Deactivate a User

From User Management:

1. Locate the user.
2. Select `Deactivate`.
3. Review the confirmation.
4. Confirm.

The user's account becomes inactive.

Use this carefully for Agent accounts that may currently have assigned work.

---

# 42. Reactivate a User

Locate an inactive user and select:

```text
Activate
```

After confirmation, the user regains active account status.

---

# 43. SLA Settings

Open:

```text
/admin/sla
```

Administrators can view and modify SLA durations for supported ticket priorities.

Typical priorities include:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Enter a valid positive duration and save.

Invalid SLA configurations are rejected by backend validation.

---

# 44. Application Configuration

Open:

```text
/admin/config
```

Operational settings can include:

- SLA warning threshold.
- Escalation check interval.
- Maximum active tickets per Agent.
- Requester reopen behavior.
- Admin public responses.
- Persistent notifications.
- WebSocket notifications.
- Automatic reassignment after SLA breach.

Save changes after reviewing the values.

---

# 45. Automatic SLA Reassignment

When:

```text
auto_reassign_on_escalation = true
```

an assigned ticket that first breaches its SLA can be automatically moved to another eligible Agent.

The replacement Agent must:

- Be active.
- Have the Agent role.
- Not be the current Agent.
- Be below workload capacity.

Eligible Agents are ranked by active workload.

If workloads are equal, deterministic tie-breaking is used.

If no replacement exists, the ticket remains assigned to its current Agent but still becomes escalated.

---

# 46. What Users See During Auto-Reassignment

The previous Agent can receive a notification informing them that the overdue ticket was reassigned.

The new Agent can receive a notification that an escalated ticket was assigned to them.

The ticket's audit timeline records the relevant escalation and reassignment history.

---

# 47. Reports

Open:

```text
/admin/reports
```

The Admin can review operational report information.

Reports can include:

- Ticket summary information.
- SLA breach information.
- Agent performance information.

Date filters can be applied where supported.

---

# 48. CSV Exports

From Reports, the Admin can download supported CSV exports such as:

```text
Ticket Report
SLA Breach Report
Agent Performance Report
```

The browser downloads the generated CSV file.

---

# 49. Audit Timeline

Ticket Details contains an audit/activity history.

This history helps explain events such as:

```text
Ticket Created
Assigned
Work Started
Response Added
Priority Changed
SLA Escalated
Automatically Reassigned
Resolved
Reopened
Closed
```

System-generated events may display the actor as `System`.

---

# 50. Unauthorized Pages

If a user attempts to access a page outside their role, SupportFlow redirects them to an unauthorized page or returns the appropriate backend authorization error.

Examples:

```text
Requester → /admin       denied
Agent     → /admin       denied
Admin     → /requester   denied
```

The frontend route guard improves navigation safety, while the backend remains the authoritative security layer.

---

# 51. Common Error States

## Invalid Login

Check:

- Email.
- Password.
- Account active status.

## Unauthorized

The authenticated role does not have permission for the requested operation.

## Ticket Not Found

The ticket may not exist, or the authenticated user may not have access.

## Assignment Rejected

The selected Agent may be inactive or at configured capacity.

## Invalid SLA Configuration

Verify that the entered SLA values satisfy backend validation.

## Backend Unavailable

If pages fail to load, verify that FastAPI is running at:

```text
http://127.0.0.1:8000
```

## Frontend Unavailable

Verify that Vite is running at:

```text
http://127.0.0.1:5173
```

---

# 52. Logging Out

Use the Logout button in the application navigation.

Logout:

- Clears the authenticated frontend session.
- Disconnects the user's active WebSocket connection.
- Returns the user to the login flow.

Always log out when using shared environments.

---

# 53. E2E Demo Accounts

The automated E2E environment uses deterministic accounts such as:

```text
Requester
requester.e2e@example.com

Agent
agent.e2e@example.com

Secondary Agent
agent2.e2e@example.com

Administrator
admin.e2e@example.com
```

These accounts belong to the E2E environment.

Do not reuse test credentials as production credentials.

---

# 54. Recommended Manual Demo

A complete manual demonstration can follow this sequence.

## Requester

```text
Login
  ↓
Create CRITICAL ticket
  ↓
Open Ticket Details
  ↓
Show SLA information
```

## Admin

```text
Login
  ↓
All Tickets
  ↓
Open new ticket
  ↓
Assign Agent
```

## Agent

Keep the Agent browser open before Admin assignment to demonstrate live notification behavior.

```text
Receive assignment notification
        ↓
Open ticket
        ↓
Start Work
        ↓
Send public response
        ↓
Add internal note
```

## Requester

Open the ticket again.

Verify:

```text
Public response visible
Internal note hidden
```

## Agent

```text
Resolve Ticket
```

Enter a resolution summary.

## Requester

```text
View Resolution Summary
        ↓
Close Ticket
```

## Admin

Finish by showing:

```text
Dashboard
User Management
SLA Settings
Application Configuration
Reports
```

---

# 55. Recommended Engineering Verification Demo

After demonstrating the application, show automated verification.

Backend:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest -v
```

Expected:

```text
98 passed
```

Frontend browser suite:

```powershell
cd frontend
npx playwright test
```

Expected:

```text
24 passed
```

Also show the successful GitHub Actions workflow.

---

# 56. User Guide Summary

The normal SupportFlow operational workflow is:

```text
Requester raises issue
        ↓
Admin assigns Agent
        ↓
Agent starts work
        ↓
Requester / Agent communicate
        ↓
SLA continuously monitored
        ↓
Ticket resolved on time
        │
        └──────────────┐
                       │
                  OR SLA breached
                       │
                       ▼
                   ESCALATED
                       ↓
            Optional auto-reassignment
                       ↓
                  Agent resolves
                       ↓
                Requester closes
```

Each role has a clearly defined responsibility, while backend authorization, audit history, SLA rules, notifications, and automated tests protect the integrity of the workflow.
