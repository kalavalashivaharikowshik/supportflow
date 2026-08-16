import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  ROLES,
} from "../../constants/roles";

import {
  useParams,
} from "react-router";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import Select from "../../components/common/Select";

import AuditTimeline from "../../components/audit/AuditTimeline";
import ConfirmDialog from "../../components/common/ConfirmDialog";

import PriorityBadge from "../../components/tickets/PriorityBadge";
import SlaStatusCard from "../../components/tickets/SlaStatusCard";
import TicketConversation from "../../components/tickets/TicketConversation";
import TicketStatusBadge from "../../components/tickets/TicketStatusBadge";

import {
  TICKET_STATUS,
} from "../../constants/ticketStatus";
import {
  PRIORITY_OPTIONS,
} from "../../constants/priorities";

import useAuth from "../../hooks/useAuth";
import {
  getUsers,
} from "../../services/userService";

import {
  addTicketResponse,
  assignTicket,
  closeTicket,
  getTicketAudit,
  getTicketById,
  getTicketResponses,
  reassignTicket,
  reopenTicket,
  resolveTicket,
  startTicketWork,
  updateTicketPriority,
} from "../../services/ticketService";

import {
  getTicketSlaStatus,
} from "../../services/slaService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";

import {
  formatDateTime,
} from "../../utils/dateTime";


function TicketDetails() {
  const {
    ticketId,
  } = useParams();

  const {
    user,
  } = useAuth();

  const isRequester =
    user?.role ===
    ROLES.REQUESTER;

  const isAgent =
    user?.role ===
    ROLES.AGENT;

  const isAdmin =
    user?.role ===
    ROLES.ADMIN;

  const [ticket, setTicket] =
    useState(null);

  const [sla, setSla] =
    useState(null);

  const [
    responses,
    setResponses,
  ] = useState([]);

  const [audit, setAudit] =
    useState([]);

  const [reply, setReply] =
    useState("");

  const [
    confirmation,
    setConfirmation,
  ] = useState(null);

  const [
    isInternalNote,
    setIsInternalNote,
  ] = useState(false);

  const [
    resolutionSummary,
    setResolutionSummary,
  ] = useState("");

  const [agents, setAgents] =
    useState([]);

  const [
    selectedAgentId,
    setSelectedAgentId,
  ] = useState("");

  const [
    selectedPriority,
    setSelectedPriority,
  ] = useState("");

  const [loading, setLoading] =
    useState(true);

  const [
    actionLoading,
    setActionLoading,
  ] = useState(false);

  const [error, setError] =
    useState("");


  const loadTicket =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const [
          ticketResult,
          slaResult,
          responseResult,
          auditResult,
        ] = await Promise.all([
          getTicketById(
            ticketId
          ),

          getTicketSlaStatus(
            ticketId
          ),

          getTicketResponses(
            ticketId
          ),

          getTicketAudit(
            ticketId
          ),
        ]);

        setTicket(
          ticketResult
        );

        setSla(
          slaResult
        );

        setResponses(
          responseResult.items ??
          responseResult
        );

        setAudit(
          auditResult.items ??
          auditResult ??
          []
        );
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load ticket."
          )
        );
      } finally {
        setLoading(false);
      }
    }, [ticketId]);


  useEffect(() => {
    loadTicket();
  }, [loadTicket]);

  const loadAgents =
    useCallback(async () => {
        if (!isAdmin) {
        return;
        }

        try {
        const result =
            await getUsers({
            role: "AGENT",
            is_active: true,
            page: 1,
            page_size: 100,
            });

        setAgents(
            result.items ?? []
        );
        } catch {
        setAgents([]);
        }
    }, [isAdmin]);


    useEffect(() => {
    loadAgents();
    }, [loadAgents]);

    useEffect(() => {
    if (!ticket) {
        return;
    }

    setSelectedPriority(
        ticket.priority
    );

    setSelectedAgentId(
        ticket.assigned_agent_id
        ? String(
            ticket.assigned_agent_id
            )
        : ""
    );
    }, [ticket]);


  const handleReply =
    async (event) => {
      event.preventDefault();

      const message =
        reply.trim();

      if (!message) {
        toast.error(
          "Enter a response."
        );
        return;
      }

      setActionLoading(true);

      try {
        await addTicketResponse(
          ticketId,
          {
            message,
            is_internal:
              (
                isAgent ||
                isAdmin
              )
                ? isInternalNote
                : false,
          }
        );

        setReply("");
        setIsInternalNote(false);

        toast.success(
          "Response added."
        );

        await loadTicket();
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to add response."
          )
        );
      } finally {
        setActionLoading(false);
      }
    };


  const handleClose =
  async () => {
    setActionLoading(true);

    try {
      await closeTicket(
        ticketId
      );

      toast.success(
        "Ticket closed."
      );

      setConfirmation(null);

      await loadTicket();
    } catch (apiError) {
      toast.error(
        getApiErrorMessage(
          apiError,
          "Unable to close ticket."
        )
      );
    } finally {
      setActionLoading(false);
    }
  };


  const handleReopen =
  async () => {
    setActionLoading(true);

    try {
      await reopenTicket(
        ticketId
      );

      toast.success(
        "Ticket reopened."
      );

      setConfirmation(null);

      await loadTicket();
    } catch (apiError) {
      toast.error(
        getApiErrorMessage(
          apiError,
          "Unable to reopen ticket."
        )
      );
    } finally {
      setActionLoading(false);
    }
  };

    const handleStartWork =
    async () => {
        setActionLoading(true);

        try {
        await startTicketWork(
            ticketId
        );

        toast.success(
            "Work started."
        );

        await loadTicket();
        } catch (apiError) {
        toast.error(
            getApiErrorMessage(
            apiError,
            "Unable to start work."
            )
        );
        } finally {
        setActionLoading(false);
        }
    };

    const handleResolve =
  (event) => {
    event.preventDefault();

    const summary =
      resolutionSummary.trim();

    if (!summary) {
      toast.error(
        "Resolution summary is required."
      );

      return;
    }

    setConfirmation(
      "resolve"
    );
  };

  const confirmResolve =
  async () => {
    setActionLoading(true);

    try {
      await resolveTicket(
        ticketId,
        {
          resolution_summary:
            resolutionSummary.trim(),
        }
      );

      setResolutionSummary("");

      setConfirmation(null);

      toast.success(
        "Ticket resolved successfully."
      );

      await loadTicket();
    } catch (apiError) {
      toast.error(
        getApiErrorMessage(
          apiError,
          "Unable to resolve ticket."
        )
      );
    } finally {
      setActionLoading(false);
    }
  };

    const handleAssignment =
    async () => {
        if (!selectedAgentId) {
        toast.error(
            "Select an agent."
        );

        return;
        }

        setActionLoading(true);

        try {
        if (
            ticket.assigned_agent_id
        ) {
            await reassignTicket(
            ticketId,
            Number(
                selectedAgentId
            )
            );

            toast.success(
            "Ticket reassigned."
            );
        } else {
            await assignTicket(
            ticketId,
            Number(
                selectedAgentId
            )
            );

            toast.success(
            "Ticket assigned."
            );
        }

        await loadTicket();

        } catch (apiError) {
        toast.error(
            getApiErrorMessage(
            apiError,
            "Unable to update assignment."
            )
        );

        } finally {
        setActionLoading(false);
        }
    };

    const handlePriorityUpdate =
    async () => {
        if (!selectedPriority) {
        toast.error(
            "Select a priority."
        );

        return;
        }

        if (
        selectedPriority ===
        ticket.priority
        ) {
        toast.error(
            "Select a different priority."
        );

        return;
        }

        setActionLoading(true);

        try {
        await updateTicketPriority(
            ticketId,
            selectedPriority
        );

        toast.success(
            "Priority updated."
        );

        await loadTicket();

        } catch (apiError) {
        toast.error(
            getApiErrorMessage(
            apiError,
            "Unable to update priority."
            )
        );

        } finally {
        setActionLoading(false);
        }
    };


  if (loading) {
    return (
      <LoadingSpinner
        label="Loading ticket..."
      />
    );
  }


  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={
          loadTicket
        }
      />
    );
  }


  const canReply =
    ![
        TICKET_STATUS.CLOSED,
    ].includes(
        ticket.status
    );


  const canRequesterDecision =
    isRequester &&
    ticket.status ===
        TICKET_STATUS.RESOLVED;


  return (
    <div className="space-y-6">
      <div
        className="
          flex flex-col gap-4
          lg:flex-row
          lg:items-start
          lg:justify-between
        "
      >
        <div>
          <p
            className="
              text-sm font-semibold
              text-slate-500
            "
          >
            {
              ticket.ticket_number
            }
          </p>

          <h1
            className="
              mt-1 text-2xl
              font-bold
              text-slate-900
            "
          >
            {ticket.title}
          </h1>

          <div
            className="
              mt-3 flex
              flex-wrap gap-2
            "
          >
            <PriorityBadge
              priority={
                ticket.priority
              }
            />

            <TicketStatusBadge
              status={
                ticket.status
              }
            />
          </div>
        </div>

        <div
            className="
                flex flex-wrap gap-2
            "
            >
            {isAgent &&
                ticket.status ===
                TICKET_STATUS.ASSIGNED && (
                <Button
                    loading={
                    actionLoading
                    }
                    onClick={
                    handleStartWork
                    }
                >
                    Start Work
                </Button>
                )}

            {canRequesterDecision && (
                <>
                <Button
                    variant="secondary"
                    loading={
                        actionLoading
                    }
                    onClick={
                        () =>
                        setConfirmation(
                            "reopen"
                        )
                    }
                    >
                    Reopen
                    </Button>

                <Button
                    loading={
                        actionLoading
                    }
                    onClick={
                        () =>
                        setConfirmation(
                            "close"
                        )
                    }
                    >
                    Close Ticket
                    </Button>
                </>
            )}
            </div>
        </div>
      <div
        className="
          grid gap-6
          lg:grid-cols-[2fr_1fr]
        "
      >
        <div
          className="
            space-y-6
          "
        >
          <section
            className="
              rounded-xl border
              border-slate-200
              bg-white p-6
              shadow-sm
            "
          >
            <h2
              className="
                text-lg font-semibold
                text-slate-900
              "
            >
              Ticket details
            </h2>

            <p
              className="
                mt-4 whitespace-pre-wrap
                text-sm leading-6
                text-slate-700
              "
            >
              {
                ticket.description
              }
            </p>

            {ticket.resolution_summary && (
              <div
                className="
                  mt-6 rounded-lg
                  border border-emerald-200
                  bg-emerald-50 p-4
                "
              >
                <p
                  className="
                    text-xs font-semibold
                    uppercase tracking-wide
                    text-emerald-700
                  "
                >
                  Resolution Summary
                </p>

                <p
                  className="
                    mt-2 whitespace-pre-wrap
                    text-sm text-emerald-900
                  "
                >
                  {
                    ticket.resolution_summary
                  }
                </p>
              </div>
            )}

            <div
              className="
                mt-6 grid gap-4
                sm:grid-cols-2
              "
            >
              <div>
                <p
                  className="
                    text-xs font-medium
                    uppercase
                    text-slate-500
                  "
                >
                  Category
                </p>

                <p
                  className="
                    mt-1 text-sm
                    font-medium
                    text-slate-900
                  "
                >
                  {
                    ticket.category
                  }
                </p>
              </div>

              <div>
                <p
                  className="
                    text-xs font-medium
                    uppercase
                    text-slate-500
                  "
                >
                  Created
                </p>

                <p
                  className="
                    mt-1 text-sm
                    font-medium
                    text-slate-900
                  "
                >
                  {formatDateTime(
                    ticket.created_at
                  )}
                </p>
              </div>
            </div>
          </section>

          <section
            className="
              rounded-xl border
              border-slate-200
              bg-white p-6
              shadow-sm
            "
          >
            <h2
              className="
                text-lg font-semibold
                text-slate-900
              "
            >
              Conversation
            </h2>

            <div className="mt-5">
              <TicketConversation
                responses={
                  responses
                }
                currentUserId={
                  user.id
                }
              />
            </div>

            {canReply && (
              <form
                onSubmit={
                  handleReply
                }
                className="
                  mt-6
                  border-t
                  border-slate-200
                  pt-5
                "
              >
                <label
                  htmlFor="reply"
                  className="
                    text-sm
                    font-medium
                    text-slate-700
                  "
                >
                  Add response
                </label>

                <textarea
                    id="reply"
                    value={reply}
                    onChange={
                        (event) =>
                        setReply(
                            event.target.value
                        )
                    }
                    placeholder="Write a response..."
                    className="
                        mt-2 min-h-28
                        w-full rounded-lg
                        border
                        border-slate-300
                        p-3 text-sm
                        outline-none
                        focus:border-slate-500
                        focus:ring-2
                        focus:ring-slate-200
                    "
                    />

                    {(isAgent ||
                      isAdmin
                    ) && (
                    <label
                      className="
                        mt-3 flex
                        items-center gap-2
                        text-sm text-slate-700
                      "
                    >
                        <input
                        type="checkbox"
                        checked={
                            isInternalNote
                        }
                        onChange={
                            (event) =>
                            setIsInternalNote(
                                event.target.checked
                            )
                        }
                        className="
                            h-4 w-4 rounded
                            border-slate-300
                        "
                        />

                        <span>
                        Internal note
                        </span>

                        <span
                        className="
                            text-xs text-slate-500
                        "
                        >
                        Visible only to support staff
                        </span>
                    </label>
                    )}

                    <div
                    className="
                        mt-3 flex
                        justify-end
                    "
                    >
                  <Button
                    type="submit"
                    loading={
                      actionLoading
                    }
                  >
                    Send response
                  </Button>
                </div>
              </form>
            )}
          </section>

          {isAgent &&
            [
              TICKET_STATUS.IN_PROGRESS,
              TICKET_STATUS.ESCALATED,
            ].includes(
              ticket.status
            ) && (
              <section
                className="
                  rounded-xl border
                  border-slate-200
                  bg-white p-6
                  shadow-sm
                "
              >
                <h2
                  className="
                    text-lg font-semibold
                    text-slate-900
                  "
                >
                  Resolve Ticket
                </h2>

                <p
                  className="
                    mt-1 text-sm
                    text-slate-500
                  "
                >
                  Add a clear resolution summary before marking the ticket resolved.
                </p>

                <form
                  onSubmit={
                    handleResolve
                  }
                  className="mt-5"
                >
                  <textarea
                    value={
                      resolutionSummary
                    }
                    onChange={
                      (event) =>
                        setResolutionSummary(
                          event.target.value
                        )
                    }
                    placeholder="Describe the fix or resolution..."
                    className="
                      min-h-32 w-full
                      rounded-lg border
                      border-slate-300
                      p-3 text-sm
                      outline-none
                      focus:border-slate-500
                      focus:ring-2
                      focus:ring-slate-200
                    "
                  />

                  <div
                    className="
                      mt-3 flex
                      justify-end
                    "
                  >
                    <Button
                      type="submit"
                      loading={
                        actionLoading
                      }
                    >
                      Resolve Ticket
                    </Button>
                  </div>
                </form>
              </section>
            )}

          <section
            className="
              rounded-xl border
              border-slate-200
              bg-white p-6
              shadow-sm
            "
          >
            <h2
              className="
                text-lg font-semibold
                text-slate-900
              "
            >
              Activity timeline
            </h2>

            <div className="mt-5">
              <AuditTimeline
                items={audit}
              />
            </div>
          </section>
        </div>

        <aside
          className="
            space-y-5
          "
        >
          {sla && (
            <SlaStatusCard
              sla={sla}
            />
          )}

          {isAdmin && (
            <div
                className="
                rounded-xl border
                border-slate-200
                bg-white p-5
                shadow-sm
                "
            >
                <h3
                className="
                    font-semibold
                    text-slate-900
                "
                >
                Admin Actions
                </h3>

                <div
                className="
                    mt-4 space-y-5
                "
                >
                <div>
                    <Select
                    label={
                        ticket.assigned_agent_id
                        ? "Reassign Agent"
                        : "Assign Agent"
                    }
                    value={
                        selectedAgentId
                    }
                    onChange={
                        (event) =>
                        setSelectedAgentId(
                            event.target.value
                        )
                    }
                    options={
                        agents.map(
                        (agent) => ({
                            value:
                            String(
                                agent.id
                            ),
                            label:
                            `${agent.full_name} (${agent.email})`,
                        })
                        )
                    }
                    placeholder="Select Agent"
                    />

                    <Button
                    className="mt-3 w-full"
                    loading={
                        actionLoading
                    }
                    onClick={
                        handleAssignment
                    }
                    >
                    {
                        ticket.assigned_agent_id
                        ? "Reassign Ticket"
                        : "Assign Ticket"
                    }
                    </Button>
                </div>

                <div
                    className="
                    border-t
                    border-slate-200
                    pt-4
                    "
                >
                    <Select
                    label="Priority"
                    value={
                        selectedPriority
                    }
                    onChange={
                        (event) =>
                        setSelectedPriority(
                            event.target.value
                        )
                    }
                    options={
                        PRIORITY_OPTIONS
                    }
                    />

                    <Button
                    variant="secondary"
                    className="mt-3 w-full"
                    loading={
                        actionLoading
                    }
                    onClick={
                        handlePriorityUpdate
                    }
                    >
                    Update Priority
                    </Button>
                </div>
                </div>
            </div>
            )}

          <div
            className="
              rounded-xl border
              border-slate-200
              bg-white p-5
              shadow-sm
            "
          >
            <h3
              className="
                font-semibold
                text-slate-900
              "
            >
              Assignment
            </h3>

            <div
              className="
                mt-4 space-y-3
                text-sm
              "
            >
              <div>
                <p
                  className="
                    text-slate-500
                  "
                >
                  Assigned agent
                </p>

                <p
                  className="
                    mt-1 font-medium
                    text-slate-900
                  "
                >
                  {
                    ticket.assigned_agent_id
                      ? `Agent #${ticket.assigned_agent_id}`
                      : "Not assigned yet"
                  }
                </p>
              </div>

              <div>
                <p
                  className="
                    text-slate-500
                  "
                >
                  First response
                </p>

                <p
                  className="
                    mt-1 font-medium
                    text-slate-900
                  "
                >
                  {formatDateTime(
                    ticket.first_response_at
                  )}
                </p>
              </div>

              <div>
                <p
                  className="
                    text-slate-500
                  "
                >
                  Resolved
                </p>

                <p
                  className="
                    mt-1 font-medium
                    text-slate-900
                  "
                >
                  {formatDateTime(
                    ticket.resolved_at
                  )}
                </p>
              </div>
            </div>
          </div>
       </aside>
      </div>

      <ConfirmDialog
        open={
          confirmation ===
          "close"
        }
        title="Close ticket?"
        message="This will close the resolved ticket. Further replies will no longer be allowed."
        confirmLabel="Close Ticket"
        variant="primary"
        loading={
          actionLoading
        }
        onConfirm={
          handleClose
        }
        onCancel={
          () =>
            setConfirmation(
              null
            )
        }
      />

      <ConfirmDialog
        open={
          confirmation ===
          "reopen"
        }
        title="Reopen ticket?"
        message="The ticket will return to the active support workflow."
        confirmLabel="Reopen Ticket"
        variant="primary"
        loading={
          actionLoading
        }
        onConfirm={
          handleReopen
        }
        onCancel={
          () =>
            setConfirmation(
              null
            )
        }
      />

      <ConfirmDialog
        open={
          confirmation ===
          "resolve"
        }
        title="Resolve ticket?"
        message="Confirm that the resolution summary is complete and the reported issue has been addressed."
        confirmLabel="Resolve Ticket"
        variant="primary"
        loading={
          actionLoading
        }
        onConfirm={
          confirmResolve
        }
        onCancel={
          () =>
            setConfirmation(
              null
            )
        }
      />
    </div>
  );
}


export default TicketDetails;