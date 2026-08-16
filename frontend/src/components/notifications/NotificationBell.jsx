import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  Bell,
  CheckCheck,
} from "lucide-react";

import {
  Link,
} from "react-router";

import toast from "react-hot-toast";

import {
  ROUTES,
} from "../../constants/routes";

import useNotifications from "../../hooks/useNotifications";

import NotificationItem from "./NotificationItem";


function NotificationBell() {
  const [open, setOpen] =
    useState(false);

  const [
    markingAll,
    setMarkingAll,
  ] = useState(false);

  const containerRef =
    useRef(null);

  const {
    unreadCount,
    recentNotifications,
    loading,
    connected,
    markRead,
    markAllRead,
  } = useNotifications();


  useEffect(() => {
    const handleClickOutside =
      (event) => {
        if (
          containerRef.current &&
          !containerRef.current.contains(
            event.target
          )
        ) {
          setOpen(false);
        }
      };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };
  }, []);


  useEffect(() => {
    if (!open) {
      return undefined;
    }

    const handleEscape =
      (event) => {
        if (
          event.key ===
          "Escape"
        ) {
          setOpen(false);
        }
      };

    document.addEventListener(
      "keydown",
      handleEscape
    );

    return () => {
      document.removeEventListener(
        "keydown",
        handleEscape
      );
    };
  }, [open]);


  const handleMarkAll =
    async () => {
      if (markingAll) {
        return;
      }

      setMarkingAll(true);

      try {
        await markAllRead();
      } catch {
        toast.error(
          "Unable to mark notifications as read."
        );
      } finally {
        setMarkingAll(false);
      }
    };


  return (
    <div
      ref={containerRef}
      className="relative"
    >
      <button
        type="button"
        onClick={
          () =>
            setOpen(
              (current) =>
                !current
            )
        }
        className="
          relative inline-flex
          h-10 w-10
          items-center
          justify-center
          rounded-lg
          text-slate-600
          transition
          hover:bg-slate-100
          hover:text-slate-900
          focus-visible:outline-none
          focus-visible:ring-2
          focus-visible:ring-slate-400
          focus-visible:ring-offset-2
        "
        aria-label={
          unreadCount > 0
            ? `Notifications, ${unreadCount} unread`
            : "Notifications"
        }
        aria-expanded={open}
        aria-haspopup="true"
      >
        <Bell
          className="h-5 w-5"
        />

        {unreadCount > 0 && (
          <span
            className="
              absolute -right-1
              -top-1 inline-flex
              min-h-5 min-w-5
              items-center
              justify-center
              rounded-full
              bg-red-600 px-1
              text-[10px]
              font-bold text-white
            "
          >
            {
              unreadCount > 99
                ? "99+"
                : unreadCount
            }
          </span>
        )}

        <span
          className={`
            absolute bottom-1
            right-1 h-2 w-2
            rounded-full
            ${
              connected
                ? "bg-emerald-500"
                : "bg-slate-300"
            }
          `}
          aria-hidden="true"
        />
      </button>

      {open && (
        <div
          className="
            absolute right-0
            z-50 mt-2
            w-[calc(100vw-2rem)]
            rounded-xl border
            border-slate-200
            bg-white p-3
            shadow-xl
            sm:w-[22rem]
          "
        >
          <div
            className="
              flex items-center
              justify-between
              gap-3 px-1 pb-3
            "
          >
            <div>
              <h3
                className="
                  font-semibold
                  text-slate-900
                "
              >
                Notifications
              </h3>

              <p
                className="
                  text-xs
                  text-slate-500
                "
              >
                {unreadCount}{" "}
                {unreadCount === 1
                  ? "unread notification"
                  : "unread notifications"}
              </p>
            </div>

            {unreadCount > 0 && (
              <button
                type="button"
                onClick={
                  handleMarkAll
                }
                disabled={
                  markingAll
                }
                className="
                  inline-flex
                  items-center gap-1
                  rounded-md px-2
                  py-1 text-xs
                  font-semibold
                  text-slate-600
                  transition
                  hover:bg-slate-100
                  hover:text-slate-900
                  focus-visible:outline-none
                  focus-visible:ring-2
                  focus-visible:ring-slate-400
                  disabled:cursor-not-allowed
                  disabled:opacity-60
                "
              >
                {markingAll ? (
                  <span
                    className="
                      h-3.5 w-3.5
                      animate-spin
                      rounded-full
                      border-2
                      border-current
                      border-t-transparent
                    "
                    aria-hidden="true"
                  />
                ) : (
                  <CheckCheck
                    className="h-4 w-4"
                  />
                )}

                {markingAll
                  ? "Updating..."
                  : "Read all"}
              </button>
            )}
          </div>

          <div
            className="
              max-h-96
              space-y-2
              overflow-y-auto
            "
          >
            {loading ? (
              <p
                className="
                  px-2 py-6
                  text-center
                  text-sm
                  text-slate-500
                "
                role="status"
              >
                Loading...
              </p>
            ) : recentNotifications
                .length === 0 ? (
              <p
                className="
                  px-2 py-6
                  text-center
                  text-sm
                  text-slate-500
                "
              >
                No notifications yet.
              </p>
            ) : (
              recentNotifications.map(
                (notification) => (
                  <div
                    key={
                      notification.id
                    }
                    onClick={
                      () =>
                        setOpen(
                          false
                        )
                    }
                  >
                    <NotificationItem
                      notification={
                        notification
                      }
                      onRead={
                        markRead
                      }
                      compact
                    />
                  </div>
                )
              )
            )}
          </div>

          <div
            className="
              mt-3 border-t
              border-slate-200
              pt-3 text-center
            "
          >
            <Link
              to={
                ROUTES.NOTIFICATIONS
              }
              onClick={
                () =>
                  setOpen(false)
              }
              className="
                inline-flex
                rounded-md px-2
                py-1 text-sm
                font-semibold
                text-slate-700
                transition
                hover:bg-slate-100
                hover:text-slate-950
                focus-visible:outline-none
                focus-visible:ring-2
                focus-visible:ring-slate-400
              "
            >
              View all notifications
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}


export default NotificationBell;