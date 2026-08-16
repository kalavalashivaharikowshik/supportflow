const variants = {
  primary:
    "bg-slate-900 text-white hover:bg-slate-800 focus-visible:ring-slate-500",

  secondary:
    "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 focus-visible:ring-slate-400",

  danger:
    "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500",

  ghost:
    "bg-transparent text-slate-700 hover:bg-slate-100 focus-visible:ring-slate-400",
};


const sizes = {
  sm:
    "min-h-9 px-3 py-1.5 text-sm",

  md:
    "min-h-10 px-4 py-2 text-sm",

  lg:
    "min-h-11 px-5 py-2.5 text-base",
};


function Button({
  children,
  type = "button",
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  className = "",
  ...props
}) {
  const isDisabled =
    disabled || loading;


  return (
    <button
      type={type}
      disabled={isDisabled}
      aria-busy={
        loading
          ? "true"
          : undefined
      }
      className={`
        inline-flex
        items-center
        justify-center
        gap-2
        rounded-lg
        font-semibold
        transition
        focus-visible:outline-none
        focus-visible:ring-2
        focus-visible:ring-offset-2
        disabled:cursor-not-allowed
        disabled:opacity-60
        ${variants[variant] ??
          variants.primary}
        ${sizes[size] ??
          sizes.md}
        ${className}
      `}
      {...props}
    >
      {loading && (
        <span
          className="
            h-4 w-4
            shrink-0
            animate-spin
            rounded-full
            border-2
            border-current
            border-t-transparent
          "
          aria-hidden="true"
        />
      )}

      <span>
        {loading
          ? "Please wait..."
          : children}
      </span>
    </button>
  );
}


export default Button;