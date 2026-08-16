import {
  useCallback,
  useEffect,
  useState,
} from "react";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import ErrorState from "../../components/common/ErrorState";
import LoadingSpinner from "../../components/common/LoadingSpinner";
import PageHeader from "../../components/common/PageHeader";

import {
  getSlaConfigs,
  updateSlaConfig,
} from "../../services/slaService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";


function SLASettings() {
  const [items, setItems] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [
    savingPriority,
    setSavingPriority,
  ] = useState(null);

  const [error, setError] =
    useState("");


  const loadConfigs =
    useCallback(async () => {
      setLoading(true);
      setError("");

      try {
        const result =
          await getSlaConfigs();

        setItems(
          result.items ??
          result
        );
      } catch (apiError) {
        setError(
          getApiErrorMessage(
            apiError,
            "Unable to load SLA settings."
          )
        );
      } finally {
        setLoading(false);
      }
    }, []);


  useEffect(() => {
    loadConfigs();
  }, [loadConfigs]);


  const updateMinutes = (
    priority,
    value
  ) => {
    setItems(
      (current) =>
        current.map(
          (item) =>
            item.priority ===
            priority
              ? {
                  ...item,
                  resolution_minutes:
                    value,
                }
              : item
        )
    );
  };


  const saveConfig =
    async (item) => {
      const minutes =
        Number(
          item.resolution_minutes
        );

      if (
        !Number.isInteger(
          minutes
        ) ||
        minutes <= 0
      ) {
        toast.error(
          "SLA minutes must be a positive whole number."
        );
        return;
      }

      setSavingPriority(
        item.priority
      );

      try {
        await updateSlaConfig(
          item.priority,
          {
            resolution_minutes:
              minutes,
            is_active:
              item.is_active,
          }
        );

        toast.success(
          `${item.priority} SLA updated.`
        );

        await loadConfigs();
      } catch (apiError) {
        toast.error(
          getApiErrorMessage(
            apiError,
            "Unable to update SLA."
          )
        );
      } finally {
        setSavingPriority(
          null
        );
      }
    };


  if (loading) {
    return (
      <LoadingSpinner
        label="Loading SLA settings..."
      />
    );
  }


  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={
          loadConfigs
        }
      />
    );
  }


  return (
    <div className="space-y-6">
      <PageHeader
        title="SLA Settings"
        description="Configure resolution windows for each ticket priority."
      />

      <div
        className="
          grid gap-4
          md:grid-cols-2
        "
      >
        {items.map(
          (item) => (
            <div
              key={
                item.priority
              }
              className="
                rounded-xl border
                border-slate-200
                bg-white p-5
                shadow-sm
              "
            >
              <h2
                className="
                  font-semibold
                  text-slate-900
                "
              >
                {item.priority}
              </h2>

              <label
                className="
                  mt-4 block
                  text-sm font-medium
                  text-slate-700
                "
              >
                Resolution minutes
              </label>

              <input
                type="number"
                min="1"
                value={
                  item.resolution_minutes
                }
                onChange={
                  (event) =>
                    updateMinutes(
                      item.priority,
                      event.target.value
                    )
                }
                className="
                  mt-2 w-full
                  rounded-lg border
                  border-slate-300
                  px-3 py-2
                  text-sm
                "
              />

              <Button
                className="mt-4"
                loading={
                  savingPriority ===
                  item.priority
                }
                onClick={
                  () =>
                    saveConfig(
                      item
                    )
                }
              >
                Save
              </Button>
            </div>
          )
        )}
      </div>
    </div>
  );
}


export default SLASettings;