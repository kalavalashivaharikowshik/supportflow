function Select({
  label,
  error,
  id,
  options = [],
  placeholder = "Select an option",
  className = "",
  ...props
}) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label
          htmlFor={id}
          className="block text-sm font-medium text-slate-700"
        >
          {label}
        </label>
      )}

      <select
        id={id}
        className={`
          w-full rounded-lg border
          border-slate-300 bg-white
          px-3 py-2.5 text-sm
          text-slate-900 outline-none
          transition
          focus:border-slate-500
          focus:ring-2
          focus:ring-slate-200
          ${error
            ? "border-red-500"
            : ""}
          ${className}
        `}
        {...props}
      >
        <option value="">
          {placeholder}
        </option>

        {options.map(
          (option) => (
            <option
              key={option.value}
              value={option.value}
            >
              {option.label}
            </option>
          )
        )}
      </select>

      {error && (
        <p className="text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}


export default Select;