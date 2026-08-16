import {
  useCallback,
  useEffect,
  useState,
} from "react";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import ErrorState from "../../components/common/ErrorState";
import Input from "../../components/common/Input";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";

import {
  getAdminConfig,
  updateAdminConfig,
} from "../../services/configService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function AdminConfiguration() {
  const [config, setConfig] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");


  const loadConfig =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const result =
          await getAdminConfig();

        setConfig(result);
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load configuration."
          )
        );
      } finally {
        setLoading(false);
      }
    }, []);


  useEffect(() => {
    loadConfig();
  }, [loadConfig]);


  const updateField = (
    field,
    value
  ) => {
    setConfig(
      (current) => ({
        ...current,
        [field]: value,
      })
    );
  };


  const handleSubmit =
    async (event) => {
      event.preventDefault();

      setSaving(true);

      try {
        const result =
          await updateAdminConfig({
            sla_warning_threshold_percent:
              Number(
                config.sla_warning_threshold_percent
              ),

            escalation_check_interval_seconds:
              Number(
                config.escalation_check_interval_seconds
              ),

            max_active_tickets_per_agent:
              Number(
                config.max_active_tickets_per_agent
              ),
              
            auto_reassign_on_escalation:
              config.auto_reassign_on_escalation,

            allow_requester_reopen:
              config.allow_requester_reopen,

            allow_admin_public_response:
              config.allow_admin_public_response,

            notifications_enabled:
              config.notifications_enabled,

            websocket_notifications_enabled:
              config.websocket_notifications_enabled,
          });

        setConfig(result);

        toast.success(
          "Configuration updated."
        );
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to update configuration."
          )
        );
      } finally {
        setSaving(false);
      }
    };


  if (loading) {
    return (
      <LoadingSpinner
        label="Loading configuration..."
      />
    );
  }


  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={
          loadConfig
        }
      />
    );
  }


  return (
    <div className="space-y-6">
      <PageHeader
        title="Admin Configuration"
        description="Manage operational SupportFlow settings."
      />

      <form
        onSubmit={handleSubmit}
        className="
          max-w-3xl space-y-6
          rounded-xl border
          border-slate-200
          bg-white p-6
          shadow-sm
        "
      >
        <div
          className="
            grid gap-4
            sm:grid-cols-2
          "
        >
          <Input
            type="number"
            min="50"
            max="99"
            label="SLA warning threshold (%)"
            value={
              config.sla_warning_threshold_percent
            }
            onChange={
              (event) =>
                updateField(
                  "sla_warning_threshold_percent",
                  event.target.value
                )
            }
          />

          <Input
            type="number"
            min="10"
            max="3600"
            label="Escalation scan interval (seconds)"
            value={
              config.escalation_check_interval_seconds
            }
            onChange={
              (event) =>
                updateField(
                  "escalation_check_interval_seconds",
                  event.target.value
                )
            }
          />

          <Input
            type="number"
            min="1"
            max="500"
            label="Maximum active tickets per Agent"
            value={
              config.max_active_tickets_per_agent
            }
            onChange={
              (event) =>
                updateField(
                  "max_active_tickets_per_agent",
                  event.target.value
                )
            }
          />
        </div>

        <div
          className="space-y-4"
        >
          {[
            [
              "auto_reassign_on_escalation",
              "Automatically reassign SLA-breached tickets",
            ],
            [
              "allow_requester_reopen",
              "Allow requester to reopen resolved tickets",
            ],
            [
              "allow_admin_public_response",
              "Allow Admin public ticket responses",
            ],
            [
              "notifications_enabled",
              "Enable persistent notifications",
            ],
            [
              "websocket_notifications_enabled",
              "Enable live WebSocket notifications",
            ],
          ].map(
            ([
              field,
              label,
            ]) => (
              <label
                key={field}
                className="
                  flex items-center
                  gap-3
                  text-sm
                  text-slate-700
                "
              >
                <input
                  type="checkbox"
                  checked={
                    config[field]
                  }
                  onChange={
                    (event) =>
                      updateField(
                        field,
                        event.target.checked
                      )
                  }
                  className="
                    h-4 w-4
                    rounded
                  "
                />

                {label}
              </label>
            )
          )}
        </div>

        <Button
          type="submit"
          loading={saving}
        >
          Save Configuration
        </Button>
      </form>
    </div>
  );
}


export default AdminConfiguration;