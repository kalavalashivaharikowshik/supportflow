/* eslint-disable react-refresh/only-export-components */

import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import toast from "react-hot-toast";

import {
  getNotifications,
  getUnreadCount,
  markAllNotificationsRead,
  markNotificationRead,
} from "../services/notificationService";

import useAuth from "../hooks/useAuth";
import useWebSocket from "../hooks/useWebSocket";


export const NotificationContext =
  createContext(null);


export function NotificationProvider({
  children,
}) {
  const {
    isAuthenticated,
  } = useAuth();

  const [
    unreadCount,
    setUnreadCount,
  ] = useState(0);

  const [
    recentNotifications,
    setRecentNotifications,
  ] = useState([]);

  const [loading, setLoading] =
    useState(false);


  /*
   * Prevents a notification from being
   * counted twice if the same WebSocket
   * message is received more than once.
   */
  const seenNotificationIdsRef =
    useRef(new Set());


  /*
   * Used so the initial WebSocket connection
   * does not immediately duplicate the REST
   * loading already performed after login.
   *
   * Later reconnects will refresh REST state
   * so missed notifications are recovered.
   */
  const hasConnectedOnceRef =
    useRef(false);


  const loadUnreadCount =
    useCallback(async () => {
      if (!isAuthenticated) {
        setUnreadCount(0);
        return;
      }

      try {
        const result =
          await getUnreadCount();

        setUnreadCount(
          result.unread_count ??
          result.count ??
          0
        );
      } catch {
        /*
         * Notification-count failure must not
         * break the authenticated application.
         */
      }
    }, [isAuthenticated]);


  const loadRecentNotifications =
    useCallback(async () => {
      if (!isAuthenticated) {
        setRecentNotifications(
          []
        );

        return;
      }

      setLoading(true);

      try {
        const result =
          await getNotifications({
            page: 1,
            page_size: 5,
          });

        const items =
          result.items ?? [];

        setRecentNotifications(
          items
        );

        items.forEach(
          (notification) => {
            if (
              notification.id !==
              undefined &&
              notification.id !==
              null
            ) {
              seenNotificationIdsRef
                .current
                .add(
                  notification.id
                );
            }
          }
        );
      } catch {
        setRecentNotifications(
          []
        );
      } finally {
        setLoading(false);
      }
    }, [isAuthenticated]);


  const handleWebSocketMessage =
    useCallback(
      (message) => {
        if (
          message.type ===
          "CONNECTED"
        ) {
          return;
        }

        if (
          message.type ===
          "PONG"
        ) {
          return;
        }

        if (
          message.type !==
          "NOTIFICATION"
        ) {
          return;
        }

        const notification =
          message.data;

        if (!notification) {
          return;
        }

        const notificationId =
          notification.id;

        if (
          notificationId !==
            undefined &&
          notificationId !==
            null &&
          seenNotificationIdsRef
            .current
            .has(
              notificationId
            )
        ) {
          return;
        }

        if (
          notificationId !==
            undefined &&
          notificationId !==
            null
        ) {
          seenNotificationIdsRef
            .current
            .add(
              notificationId
            );
        }

        setUnreadCount(
          (current) =>
            current + 1
        );

        setRecentNotifications(
          (current) => {
            const withoutDuplicate =
              current.filter(
                (item) =>
                  item.id !==
                  notificationId
              );

            return [
              notification,
              ...withoutDuplicate,
            ].slice(0, 5);
          }
        );

        const toastMessage =
          notification.message
            ? (
                notification.title
                  ? `${notification.title}: ${notification.message}`
                  : notification.message
              )
            : (
                notification.title ??
                "New notification"
              );

        toast(
          toastMessage
        );
      },
      []
    );


  const {
    connected,
  } = useWebSocket({
    enabled:
      isAuthenticated,

    onMessage:
      handleWebSocketMessage,
  });


  /*
   * Initial REST loading after login.
   */
  useEffect(() => {
    if (!isAuthenticated) {
      setUnreadCount(0);

      setRecentNotifications(
        []
      );

      seenNotificationIdsRef
        .current
        .clear();

      hasConnectedOnceRef.current =
        false;

      return;
    }

    loadUnreadCount();

    loadRecentNotifications();
  }, [
    isAuthenticated,
    loadUnreadCount,
    loadRecentNotifications,
  ]);


  /*
   * Do not duplicate REST requests when the
   * WebSocket first connects.
   *
   * On later reconnects, refresh persistent
   * notification state in case events were
   * missed while disconnected.
   */
  useEffect(() => {
    if (
      !isAuthenticated ||
      !connected
    ) {
      return;
    }

    if (
      !hasConnectedOnceRef.current
    ) {
      hasConnectedOnceRef.current =
        true;

      return;
    }

    loadUnreadCount();

    loadRecentNotifications();
  }, [
    connected,
    isAuthenticated,
    loadUnreadCount,
    loadRecentNotifications,
  ]);


  const markRead =
    useCallback(
      async (
        notificationId
      ) => {
        const notification =
          recentNotifications.find(
            (item) =>
              item.id ===
              notificationId
          );

        await markNotificationRead(
          notificationId
        );

        setRecentNotifications(
          (current) =>
            current.map(
              (item) =>
                item.id ===
                notificationId
                  ? {
                      ...item,
                      is_read: true,
                    }
                  : item
            )
        );

        if (
          notification &&
          !notification.is_read
        ) {
          setUnreadCount(
            (current) =>
              Math.max(
                0,
                current - 1
              )
          );
        } else {
          /*
           * Notification might have been opened
           * from the full Notifications page and
           * therefore may not exist in the recent
           * five-item preview.
           */
          await loadUnreadCount();
        }
      },
      [
        recentNotifications,
        loadUnreadCount,
      ]
    );


  const markAllRead =
    useCallback(async () => {
      await markAllNotificationsRead();

      setUnreadCount(0);

      setRecentNotifications(
        (current) =>
          current.map(
            (notification) => ({
              ...notification,
              is_read: true,
            })
          )
      );
    }, []);


  const refreshNotifications =
    useCallback(async () => {
      await Promise.all([
        loadUnreadCount(),
        loadRecentNotifications(),
      ]);
    }, [
      loadUnreadCount,
      loadRecentNotifications,
    ]);


  const value =
    useMemo(
      () => ({
        unreadCount,
        recentNotifications,
        loading,
        connected,
        markRead,
        markAllRead,
        refreshNotifications,
      }),
      [
        unreadCount,
        recentNotifications,
        loading,
        connected,
        markRead,
        markAllRead,
        refreshNotifications,
      ]
    );


  return (
    <NotificationContext.Provider
      value={value}
    >
      {children}
    </NotificationContext.Provider>
  );
}