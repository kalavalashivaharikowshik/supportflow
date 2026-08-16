import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  AlertTriangle,
  CheckCircle2,
  CircleDot,
  Clock3,
  Plus,
  Tickets,
} from "lucide-react";

import {
  Link,
} from "react-router";

import Button from "../../components/common/Button";
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
  getRequesterDashboard,
} from "../../services/dashboardService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function RequesterDashboard() {
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
          await getRequesterDashboard();

        setData(result);
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load dashboard."
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
        label="Loading dashboard..."
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
        title="Requester Dashboard"
        description="Track your support requests and SLA activity."
        action={
          <Link
            to={
              ROUTES.CREATE_TICKET
            }
          >
            <Button>
              <Plus
                className="
                  mr-2 h-4 w-4
                "
              />
              Create ticket
            </Button>
          </Link>
        }
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
          title="Active"
          value={
            data.active_tickets
          }
          icon={CircleDot}
        />

        <MetricCard
          title="Resolved"
          value={
            data.resolved_tickets
          }
          icon={CheckCircle2}
        />

        <MetricCard
          title="SLA Breached"
          value={
            data.escalated_tickets
          }
          icon={AlertTriangle}
        />

        <MetricCard
          title="Open"
          value={
            data.open_tickets
          }
          icon={Clock3}
        />

        <MetricCard
          title="Closed"
          value={
            data.closed_tickets
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
      </div>

      <section
        className="space-y-4"
      >
        <div
          className="
            flex items-center
            justify-between
          "
        >
          <div>
            <h2
              className="
                text-lg font-semibold
                text-slate-900
              "
            >
              Recent tickets
            </h2>

            <p
              className="
                text-sm
                text-slate-500
              "
            >
              Your most recently
              created support requests.
            </p>
          </div>

          <Link
            to={
              ROUTES.REQUESTER_TICKETS
            }
            className="
              text-sm font-semibold
              text-slate-700
              hover:text-slate-950
            "
          >
            View all
          </Link>
        </div>

        {data.recent_tickets
          .length === 0 ? (
          <EmptyState
            title="No tickets yet"
            description="Create your first support ticket to get started."
          />
        ) : (
          <TicketTable
            tickets={
              data.recent_tickets
            }
          />
        )}
      </section>
    </div>
  );
}


export default RequesterDashboard;