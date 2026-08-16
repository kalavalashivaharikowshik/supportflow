function MetricCard({
  title,
  value,
  description,
  icon: Icon,
}) {
  return (
    <div
      className="
        group
        rounded-2xl border
        border-slate-200
        bg-white p-5
        shadow-sm
        transition-all
        duration-200
        hover:-translate-y-0.5
        hover:shadow-md
      "
    >
      <div
        className="
          flex items-start
          justify-between
          gap-4
        "
      >
        <div
          className="
            min-w-0
          "
        >
          <p
            className="
              text-sm
              font-medium
              text-slate-500
            "
          >
            {title}
          </p>

          <p
            className="
              mt-2 truncate
              text-3xl
              font-bold
              tracking-tight
              text-slate-900
            "
          >
            {value ?? "—"}
          </p>
        </div>

        {Icon && (
          <div
            className="
              shrink-0
              rounded-xl
              bg-slate-100
              p-2.5
              text-slate-700
              transition
              group-hover:bg-slate-200
            "
          >
            <Icon
              className="
                h-5 w-5
              "
              aria-hidden="true"
            />
          </div>
        )}
      </div>

      {description && (
        <p
          className="
            mt-3
            text-xs
            leading-5
            text-slate-500
          "
        >
          {description}
        </p>
      )}
    </div>
  );
}


export default MetricCard;