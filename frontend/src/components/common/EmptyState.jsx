import {
  Inbox,
} from "lucide-react";


function EmptyState({
  title = "Nothing here yet",
  description = (
    "There is currently no data to display."
  ),
  action = null,
}) {
  return (
    <div
      className="
        rounded-xl border border-dashed
        border-slate-300 bg-white px-6
        py-12 text-center
      "
    >
      <Inbox
        className="mx-auto h-10 w-10 text-slate-400"
      />

      <h3
        className="
          mt-4 text-base font-semibold
          text-slate-900
        "
      >
        {title}
      </h3>

      <p
        className="
          mx-auto mt-2 max-w-md text-sm
          text-slate-500
        "
      >
        {description}
      </p>

      {action && (
        <div className="mt-5">
          {action}
        </div>
      )}
    </div>
  );
}


export default EmptyState;