function PageHeader({
  title,
  description,
  action,
}) {
  return (
    <div
      className="
        flex flex-col
        gap-4
        sm:flex-row
        sm:items-start
        sm:justify-between
      "
    >
      <div
        className="
          min-w-0
        "
      >
        <h1
          className="
            text-2xl
            font-bold
            tracking-tight
            text-slate-900
            sm:text-3xl
          "
        >
          {title}
        </h1>

        {description && (
          <p
            className="
              mt-2
              max-w-3xl
              text-sm
              leading-6
              text-slate-500
            "
          >
            {description}
          </p>
        )}
      </div>

      {action && (
        <div
          className="
            flex shrink-0
            items-center
            sm:pt-1
          "
        >
          {action}
        </div>
      )}
    </div>
  );
}


export default PageHeader;