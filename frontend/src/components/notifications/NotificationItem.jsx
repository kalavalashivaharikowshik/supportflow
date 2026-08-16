import {
  Link,
} from "react-router";

import {
  getTicketDetailsRoute,
} from "../../constants/routes";

import {
  formatRelativeTime,
} from "../../utils/dateTime";

import NotificationTypeBadge from "./NotificationTypeBadge";


function NotificationItem({
  notification,
  onRead,
  compact = false,
}) {
  const handleClick =
    async () => {
      if (
        !notification.is_read
      ) {
        try {
          await onRead(
            notification.id
          );
        } catch {
          /*
           * Navigation or interaction should
           * still continue even if marking
           * the notification as read fails.
           */
        }
      }
    };


  const title =
    notification.title ??
    "Notification";


  const content = (
    <div
      className={`
        rounded-lg border p-3
        transition

        ${
          notification.is_read
            ? "border-slate-200 bg-white"
            : "border-blue-200 bg-blue-50"
        }
      `}
    >
      <div
        className="
          flex items-start
          justify-between
          gap-3
        "
      >
        <div className="min-w-0">
          <NotificationTypeBadge
            type={
              notification.notification_type ??
              notification.type
            }
          />

          <p
            className="
              mt-2 text-sm
              font-semibold
              text-slate-900
            "
          >
            {title}
          </p>

          {notification.message && (
            <p
              className={`
                mt-1 text-sm
                text-slate-600

                ${
                  compact
                    ? "line-clamp-2"
                    : ""
                }
              `}
            >
              {
                notification.message
              }
            </p>
          )}

          <p
            className="
              mt-2 text-xs
              text-slate-500
            "
          >
            {formatRelativeTime(
              notification.created_at
            )}
          </p>
        </div>

        {!notification.is_read && (
          <>
            <span
              className="
                mt-1 h-2.5 w-2.5
                shrink-0 rounded-full
                bg-blue-600
              "
              aria-hidden="true"
            />

            <span className="sr-only">
              Unread notification
            </span>
          </>
        )}
      </div>
    </div>
  );


  const commonClassName = `
    block w-full
    rounded-lg
    text-left
    focus-visible:outline-none
    focus-visible:ring-2
    focus-visible:ring-slate-400
    focus-visible:ring-offset-2
  `;


  if (
    notification.ticket_id
  ) {
    return (
      <Link
        to={
          getTicketDetailsRoute(
            notification.ticket_id
          )
        }
        onClick={
          handleClick
        }
        className={
          commonClassName
        }
      >
        {content}
      </Link>
    );
  }


  return (
    <button
      type="button"
      onClick={
        handleClick
      }
      className={
        commonClassName
      }
      aria-label={
        notification.is_read
          ? title
          : `${title}, unread`
      }
    >
      {content}
    </button>
  );
}


export default NotificationItem;