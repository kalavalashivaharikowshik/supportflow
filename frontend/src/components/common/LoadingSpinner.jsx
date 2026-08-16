function LoadingSpinner({
  label = "Loading...",
}) {
  return (
    <div
      className="flex items-center justify-center gap-3 py-8 text-slate-600"
      role="status"
    >
      <span
        className="
          h-5 w-5 animate-spin rounded-full
          border-2 border-slate-300
          border-t-slate-900
        "
      />

      <span className="text-sm">
        {label}
      </span>
    </div>
  );
}


export default LoadingSpinner;