import {
  Search,
  X,
} from "lucide-react";


function SearchInput({
  value,
  onChange,
  placeholder = "Search...",
}) {
  return (
    <div className="relative">
      <Search
        className="
          pointer-events-none absolute
          left-3 top-1/2 h-4 w-4
          -translate-y-1/2
          text-slate-400
        "
      />

      <input
        type="search"
        value={value}
        onChange={
          (event) =>
            onChange(event.target.value)
        }
        placeholder={placeholder}
        className="
          w-full rounded-lg border
          border-slate-300 bg-white
          py-2.5 pl-9 pr-9 text-sm
          outline-none transition
          focus:border-slate-500
          focus:ring-2
          focus:ring-slate-200
        "
      />

      {value && (
        <button
          type="button"
          onClick={() => onChange("")}
          className="
            absolute right-3 top-1/2
            -translate-y-1/2
            text-slate-400
            hover:text-slate-700
          "
          aria-label="Clear search"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}


export default SearchInput;