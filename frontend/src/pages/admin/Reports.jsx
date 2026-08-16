import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  Download,
} from "lucide-react";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import ErrorState from "../../components/common/ErrorState";
import Input from "../../components/common/Input";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";

import MetricCard from "../../components/dashboard/MetricCard";

import {
  downloadAgentReport,
  downloadSlaReport,
  downloadTicketReport,
  getAgentPerformanceReport,
  getSlaBreachReport,
  getTicketReportSummary,
} from "../../services/reportService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


const buildDateParams = (
  startDate,
  endDate
) => {
  const params = {};

  if (startDate) {
    params.start_date =
      new Date(
        `${startDate}T00:00:00`
      ).toISOString();
  }

  if (endDate) {
    params.end_date =
      new Date(
        `${endDate}T23:59:59`
      ).toISOString();
  }

  return params;
};


function Reports() {
  const [summary, setSummary] =
    useState(null);

  const [slaItems, setSlaItems] =
    useState([]);

  const [agents, setAgents] =
    useState([]);

  /*
   * Draft values:
   * what the Admin is currently selecting.
   */
  const [
    startDate,
    setStartDate,
  ] = useState("");

  const [
    endDate,
    setEndDate,
  ] = useState("");

  /*
   * Applied values:
   * the date range currently being used
   * by reports and CSV downloads.
   */
  const [
    appliedStartDate,
    setAppliedStartDate,
  ] = useState("");

  const [
    appliedEndDate,
    setAppliedEndDate,
  ] = useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const loadReports =
    useCallback(
      async (
        filterStartDate =
          appliedStartDate,
        filterEndDate =
          appliedEndDate
      ) => {
        setLoading(true);
        setError("");

        try {
          const params =
            buildDateParams(
              filterStartDate,
              filterEndDate
            );

          const [
            summaryResult,
            slaResult,
            agentResult,
          ] = await Promise.all([
            getTicketReportSummary(
              params
            ),

            getSlaBreachReport(
              params
            ),

            getAgentPerformanceReport(
              params
            ),
          ]);

          setSummary(
            summaryResult
          );

          setSlaItems(
            slaResult
          );

          setAgents(
            agentResult
          );
        } catch (apiError) {
          setError(
            getApiErrorMessage(
              apiError,
              "Unable to load reports."
            )
          );
        } finally {
          setLoading(false);
        }
      },
      [
        appliedStartDate,
        appliedEndDate,
      ]
    );


  useEffect(() => {
    loadReports();
  }, [loadReports]);


  const validateDateRange = (
    filterStartDate,
    filterEndDate
  ) => {
    if (
      filterStartDate &&
      filterEndDate &&
      filterStartDate >
        filterEndDate
    ) {
      toast.error(
        "Start date cannot be after end date."
      );

      return false;
    }

    return true;
  };


  const handleApplyFilter =
    async () => {
      if (
        !validateDateRange(
          startDate,
          endDate
        )
      ) {
        return;
      }

      setAppliedStartDate(
        startDate
      );

      setAppliedEndDate(
        endDate
      );

      await loadReports(
        startDate,
        endDate
      );
    };


  const handleClearFilter =
    async () => {
      setStartDate("");
      setEndDate("");

      setAppliedStartDate("");
      setAppliedEndDate("");

      await loadReports(
        "",
        ""
      );
    };


  const runDownload =
    async (
      downloadFunction,
      successMessage
    ) => {
      try {
        await downloadFunction();

        toast.success(
          successMessage
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to download report."
          )
        );
      }
    };


  const appliedDateParams =
    buildDateParams(
      appliedStartDate,
      appliedEndDate
    );


  if (loading) {
    return (
      <LoadingSpinner
        label="Loading reports..."
      />
    );
  }


  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={
          () =>
            loadReports()
        }
      />
    );
  }


  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Review operational performance and export report data."
      />

      <div
        className="
          rounded-xl border
          border-slate-200
          bg-white p-4
        "
      >
        <div
          className="
            grid gap-4
            sm:grid-cols-2
            lg:grid-cols-[1fr_1fr_auto_auto]
            lg:items-end
          "
        >
          <Input
            type="date"
            label="Start date"
            value={
              startDate
            }
            onChange={
              (event) =>
                setStartDate(
                  event.target.value
                )
            }
          />

          <Input
            type="date"
            label="End date"
            value={
              endDate
            }
            onChange={
              (event) =>
                setEndDate(
                  event.target.value
                )
            }
          />

          <Button
            onClick={
              handleApplyFilter
            }
            className="
              w-full
              lg:w-auto
            "
          >
            Apply Filter
          </Button>

          <Button
            variant="secondary"
            onClick={
              handleClearFilter
            }
            disabled={
              !startDate &&
              !endDate &&
              !appliedStartDate &&
              !appliedEndDate
            }
            className="
              w-full
              lg:w-auto
            "
          >
            Clear
          </Button>
        </div>

        {(
          appliedStartDate ||
          appliedEndDate
        ) && (
          <p
            className="
              mt-3 text-sm
              text-slate-500
            "
          >
            Showing reports
            {appliedStartDate
              ? ` from ${appliedStartDate}`
              : ""}
            {appliedEndDate
              ? ` through ${appliedEndDate}`
              : ""}
            .
          </p>
        )}
      </div>

      <div
        className="
          grid gap-4
          sm:grid-cols-2
          lg:grid-cols-3
        "
      >
        <MetricCard
          title="Total Tickets"
          value={
            summary.total_tickets
          }
        />

        <MetricCard
          title="Active"
          value={
            summary.active_tickets
          }
        />

        <MetricCard
          title="Resolved"
          value={
            summary.resolved_tickets
          }
        />

        <MetricCard
          title="Closed"
          value={
            summary.closed_tickets
          }
        />

        <MetricCard
          title="Escalated"
          value={
            summary.escalated_tickets
          }
        />

        <MetricCard
          title="SLA Breaches"
          value={
            summary.sla_breached_tickets
          }
        />
      </div>

      <div
        className="
          grid gap-4
          md:grid-cols-3
        "
      >
        <Button
          variant="secondary"
          onClick={
            () =>
              runDownload(
                () =>
                  downloadTicketReport(
                    appliedDateParams
                  ),
                "Ticket report downloaded."
              )
          }
        >
          <Download
            className="
              h-4 w-4
            "
          />
          Ticket CSV
        </Button>

        <Button
          variant="secondary"
          onClick={
            () =>
              runDownload(
                () =>
                  downloadSlaReport(
                    appliedDateParams
                  ),
                "SLA report downloaded."
              )
          }
        >
          <Download
            className="
              h-4 w-4
            "
          />
          SLA CSV
        </Button>

        <Button
          variant="secondary"
          onClick={
            () =>
              runDownload(
                () =>
                  downloadAgentReport(
                    appliedDateParams
                  ),
                "Agent report downloaded."
              )
          }
        >
          <Download
            className="
              h-4 w-4
            "
          />
          Agent CSV
        </Button>
      </div>

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
          SLA Breaches
        </h2>

        <p
          className="
            mt-2 text-sm
            text-slate-500
          "
        >
          Total records:{" "}
          {slaItems.length}
        </p>
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
          Agent Performance
        </h2>

        <div
          className="
            mt-5 overflow-x-auto
          "
        >
          <table
            className="
              min-w-full
              divide-y
              divide-slate-200
            "
          >
            <caption
              className="sr-only"
            >
              Agent performance report
            </caption>

            <thead>
              <tr>
                <th
                  scope="col"
                  className="
                    px-3 py-2
                    text-left
                    text-xs uppercase
                    text-slate-500
                  "
                >
                  Agent
                </th>

                <th
                  scope="col"
                  className="
                    px-3 py-2
                    text-left
                    text-xs uppercase
                    text-slate-500
                  "
                >
                  Assigned
                </th>

                <th
                  scope="col"
                  className="
                    px-3 py-2
                    text-left
                    text-xs uppercase
                    text-slate-500
                  "
                >
                  Resolved
                </th>

                <th
                  scope="col"
                  className="
                    px-3 py-2
                    text-left
                    text-xs uppercase
                    text-slate-500
                  "
                >
                  Escalated
                </th>

                <th
                  scope="col"
                  className="
                    px-3 py-2
                    text-left
                    text-xs uppercase
                    text-slate-500
                  "
                >
                  Avg Response
                </th>
              </tr>
            </thead>

            <tbody
              className="
                divide-y
                divide-slate-100
              "
            >
              {agents.map(
                (agent) => (
                  <tr
                    key={
                      agent.agent_id
                    }
                  >
                    <td
                      className="
                        px-3 py-3
                      "
                    >
                      <p
                        className="
                          font-medium
                          text-slate-900
                        "
                      >
                        {
                          agent.full_name
                        }
                      </p>

                      <p
                        className="
                          text-xs
                          text-slate-500
                        "
                      >
                        {
                          agent.email
                        }
                      </p>
                    </td>

                    <td
                      className="
                        px-3 py-3
                      "
                    >
                      {
                        agent.total_assigned
                      }
                    </td>

                    <td
                      className="
                        px-3 py-3
                      "
                    >
                      {
                        agent.resolved_tickets
                      }
                    </td>

                    <td
                      className="
                        px-3 py-3
                      "
                    >
                      {
                        agent.escalated_tickets
                      }
                    </td>

                    <td
                      className="
                        px-3 py-3
                      "
                    >
                      {
                        agent.average_first_response_minutes
                          ?? "—"
                      }
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}


export default Reports;