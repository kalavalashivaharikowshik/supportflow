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
  getAllTickets,
} from "../../services/ticketService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


const STATUS_OPTIONS =
  Object.values(
    TICKET_STATUS
  ).map(
    (status) => ({
      value: status,
      label:
        status.replaceAll(
          "_",
          " "
        ),
    })
  );


const ASSIGNMENT_OPTIONS = [
  {
    value: "all",
    label: "All assignment states",
  },
  {
    value: "assigned",
    label: "Assigned",
  },
  {
    value: "unassigned",
    label: "Unassigned",
  },
];


const SLA_OPTIONS = [
  {
    value: "all",
    label: "All SLA states",
  },
  {
    value: "at_risk",
    label: "At Risk",
  },
  {
    value: "breached",
    label: "Breached",
  },
];


function AllTickets() {
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

  const [
    assignment,
    setAssignment,
  ] = useState("all");

  const [
    slaState,
    setSlaState,
  ] = useState("all");

  const [sortBy, setSortBy] =
    useState("created_at");

  const [
    sortDirection,
    setSortDirection,
  ] = useState("desc");

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

        if (
          assignment ===
          "assigned"
        ) {
          params.is_assigned =
            true;
        }

        if (
          assignment ===
          "unassigned"
        ) {
          params.is_assigned =
            false;
        }

        if (
          slaState ===
          "at_risk"
        ) {
          params.is_at_risk =
            true;
        }

        if (
          slaState ===
          "breached"
        ) {
          params.is_sla_breached =
            true;
        }

        const result =
          await getAllTickets(
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
            "Unable to load tickets."
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
      assignment,
      slaState,
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
    assignment,
    slaState,
    sortBy,
    sortDirection,
  ]);


  return (
    <div className="space-y-6">
      <PageHeader
        title="All Tickets"
        description="Monitor and manage the complete SupportFlow ticket queue."
      />

      <div
        className="
          grid gap-3
          rounded-xl border
          border-slate-200
          bg-white p-4
          md:grid-cols-2
          xl:grid-cols-4
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
            placeholder="Search ticket, requester name, or email..."
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
          value={assignment}
          onChange={
            (event) =>
              setAssignment(
                event.target.value
              )
          }
          options={
            ASSIGNMENT_OPTIONS
          }
        />

        <Select
          value={slaState}
          onChange={
            (event) =>
              setSlaState(
                event.target.value
              )
          }
          options={
            SLA_OPTIONS
          }
        />

        <Select
          value={sortBy}
          onChange={
            (event) =>
              setSortBy(
                event.target.value
              )
          }
          options={[
            {
              value:
                "created_at",
              label:
                "Created date",
            },
            {
              value:
                "sla_deadline",
              label:
                "SLA deadline",
            },
            {
              value:
                "priority",
              label:
                "Priority",
            },
            {
              value:
                "status",
              label:
                "Status",
            },
          ]}
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
              value: "desc",
              label: "Descending",
            },
            {
              value: "asc",
              label: "Ascending",
            },
          ]}
        />
      </div>

      {
        loading
          ? (
            <LoadingSpinner
              label="Loading tickets..."
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
                  title="No matching tickets"
                  description="Try changing the current filters."
                />
              )
              : (
                <>
                  <TicketTable
                    tickets={
                      tickets
                    }
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


export default AllTickets;