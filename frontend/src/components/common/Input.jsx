function Input({
  label,
  error,
  id,
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

      <input
        id={id}
        className={`
          w-full rounded-lg border
          border-slate-300 bg-white
          px-3 py-2.5 text-sm
          text-slate-900 outline-none
          transition
          placeholder:text-slate-400
          focus:border-slate-500
          focus:ring-2
          focus:ring-slate-200
          ${error
            ? "border-red-500"
            : ""}
          ${className}
        `}
        {...props}
      />

      {error && (
        <p className="text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}


export default Input;