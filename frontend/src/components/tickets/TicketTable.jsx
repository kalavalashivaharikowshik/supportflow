import {
  Link,
} from "react-router";

import {
  getTicketDetailsRoute,
} from "../../constants/routes";

import {
  formatDateTime,
} from "../../utils/dateTime";

import PriorityBadge from "./PriorityBadge";
import TicketStatusBadge from "./TicketStatusBadge";


function TicketTable({
  tickets,
}) {
  return (
    <div
      className="
        overflow-hidden
        rounded-2xl
        border
        border-slate-200
        bg-white
        shadow-sm
      "
    >
      <div className="overflow-x-auto">
        <table
          className="
            min-w-[900px]
            w-full
            divide-y
            divide-slate-200
          "
        >
          <thead
            className="
              bg-slate-50
            "
          >
            <tr>
              <th
                scope="col"
                className="
                  px-4 py-3
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-slate-500
                "
              >
                Ticket
              </th>

              <th
                scope="col"
                className="
                  px-4 py-3
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-slate-500
                "
              >
                Priority
              </th>

              <th
                scope="col"
                className="
                  px-4 py-3
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-slate-500
                "
              >
                Status
              </th>

              <th
                scope="col"
                className="
                  px-4 py-3
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-slate-500
                "
              >
                SLA Deadline
              </th>

              <th
                scope="col"
                className="
                  px-4 py-3
                  text-left
                  text-xs
                  font-semibold
                  uppercase
                  tracking-wide
                  text-slate-500
                "
              >
                Created
              </th>
            </tr>
          </thead>

          <tbody
            className="
              divide-y
              divide-slate-100
              bg-white
            "
          >
            {tickets.map(
              (ticket) => (
                <tr
                  key={ticket.id}
                  className="
                    transition
                    hover:bg-slate-50
                  "
                >
                  <td
                    className="
                      px-4 py-4
                      align-top
                    "
                  >
                    <div
                      className="
                        min-w-0
                      "
                    >
                      <Link
                        to={
                          getTicketDetailsRoute(
                            ticket.id
                          )
                        }
                        className="
                          inline-block
                          font-semibold
                          text-slate-900
                          transition
                          hover:text-slate-700
                          hover:underline
                          focus:outline-none
                          focus:ring-2
                          focus:ring-slate-400
                          focus:ring-offset-2
                        "
                      >
                        {
                          ticket.ticket_number
                        }
                      </Link>

                      <p
                        className="
                          mt-1
                          max-w-[18rem]
                          truncate
                          text-sm
                          text-slate-500
                        "
                        title={
                          ticket.title
                        }
                      >
                        {ticket.title}
                      </p>
                    </div>
                  </td>

                  <td
                    className="
                      px-4 py-4
                      align-top
                    "
                  >
                    <PriorityBadge
                      priority={
                        ticket.priority
                      }
                    />
                  </td>

                  <td
                    className="
                      px-4 py-4
                      align-top
                    "
                  >
                    <TicketStatusBadge
                      status={
                        ticket.status
                      }
                    />
                  </td>

                  <td
                    className="
                      whitespace-nowrap
                      px-4 py-4
                      align-top
                      text-sm
                      text-slate-600
                    "
                  >
                    {formatDateTime(
                      ticket.sla_deadline
                    )}
                  </td>

                  <td
                    className="
                      whitespace-nowrap
                      px-4 py-4
                      align-top
                      text-sm
                      text-slate-600
                    "
                  >
                    {formatDateTime(
                      ticket.created_at
                    )}
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}


export default TicketTable;