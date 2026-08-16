import {
  formatDateTime,
} from "../../utils/dateTime";


function AuditTimeline({
  items,
}) {
  if (items.length === 0) {
    return (
      <p
        className="
          text-sm
          text-slate-500
        "
      >
        No audit activity available.
      </p>
    );
  }


  return (
    <div
      className="
        relative space-y-5
        border-l
        border-slate-200
        pl-5
      "
    >
      {items.map(
        (item) => (
          <div
            key={item.id}
            className="relative"
          >
            <span
              className="
                absolute -left-[25px]
                top-1 h-2.5 w-2.5
                rounded-full
                bg-slate-500
              "
            />

            <p
              className="
                text-sm font-semibold
                text-slate-900
              "
            >
              {item.description}
            </p>

            <p
              className="
                mt-1 text-xs
                text-slate-500
              "
            >
              {item.actor_name ?? "System"}
              {" • "}
              {formatDateTime(
                item.created_at
              )}
            </p>
          </div>
        )
      )}
    </div>
  );
}


export default AuditTimeline;