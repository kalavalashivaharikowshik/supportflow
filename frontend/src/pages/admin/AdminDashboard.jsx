import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  Inbox,
  Tickets,
  UserRoundCheck,
  Users,
} from "lucide-react";

import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";

import AgentWorkloadTable from "../../components/dashboard/AgentWorkloadTable";
import MetricCard from "../../components/dashboard/MetricCard";

import TicketTable from "../../components/tickets/TicketTable";

import {
  getAdminDashboard,
} from "../../services/dashboardService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function AdminDashboard() {
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
          await getAdminDashboard();

        setData(result);
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load admin dashboard."
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
        label="Loading admin dashboard..."
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
        title="Admin Dashboard"
        description="Monitor SupportFlow operations, SLA risk, and team workload."
      />

      <div
        className="
          grid gap-4
          sm:grid-cols-2
          lg:grid-cols-4
        "
      >
        <MetricCard
          title="Total Tickets"
          value={
            data.total_tickets
          }
          icon={Tickets}
        />

        <MetricCard
          title="Active Tickets"
          value={
            data.active_tickets
          }
          icon={Clock3}
        />

        <MetricCard
          title="Unassigned"
          value={
            data.unassigned_tickets
          }
          icon={Inbox}
        />

        <MetricCard
          title="Escalated"
          value={
            data.escalated_tickets
          }
          icon={AlertTriangle}
        />

        <MetricCard
          title="SLA At Risk"
          value={
            data.sla_at_risk_tickets
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
          title="Requesters"
          value={
            data.total_requesters
          }
          icon={Users}
        />

        <MetricCard
          title="Active Agents"
          value={
            data.active_agents
          }
          description={
            `${data.total_agents} total agents`
          }
          icon={UserRoundCheck}
        />
      </div>

      <section
        className="space-y-4"
      >
        <h2
          className="
            text-lg font-semibold
            text-slate-900
          "
        >
          Agent workload
        </h2>

        {
          data.agent_workload
            .length === 0
            ? (
              <EmptyState
                title="No active agents"
                description="No active Agent accounts are available."
              />
            )
            : (
              <AgentWorkloadTable
                items={
                  data.agent_workload
                }
              />
            )
        }
      </section>

      <section
        className="space-y-4"
      >
        <h2
          className="
            text-lg font-semibold
            text-slate-900
          "
        >
          Recent tickets
        </h2>

        {
          data.recent_tickets
            .length === 0
            ? (
              <EmptyState
                title="No tickets"
              />
            )
            : (
              <TicketTable
                tickets={
                  data.recent_tickets
                }
              />
            )
        }
      </section>

      <section
        className="space-y-4"
      >
        <h2
          className="
            text-lg font-semibold
            text-slate-900
          "
        >
          Recent escalations
        </h2>

        {
          data.recent_escalations
            .length === 0
            ? (
              <EmptyState
                title="No escalations"
                description="No SLA breaches are currently recorded."
              />
            )
            : (
              <TicketTable
                tickets={
                  data.recent_escalations
                }
              />
            )
        }
      </section>
    </div>
  );
}


export default AdminDashboard;