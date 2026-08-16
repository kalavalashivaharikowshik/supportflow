import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
} from "lucide-react";

import {
  formatRemainingTime,
} from "../../utils/sla";

import {
  formatDateTime,
} from "../../utils/dateTime";


function SlaStatusCard({
  sla,
}) {
  let Icon =
    CheckCircle2;

  let label =
    "Within SLA";

  let containerClass =
    "border-emerald-200 bg-emerald-50";

  let textClass =
    "text-emerald-800";

  let progressClass =
    "bg-emerald-500";


  if (sla.is_breached) {
    Icon =
      AlertTriangle;

    label =
      "SLA Breached";

    containerClass =
      "border-red-200 bg-red-50";

    textClass =
      "text-red-800";

    progressClass =
      "bg-red-600";
  } else if (
    sla.is_at_risk
  ) {
    Icon =
      Clock3;

    label =
      "SLA At Risk";

    containerClass =
      "border-amber-200 bg-amber-50";

    textClass =
      "text-amber-800";

    progressClass =
      "bg-amber-500";
  }


  const consumed =
    Math.min(
      100,
      Math.max(
        0,
        Number(
          sla.percentage_consumed ??
          0
        )
      )
    );


  return (
    <div
      className={`
        rounded-2xl
        border
        p-5
        shadow-sm
        ${containerClass}
      `}
    >
      <div
        className="
          flex items-start
          gap-3
        "
      >
        <div
          className="
            shrink-0
            rounded-xl
            bg-white/70
            p-2
          "
        >
          <Icon
            className={`
              h-5 w-5
              ${textClass}
            `}
            aria-hidden="true"
          />
        </div>

        <div
          className="
            min-w-0
          "
        >
          <p
            className={`
              font-semibold
              ${textClass}
            `}
          >
            {label}
          </p>

          <p
            className={`
              mt-1 text-sm
              ${textClass}
            `}
          >
            {formatRemainingTime(
              sla.remaining_seconds
            )}
          </p>
        </div>
      </div>

      <div
        className="
          mt-5
        "
      >
        <div
          className="
            flex items-center
            justify-between
            gap-4
            text-xs
          "
        >
          <span
            className="
              font-medium
              text-slate-600
            "
          >
            SLA consumed
          </span>

          <span
            className="
              font-semibold
              text-slate-900
            "
          >
            {consumed.toFixed(0)}%
          </span>
        </div>

        <div
          className="
            mt-2
            h-2
            overflow-hidden
            rounded-full
            bg-white/70
          "
          role="progressbar"
          aria-valuemin="0"
          aria-valuemax="100"
          aria-valuenow={
            consumed
          }
          aria-label="SLA consumption"
        >
          <div
            className={`
              h-full
              rounded-full
              transition-all
              duration-300
              ${progressClass}
            `}
            style={{
              width:
                `${consumed}%`,
            }}
          />
        </div>
      </div>

      <div
        className="
          mt-5 grid
          gap-4
          text-sm
          sm:grid-cols-2
        "
      >
        <div>
          <span
            className="
              text-slate-500
            "
          >
            Deadline
          </span>

          <p
            className="
              mt-1
              font-medium
              text-slate-900
            "
          >
            {formatDateTime(
              sla.sla_deadline
            )}
          </p>
        </div>

        <div>
          <span
            className="
              text-slate-500
            "
          >
            Consumed
          </span>

          <p
            className="
              mt-1
              font-medium
              text-slate-900
            "
          >
            {consumed.toFixed(0)}%
          </p>
        </div>
      </div>
    </div>
  );
}


export default SlaStatusCard;