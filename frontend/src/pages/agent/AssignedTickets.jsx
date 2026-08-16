import {
  useCallback,
  useEffect,
  useState,
} from "react";

import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";
import Pagination from "../../components/common/Pagination";
import SearchInput from "../../components/common/SearchInput";
import Select from "../../components/common/Select";

import TicketTable from "../../components/tickets/TicketTable";

import {
  PRIORITY_OPTIONS,
} from "../../constants/priorities";

import {
  TICKET_STATUS,
} from "../../constants/ticketStatus";

import useDebounce from "../../hooks/useDebounce";

import {
  getAssignedTickets,
} from "../../services/ticketService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


const STATUS_OPTIONS = [
  TICKET_STATUS.ASSIGNED,
  TICKET_STATUS.IN_PROGRESS,
  TICKET_STATUS.ESCALATED,
  TICKET_STATUS.REOPENED,
  TICKET_STATUS.RESOLVED,
  TICKET_STATUS.CLOSED,
].map(
  (status) => ({
    value: status,
    label:
      status.replaceAll(
        "_",
        " "
      ),
  })
);


const SORT_OPTIONS = [
  {
    value: "sla_deadline",
    label: "SLA deadline",
  },
  {
    value: "priority",
    label: "Priority",
  },
  {
    value: "created_at",
    label: "Created date",
  },
  {
    value: "status",
    label: "Status",
  },
  {
    value: "ticket_number",
    label: "Ticket number",
  },
];


function AssignedTickets() {
  const [tickets, setTickets] =
    useState([]);

  const [page, setPage] =
    useState(1);

  const [
    totalPages,
    setTotalPages,
  ] = useState(0);

  const [search, setSearch] =
    useState("");

  const [priority, setPriority] =
    useState("");

  const [status, setStatus] =
    useState("");

  const [sortBy, setSortBy] =
    useState("sla_deadline");

  const [
    sortDirection,
    setSortDirection,
  ] = useState("asc");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const debouncedSearch =
    useDebounce(
      search,
      400
    );


  const loadTickets =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const params = {
          page,
          page_size: 10,
          sort_by: sortBy,
          sort_direction:
            sortDirection,
        };

        if (
          debouncedSearch.trim()
        ) {
          params.search =
            debouncedSearch.trim();
        }

        if (priority) {
          params.priority =
            priority;
        }

        if (status) {
          params.status =
            status;
        }

        const result =
          await getAssignedTickets(
            params
          );

        setTickets(
          result.items
        );

        setTotalPages(
          result.total_pages
        );
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load assigned tickets."
          )
        );
      } finally {
        setLoading(false);
      }
    }, [
      page,
      debouncedSearch,
      priority,
      status,
      sortBy,
      sortDirection,
    ]);


  useEffect(() => {
    loadTickets();
  }, [loadTickets]);


  useEffect(() => {
    setPage(1);
  }, [
    debouncedSearch,
    priority,
    status,
    sortBy,
    sortDirection,
  ]);


  return (
    <div className="space-y-6">
      <PageHeader
        title="Assigned Tickets"
        description="Work through your assigned support queue in SLA priority order."
      />

      <div
        className="
          grid gap-3
          rounded-xl border
          border-slate-200
          bg-white p-4
          md:grid-cols-2
          xl:grid-cols-5
        "
      >
        <div
          className="
            md:col-span-2
          "
        >
          <SearchInput
            value={search}
            onChange={setSearch}
            placeholder="Search ticket number or title..."
          />
        </div>

        <Select
          value={priority}
          onChange={
            (event) =>
              setPriority(
                event.target.value
              )
          }
          options={
            PRIORITY_OPTIONS
          }
          placeholder="All priorities"
        />

        <Select
          value={status}
          onChange={
            (event) =>
              setStatus(
                event.target.value
              )
          }
          options={
            STATUS_OPTIONS
          }
          placeholder="All statuses"
        />

        <Select
          value={sortBy}
          onChange={
            (event) =>
              setSortBy(
                event.target.value
              )
          }
          options={
            SORT_OPTIONS
          }
          placeholder="Sort by"
        />

        <Select
          value={
            sortDirection
          }
          onChange={
            (event) =>
              setSortDirection(
                event.target.value
              )
          }
          options={[
            {
              value: "asc",
              label: "Ascending",
            },
            {
              value: "desc",
              label: "Descending",
            },
          ]}
        />
      </div>

      {
        loading
          ? (
            <LoadingSpinner
              label="Loading assigned tickets..."
            />
          )
          : error
            ? (
              <ErrorState
                message={error}
                onRetry={loadTickets}
              />
            )
            : tickets.length === 0
              ? (
                <EmptyState
                  title="No assigned tickets"
                  description="No tickets match the current filters."
                />
              )
              : (
                <>
                  <TicketTable
                    tickets={tickets}
                  />

                  <Pagination
                    page={page}
                    totalPages={
                      totalPages
                    }
                    onPageChange={
                      setPage
                    }
                  />
                </>
              )
      }
    </div>
  );
}


export default AssignedTickets;