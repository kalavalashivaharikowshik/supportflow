import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  ListChecks,
  PlayCircle,
  Tickets,
} from "lucide-react";

import {
  Link,
} from "react-router";

import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";

import MetricCard from "../../components/dashboard/MetricCard";
import TicketTable from "../../components/tickets/TicketTable";

import {
  ROUTES,
} from "../../constants/routes";

import {
  getAgentDashboard,
} from "../../services/dashboardService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function AgentDashboard() {
  const [data, setData] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const loadDashboard =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const result =
          await getAgentDashboard();

        setData(result);
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load agent dashboard."
          )
        );
      } finally {
        setLoading(false);
      }
    }, []);


  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);


  if (loading) {
    return (
      <LoadingSpinner
        label="Loading agent dashboard..."
      />
    );
  }


  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={
          loadDashboard
        }
      />
    );
  }


  return (
    <div className="space-y-6">
      <PageHeader
        title="Agent Dashboard"
        description="Monitor assigned workload, SLA risk, and ticket progress."
      />

      <div
        className="
          grid gap-4
          sm:grid-cols-2
          lg:grid-cols-4
        "
      >
        <MetricCard
          title="Total Assigned"
          value={
            data.total_assigned_tickets
          }
          icon={Tickets}
        />

        <MetricCard
          title="Active"
          value={
            data.active_tickets
          }
          icon={ListChecks}
        />

        <MetricCard
          title="Assigned"
          value={
            data.assigned_tickets
          }
          icon={Clock3}
        />

        <MetricCard
          title="In Progress"
          value={
            data.in_progress_tickets
          }
          icon={PlayCircle}
        />

        <MetricCard
          title="Escalated"
          value={
            data.escalated_tickets
          }
          icon={AlertTriangle}
        />

        <MetricCard
          title="Resolved"
          value={
            data.resolved_tickets
          }
          icon={CheckCircle2}
        />

        <MetricCard
          title="SLA At Risk"
          value={
            data.sla_at_risk_tickets
          }
          icon={AlertTriangle}
        />

        <MetricCard
          title="Avg First Response"
          value={
            data.average_first_response_minutes
              === null
              ? "—"
              : `${data.average_first_response_minutes}m`
          }
          icon={Clock3}
        />
      </div>

      <div
        className="
          grid gap-4
          sm:grid-cols-2
        "
      >
        <div
          className="
            rounded-xl border
            border-slate-200
            bg-white p-5 shadow-sm
          "
        >
          <p
            className="
              text-sm font-medium
              text-slate-500
            "
          >
            Average Resolution
          </p>

          <p
            className="
              mt-2 text-3xl
              font-bold text-slate-900
            "
          >
            {
              data.average_resolution_minutes
                === null
                ? "—"
                : `${data.average_resolution_minutes}m`
            }
          </p>
        </div>
      </div>

      <section className="space-y-4">
        <div
          className="
            flex items-center
            justify-between gap-4
          "
        >
          <div>
            <h2
              className="
                text-lg font-semibold
                text-slate-900
              "
            >
              Recent assigned tickets
            </h2>

            <p
              className="
                text-sm text-slate-500
              "
            >
              Your most recently assigned support work.
            </p>
          </div>

          <Link
            to={ROUTES.AGENT_TICKETS}
            className="
              text-sm font-semibold
              text-slate-700
              hover:text-slate-950
            "
          >
            View all
          </Link>
        </div>

        {
          data.recent_tickets.length === 0
            ? (
              <EmptyState
                title="No assigned tickets"
                description="You currently have no assigned support tickets."
              />
            )
            : (
              <TicketTable
                tickets={data.recent_tickets}
              />
            )
        }
      </section>
    </div>
  );
}


export default AgentDashboard;