import Button from "./Button";


function Pagination({
  page,
  totalPages,
  onPageChange,
}) {
  if (totalPages <= 1) {
    return null;
  }

  return (
    <div
      className="
        flex items-center justify-between
        gap-4 border-t border-slate-200
        pt-4
      "
    >
      <p className="text-sm text-slate-500">
        Page {page} of {totalPages}
      </p>

      <div className="flex gap-2">
        <Button
          variant="secondary"
          disabled={page <= 1}
          onClick={() =>
            onPageChange(
              page - 1
            )
          }
        >
          Previous
        </Button>

        <Button
          variant="secondary"
          disabled={
            page >= totalPages
          }
          onClick={() =>
            onPageChange(
              page + 1
            )
          }
        >
          Next
        </Button>
      </div>
    </div>
  );
}


export default Pagination;