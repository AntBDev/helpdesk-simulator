import type {
  Customer,
  Ticket,
  TicketPriority,
} from "@/types";


interface TicketTableProps {
  tickets: Ticket[];
  customers: Customer[];
}


const priorityStyles: Record<
  TicketPriority,
  string
> = {
  HIGH: "bg-red-50 text-red-700 ring-red-600/20",
  MEDIUM:
    "bg-amber-50 text-amber-700 ring-amber-600/20",
  LOW: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
};


function formatStatus(status: string) {
  return status
    .split("_")
    .map(
      (word) =>
        word.charAt(0) +
        word.slice(1).toLowerCase(),
    )
    .join(" ");
}


function formatDeadline(deadline: string | null) {
  if (!deadline) {
    return "No SLA";
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(deadline));
}


export function TicketTable({
  tickets,
  customers,
}: TicketTableProps) {
  const customerMap = new Map(
    customers.map((customer) => [
      customer.id,
      `${customer.first_name} ${customer.last_name}`,
    ]),
  );

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-5 py-4">
        <h2 className="font-semibold text-slate-900">
          Ticket Queue
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Current incidents requiring service desk attention.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-5 py-3">
                Priority
              </th>

              <th className="px-5 py-3">
                Ticket
              </th>

              <th className="px-5 py-3">
                Customer
              </th>

              <th className="px-5 py-3">
                Category
              </th>

              <th className="px-5 py-3">
                Status
              </th>

              <th className="px-5 py-3">
                SLA
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100">
            {tickets.map((ticket) => (
              <tr
                key={ticket.id}
                className="transition hover:bg-slate-50"
              >
                <td className="px-5 py-4">
                  <span
                    className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset ${
                      priorityStyles[
                        ticket.priority
                      ]
                    }`}
                  >
                    {ticket.priority}
                  </span>
                </td>

                <td className="px-5 py-4">
                  <p className="font-medium text-slate-900">
                    {ticket.ticket_number}
                  </p>

                  <p className="mt-1 max-w-xs truncate text-slate-500">
                    {ticket.title}
                  </p>
                </td>

                <td className="px-5 py-4 text-slate-700">
                  {customerMap.get(
                    ticket.customer_id,
                  ) ?? "Unknown"}
                </td>

                <td className="px-5 py-4 text-slate-600">
                  {ticket.category}
                </td>

                <td className="px-5 py-4 text-slate-600">
                  {formatStatus(ticket.status)}
                </td>

                <td className="px-5 py-4 text-slate-600">
                  {formatDeadline(
                    ticket.sla_deadline,
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}