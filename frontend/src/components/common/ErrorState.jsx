import {
  CircleAlert,
} from "lucide-react";

import Button from "./Button";


function ErrorState({
  title = "Something went wrong",
  message = (
    "We could not load this information."
  ),
  onRetry,
}) {
  return (
    <div
      className="
        rounded-xl border border-red-200
        bg-red-50 px-6 py-8 text-center
      "
    >
      <CircleAlert
        className="mx-auto h-9 w-9 text-red-600"
      />

      <h3
        className="
          mt-3 font-semibold text-red-900
        "
      >
        {title}
      </h3>

      <p className="mt-2 text-sm text-red-700">
        {message}
      </p>

      {onRetry && (
        <Button
          variant="secondary"
          className="mt-5"
          onClick={onRetry}
        >
          Try again
        </Button>
      )}
    </div>
  );
}


export default ErrorState;