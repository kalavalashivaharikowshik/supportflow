function AgentWorkloadTable({
  items,
}) {
  return (
    <div
      className="
        overflow-hidden
        rounded-xl border
        border-slate-200
        bg-white shadow-sm
      "
    >
      <div className="overflow-x-auto">
        <table
          className="
            min-w-full
            divide-y
            divide-slate-200
          "
        >
          <thead
            className="bg-slate-50"
          >
            <tr>
              <th
                className="
                  px-4 py-3
                  text-left text-xs
                  font-semibold uppercase
                  text-slate-500
                "
              >
                Agent
              </th>

              <th
                className="
                  px-4 py-3
                  text-left text-xs
                  font-semibold uppercase
                  text-slate-500
                "
              >
                Assigned
              </th>

              <th
                className="
                  px-4 py-3
                  text-left text-xs
                  font-semibold uppercase
                  text-slate-500
                "
              >
                Active
              </th>

              <th
                className="
                  px-4 py-3
                  text-left text-xs
                  font-semibold uppercase
                  text-slate-500
                "
              >
                Escalated
              </th>
            </tr>
          </thead>

          <tbody
            className="
              divide-y
              divide-slate-100
            "
          >
            {items.map(
              (item) => (
                <tr
                  key={
                    item.agent_id
                  }
                >
                  <td
                    className="
                      px-4 py-4
                    "
                  >
                    <p
                      className="
                        font-semibold
                        text-slate-900
                      "
                    >
                      {
                        item.full_name
                      }
                    </p>

                    <p
                      className="
                        mt-1 text-sm
                        text-slate-500
                      "
                    >
                      {item.email}
                    </p>
                  </td>

                  <td
                    className="
                      px-4 py-4
                      text-sm
                    "
                  >
                    {
                      item.total_assigned
                    }
                  </td>

                  <td
                    className="
                      px-4 py-4
                      text-sm
                    "
                  >
                    {
                      item.active_tickets
                    }
                  </td>

                  <td
                    className="
                      px-4 py-4
                      text-sm
                    "
                  >
                    {
                      item.escalated_tickets
                    }
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


export default AgentWorkloadTable;