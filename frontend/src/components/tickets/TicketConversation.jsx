import {
  formatDateTime,
} from "../../utils/dateTime";


function TicketConversation({
  responses,
  currentUserId,
}) {
  if (
    responses.length === 0
  ) {
    return (
      <p
        className="
          rounded-lg bg-slate-50
          p-4 text-sm
          text-slate-500
        "
      >
        No responses yet.
      </p>
    );
  }


  return (
    <div className="space-y-4">
      {responses.map(
        (response) => {
          const isMine =
            response.user_id ===
            currentUserId;

          const isInternal =
            response.is_internal === true;


          return (
            <div
              key={response.id}
              className={`
                flex
                ${
                  isMine
                    ? "justify-end"
                    : "justify-start"
                }
              `}
            >
              <div
                className={`
                  max-w-2xl rounded-xl
                  border px-4 py-3

                  ${
                    isInternal
                      ? "border-amber-200 bg-amber-50 text-amber-950"
                      : isMine
                        ? "border-slate-900 bg-slate-900 text-white"
                        : "border-slate-200 bg-slate-100 text-slate-900"
                  }
                `}
              >
                {isInternal && (
                  <p
                    className="
                      mb-2 text-xs
                      font-semibold
                      uppercase tracking-wide
                      text-amber-700
                    "
                  >
                    Internal Note
                  </p>
                )}

                <p
                  className="
                    whitespace-pre-wrap
                    text-sm
                  "
                >
                  {
                    response.message
                  }
                </p>

                <p
                  className={`
                    mt-2 text-xs

                    ${
                      isInternal
                        ? "text-amber-700"
                        : isMine
                          ? "text-slate-300"
                          : "text-slate-500"
                    }
                  `}
                >
                  {formatDateTime(
                    response.created_at
                  )}
                </p>
              </div>
            </div>
          );
        }
      )}
    </div>
  );
}


export default TicketConversation;