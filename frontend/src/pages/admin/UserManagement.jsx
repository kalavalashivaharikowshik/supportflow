import {
  useCallback,
  useEffect,
  useState,
} from "react";

import toast from "react-hot-toast";

import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import EmptyState from "../../components/common/EmptyState";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";
import Pagination from "../../components/common/Pagination";
import SearchInput from "../../components/common/SearchInput";
import Select from "../../components/common/Select";
import ConfirmDialog from "../../components/common/ConfirmDialog";

import useDebounce from "../../hooks/useDebounce";

import {
  getUsers,
  updateUserStatus,
} from "../../services/userService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function UserManagement() {
  const [users, setUsers] =
    useState([]);

  const [page, setPage] =
    useState(1);

  const [
    totalPages,
    setTotalPages,
  ] = useState(0);

  const [search, setSearch] =
    useState("");

  const [role, setRole] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [
    pendingUser,
    setPendingUser,
  ] = useState(null);

  const [
    actionUserId,
    setActionUserId,
  ] = useState(null);

  const [error, setError] =
    useState("");


  const debouncedSearch =
    useDebounce(
      search,
      400
    );


  const loadUsers =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const params = {
          page,
          page_size: 10,
        };

        if (
          debouncedSearch.trim()
        ) {
          params.search =
            debouncedSearch.trim();
        }

        if (role) {
          params.role =
            role;
        }

        const result =
          await getUsers(
            params
          );

        setUsers(
          result.items
        );

        setTotalPages(
          result.total_pages
        );
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load users."
          )
        );
      } finally {
        setLoading(false);
      }
    }, [
      page,
      debouncedSearch,
      role,
    ]);


  useEffect(() => {
    loadUsers();
  }, [loadUsers]);


  useEffect(() => {
    setPage(1);
  }, [
    debouncedSearch,
    role,
  ]);


  const toggleUserStatus =
    async (user) => {
        const targetStatus =
        !user.is_active;

        setActionUserId(
        user.id
        );

        try {
        await updateUserStatus(
            user.id,
            targetStatus
        );

        toast.success(
            targetStatus
            ? "User activated."
            : "User deactivated."
        );

        await loadUsers();
        return true;
        } catch (apiError) {
        toast.error(
            getApiErrorMessage(
            apiError,
            "Unable to update user."
            )
        );

        return false;
        } finally {
        setActionUserId(
            null
        );
        }
    };


  return (
    <div className="space-y-6">
      <PageHeader
        title="User Management"
        description="Manage requester and Agent account access."
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
            placeholder="Search by name or email..."
          />
        </div>

        <Select
          value={role}
          onChange={
            (event) =>
              setRole(
                event.target.value
              )
          }
          options={[
            {
              value:
                "REQUESTER",
              label:
                "Requester",
            },
            {
              value:
                "AGENT",
              label:
                "Agent",
            },
            {
              value:
                "ADMIN",
              label:
                "Admin",
            },
          ]}
          placeholder="All roles"
        />
      </div>

      {
        loading
          ? (
            <LoadingSpinner
              label="Loading users..."
            />
          )
          : error
            ? (
              <ErrorState
                message={error}
                onRetry={loadUsers}
              />
            )
            : users.length === 0
              ? (
                <EmptyState
                  title="No users found"
                />
              )
              : (
                <>
                  <div
                    className="
                      overflow-hidden
                      rounded-xl border
                      border-slate-200
                      bg-white
                      shadow-sm
                    "
                  >
                    <div
                      className="
                        overflow-x-auto
                      "
                    >
                      <table
                        className="
                          min-w-full
                          divide-y
                          divide-slate-200
                        "
                      >
                        <thead
                          className="
                            bg-slate-50
                          "
                        >
                          <tr>
                            <th
                              className="
                                px-4 py-3
                                text-left
                                text-xs
                                font-semibold
                                uppercase
                                text-slate-500
                              "
                            >
                              User
                            </th>

                            <th
                              className="
                                px-4 py-3
                                text-left
                                text-xs
                                font-semibold
                                uppercase
                                text-slate-500
                              "
                            >
                              Role
                            </th>

                            <th
                              className="
                                px-4 py-3
                                text-left
                                text-xs
                                font-semibold
                                uppercase
                                text-slate-500
                              "
                            >
                              Status
                            </th>

                            <th
                              className="
                                px-4 py-3
                                text-right
                                text-xs
                                font-semibold
                                uppercase
                                text-slate-500
                              "
                            >
                              Action
                            </th>
                          </tr>
                        </thead>

                        <tbody
                          className="
                            divide-y
                            divide-slate-100
                          "
                        >
                          {users.map(
                            (user) => (
                              <tr
                                key={
                                  user.id
                                }
                              >
                                <td
                                  className="
                                    px-4 py-4
                                  "
                                >
                                  <p
                                    className="
                                      font-semibold
                                      text-slate-900
                                    "
                                  >
                                    {
                                      user.full_name
                                    }
                                  </p>

                                  <p
                                    className="
                                      mt-1
                                      text-sm
                                      text-slate-500
                                    "
                                  >
                                    {
                                      user.email
                                    }
                                  </p>
                                </td>

                                <td
                                  className="
                                    px-4 py-4
                                  "
                                >
                                  <Badge>
                                    {
                                      user.role
                                    }
                                  </Badge>
                                </td>

                                <td
                                  className="
                                    px-4 py-4
                                  "
                                >
                                  <Badge
                                    variant={
                                      user.is_active
                                        ? "success"
                                        : "danger"
                                    }
                                  >
                                    {
                                      user.is_active
                                        ? "Active"
                                        : "Inactive"
                                    }
                                  </Badge>
                                </td>

                                <td
                                  className="
                                    px-4 py-4
                                    text-right
                                  "
                                >
                                  <Button
                                    variant={
                                        user.is_active
                                        ? "danger"
                                        : "secondary"
                                    }
                                    loading={
                                        actionUserId ===
                                        user.id
                                    }
                                    onClick={
                                        () =>
                                        setPendingUser(
                                            user
                                        )
                                    }
                                    >
                                    {
                                        user.is_active
                                        ? "Deactivate"
                                        : "Activate"
                                    }
                                    </Button>
                                </td>
                              </tr>
                            )
                          )}
                        </tbody>
                      </table>
                    </div>
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
              )
      }

      <ConfirmDialog
        open={
          Boolean(
            pendingUser
          )
        }
        title={
          pendingUser?.is_active
            ? "Deactivate user?"
            : "Activate user?"
        }
        message={
          pendingUser?.is_active
            ? "This user will no longer be able to access protected SupportFlow features."
            : "This user will regain access to SupportFlow."
        }
        confirmLabel={
          pendingUser?.is_active
            ? "Deactivate"
            : "Activate"
        }
        variant={
          pendingUser?.is_active
            ? "danger"
            : "primary"
        }
        loading={
          actionUserId ===
          pendingUser?.id
        }
        onCancel={
          () =>
            setPendingUser(
              null
            )
        }
        onConfirm={
          async () => {
            if (
              !pendingUser
            ) {
              return;
            }

            await toggleUserStatus(
              pendingUser
            );

            setPendingUser(
              null
            );
          }
        }
      />
    </div>
  );
}


export default UserManagement;