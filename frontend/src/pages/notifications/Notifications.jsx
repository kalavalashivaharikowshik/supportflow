import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  CheckCheck,
} from "lucide-react";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";
import Pagination from "../../components/common/Pagination";
import Select from "../../components/common/Select";

import NotificationItem from "../../components/notifications/NotificationItem";

import useNotifications from "../../hooks/useNotifications";

import {
  getNotifications,
} from "../../services/notificationService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function Notifications() {
  const [items, setItems] =
    useState([]);

  const [page, setPage] =
    useState(1);

  const [
    totalPages,
    setTotalPages,
  ] = useState(0);

  const [readState, setReadState] =
    useState("all");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const {
    markRead,
    markAllRead,
    refreshNotifications,
  } = useNotifications();


  const loadNotifications =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const params = {
          page,
          page_size: 10,
        };

        if (
          readState ===
          "unread"
        ) {
          params.is_read =
            false;
        }

        if (
          readState ===
          "read"
        ) {
          params.is_read =
            true;
        }

        const result =
          await getNotifications(
            params
          );

        setItems(
          result.items
        );

        setTotalPages(
          result.total_pages
        );
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load notifications."
          )
        );
      } finally {
        setLoading(false);
      }
    }, [
      page,
      readState,
    ]);


  useEffect(() => {
    loadNotifications();
  }, [loadNotifications]);


  useEffect(() => {
    setPage(1);
  }, [readState]);


  const handleRead =
    async (
      notificationId
    ) => {
      try {
        await markRead(
          notificationId
        );

        setItems(
          (current) =>
            current.map(
              (notification) =>
                notification.id ===
                notificationId
                  ? {
                      ...notification,
                      is_read: true,
                    }
                  : notification
            )
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to mark notification as read."
          )
        );
      }
    };


  const handleReadAll =
    async () => {
      try {
        await markAllRead();

        await Promise.all([
          loadNotifications(),
          refreshNotifications(),
        ]);

        toast.success(
          "All notifications marked as read."
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to mark notifications as read."
          )
        );
      }
    };


  return (
    <div className="space-y-6">
      <PageHeader
        title="Notifications"
        description="Review ticket activity, assignments, SLA alerts, and workflow updates."
        action={
          <Button
            variant="secondary"
            onClick={
              handleReadAll
            }
          >
            <CheckCheck
              className="
                mr-2 h-4 w-4
              "
            />
            Mark all read
          </Button>
        }
      />

      <div
        className="
          max-w-xs
        "
      >
        <Select
          value={readState}
          onChange={
            (event) =>
              setReadState(
                event.target.value
              )
          }
          options={[
            {
              value: "all",
              label:
                "All notifications",
            },
            {
              value: "unread",
              label:
                "Unread only",
            },
            {
              value: "read",
              label:
                "Read only",
            },
          ]}
        />
      </div>

      {loading ? (
        <LoadingSpinner
          label="Loading notifications..."
        />
      ) : error ? (
        <ErrorState
          message={error}
          onRetry={
            loadNotifications
          }
        />
      ) : items.length === 0 ? (
        <EmptyState
          title="No notifications"
          description="There are no notifications matching the current filter."
        />
      ) : (
        <>
          <div className="space-y-3">
            {items.map(
              (notification) => (
                <NotificationItem
                  key={
                    notification.id
                  }
                  notification={
                    notification
                  }
                  onRead={
                    handleRead
                  }
                />
              )
            )}
          </div>

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
      )}
    </div>
  );
}


export default Notifications;