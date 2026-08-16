/* eslint-disable react-refresh/only-export-components */

import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  getCurrentUser,
  login as loginRequest,
  logout as logoutRequest,
} from "../services/authService";

import {
  clearAuthStorage,
  getAccessToken,
  setAccessToken,
} from "../utils/storage";


export const AuthContext =
  createContext(null);


export function AuthProvider({
  children,
}) {
  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  const clearSession =
    useCallback(() => {
      clearAuthStorage();
      setUser(null);
    }, []);


  const loadCurrentUser =
    useCallback(async () => {
      const token =
        getAccessToken();

      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        const currentUser =
          await getCurrentUser();

        setUser(currentUser);
      } catch {
        clearSession();
      } finally {
        setLoading(false);
      }
    }, [clearSession]);


  useEffect(() => {
    loadCurrentUser();
  }, [loadCurrentUser]);


  useEffect(() => {
    const handleUnauthorized =
      () => {
        clearSession();
      };

    window.addEventListener(
      "supportflow:unauthorized",
      handleUnauthorized
    );

    return () => {
      window.removeEventListener(
        "supportflow:unauthorized",
        handleUnauthorized
      );
    };
  }, [clearSession]);


  const login =
    useCallback(
      async (credentials) => {
        const result =
          await loginRequest(
            credentials
          );

        setAccessToken(
          result.access_token
        );

        const currentUser =
          result.user ??
          await getCurrentUser();

        setUser(currentUser);

        return currentUser;
      },
      []
    );


  const logout =
    useCallback(
      async () => {
        try {
          await logoutRequest();
        } catch {
          // Local logout must still succeed.
        } finally {
          clearSession();
        }
      },
      [clearSession]
    );


  const refreshUser =
    useCallback(
      async () => {
        const currentUser =
          await getCurrentUser();

        setUser(currentUser);

        return currentUser;
      },
      []
    );


  const value =
    useMemo(
      () => ({
        user,
        loading,
        isAuthenticated:
          Boolean(user),
        login,
        logout,
        refreshUser,
      }),
      [
        user,
        loading,
        login,
        logout,
        refreshUser,
      ]
    );


  return (
    <AuthContext.Provider
      value={value}
    >
      {children}
    </AuthContext.Provider>
  );
}