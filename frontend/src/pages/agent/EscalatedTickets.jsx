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

import useDebounce from "../../hooks/useDebounce";

import {
  getAssignedTickets,
} from "../../services/ticketService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function EscalatedTickets() {
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
          status: "ESCALATED",
          sort_by: "sla_deadline",
          sort_direction: "asc",
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
            "Unable to load escalated tickets."
          )
        );
      } finally {
        setLoading(false);
      }
    }, [
      page,
      debouncedSearch,
      priority,
    ]);


  useEffect(() => {
    loadTickets();
  }, [loadTickets]);


  useEffect(() => {
    setPage(1);
  }, [
    debouncedSearch,
    priority,
  ]);


  return (
    <div className="space-y-6">
      <PageHeader
        title="Escalated Tickets"
        description="Prioritize tickets that have breached their SLA."
      />

      <div
        className="
          grid gap-3
          rounded-xl border
          border-slate-200
          bg-white p-4
          md:grid-cols-3
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
            placeholder="Search escalated tickets..."
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
      </div>

      {
        loading
          ? (
            <LoadingSpinner
              label="Loading escalated tickets..."
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
                  title="No escalated tickets"
                  description="You currently have no assigned tickets that have breached SLA."
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


export default EscalatedTickets;