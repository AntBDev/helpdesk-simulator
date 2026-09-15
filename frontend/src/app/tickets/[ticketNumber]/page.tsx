import Link from "next/link";
import {
  ArrowLeft,
  Clock3,
  Laptop,
  Mail,
  UserRound,
} from "lucide-react";

import { AccountTools } from "@/components/account-tools";
import { Sidebar } from "@/components/sidebar";
import { TicketStatusControls } from "@/components/ticket-status-controls";
import {
  getCustomer,
  getDevice,
  getTicket,
  getTicketEvents,
} from "@/lib/api";


function formatDate(
  value: string | null,
) {
  if (!value) {
    return "Not available";
  }

  return new Intl.DateTimeFormat(
    "en-US",
    {
      dateStyle: "medium",
      timeStyle: "short",
    },
  ).format(new Date(value));
}


function formatStatus(
  status: string,
) {
  return status
    .split("_")
    .map(
      (word) =>
        word.charAt(0) +
        word.slice(1).toLowerCase(),
    )
    .join(" ");
}


export default async function TicketPage(
  props: {
    params: Promise<{
      ticketNumber: string;
    }>;
  },
) {
  const params = await props.params;

  const ticketNumber =
    decodeURIComponent(
      params.ticketNumber,
    );

  const ticket = await getTicket(
    ticketNumber,
  );

  const [
    customer,
    device,
    events,
  ] = await Promise.all([
    getCustomer(ticket.customer_id),

    ticket.device_id
      ? getDevice(ticket.device_id)
      : Promise.resolve(null),

    getTicketEvents(
      ticket.ticket_number,
    ),
  ]);

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <main className="min-w-0 flex-1">
        <header className="flex h-16 items-center border-b border-slate-200 bg-white px-8">
          <Link
            href="/"
            className="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-950"
          >
            <ArrowLeft size={17} />

            Back to ticket queue
          </Link>
        </header>

        <div className="mx-auto max-w-[1500px] p-8">
          <div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-start">
            <div>
              <div className="flex items-center gap-3">
                <p className="font-mono text-sm font-semibold text-slate-500">
                  {ticket.ticket_number}
                </p>

                <span className="rounded-full bg-slate-200 px-2.5 py-1 text-xs font-semibold text-slate-700">
                  {formatStatus(
                    ticket.status,
                  )}
                </span>

                <span className="rounded-full bg-red-50 px-2.5 py-1 text-xs font-semibold text-red-700">
                  {ticket.priority}
                </span>
              </div>

              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
                {ticket.title}
              </h1>

              <p className="mt-2 text-sm text-slate-500">
                {ticket.category}

                {ticket.subcategory
                  ? ` / ${ticket.subcategory}`
                  : ""}
              </p>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Workflow
              </p>

              <div className="mt-3">
                <TicketStatusControls
                  ticketNumber={
                    ticket.ticket_number
                  }
                  currentStatus={
                    ticket.status
                  }
                />
              </div>
            </div>
          </div>

          <div className="mt-8 grid gap-6 xl:grid-cols-[1fr_340px]">
            <div className="space-y-6">
              <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="font-semibold text-slate-950">
                  Issue Description
                </h2>

                <p className="mt-4 whitespace-pre-wrap leading-7 text-slate-700">
                  {ticket.description}
                </p>
              </section>

              <AccountTools
                ticketNumber={ticket.ticket_number}
              />
              
              <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
                <div className="border-b border-slate-200 px-6 py-4">
                  <h2 className="font-semibold text-slate-950">
                    Activity
                  </h2>

                  <p className="mt-1 text-sm text-slate-500">
                    Immutable ticket history and technician actions.
                  </p>
                </div>

                <div className="divide-y divide-slate-100">
                  {events.map((event) => (
                    <div
                      key={event.id}
                      className="flex gap-4 px-6 py-5"
                    >
                      <div className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-slate-400" />

                      <div>
                        <p className="text-sm font-semibold text-slate-900">
                          {formatStatus(
                            event.event_type,
                          )}
                        </p>

                        {event.details && (
                          <p className="mt-1 text-sm text-slate-600">
                            {event.details}
                          </p>
                        )}

                        <p className="mt-2 text-xs text-slate-400">
                          {event.actor}
                          {" • "}
                          {formatDate(
                            event.created_at,
                          )}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </div>

            <aside className="space-y-6">
              <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center gap-2">
                  <UserRound
                    size={18}
                    className="text-slate-500"
                  />

                  <h2 className="font-semibold text-slate-950">
                    Customer
                  </h2>
                </div>

                <p className="mt-4 font-semibold text-slate-900">
                  {customer.first_name}{" "}
                  {customer.last_name}
                </p>

                <p className="mt-1 text-sm text-slate-500">
                  {customer.job_title}
                </p>

                <p className="text-sm text-slate-500">
                  {customer.department}
                </p>

                <div className="mt-4 flex items-center gap-2 text-sm text-slate-600">
                  <Mail size={15} />

                  {customer.email}
                </div>
              </section>

              <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center gap-2">
                  <Laptop
                    size={18}
                    className="text-slate-500"
                  />

                  <h2 className="font-semibold text-slate-950">
                    Device
                  </h2>
                </div>

                {device ? (
                  <div className="mt-4">
                    <p className="font-semibold text-slate-900">
                      {device.hostname}
                    </p>

                    <p className="mt-1 text-sm text-slate-500">
                      {device.manufacturer}{" "}
                      {device.model}
                    </p>

                    <dl className="mt-4 space-y-3 text-sm">
                      <div>
                        <dt className="text-slate-400">
                          Asset tag
                        </dt>

                        <dd className="font-medium text-slate-700">
                          {device.asset_tag}
                        </dd>
                      </div>

                      <div>
                        <dt className="text-slate-400">
                          Operating system
                        </dt>

                        <dd className="font-medium text-slate-700">
                          {
                            device.operating_system
                          }{" "}
                          {device.os_version ??
                            ""}
                        </dd>
                      </div>

                      <div>
                        <dt className="text-slate-400">
                          IP address
                        </dt>

                        <dd className="font-mono text-slate-700">
                          {device.ip_address ??
                            "Not available"}
                        </dd>
                      </div>
                    </dl>
                  </div>
                ) : (
                  <p className="mt-4 text-sm text-slate-500">
                    No device associated with this incident.
                  </p>
                )}
              </section>

              <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center gap-2">
                  <Clock3
                    size={18}
                    className="text-slate-500"
                  />

                  <h2 className="font-semibold text-slate-950">
                    SLA
                  </h2>
                </div>

                <dl className="mt-4 space-y-4 text-sm">
                  <div>
                    <dt className="text-slate-400">
                      Created
                    </dt>

                    <dd className="mt-1 font-medium text-slate-700">
                      {formatDate(
                        ticket.created_at,
                      )}
                    </dd>
                  </div>

                  <div>
                    <dt className="text-slate-400">
                      Resolution deadline
                    </dt>

                    <dd className="mt-1 font-medium text-slate-700">
                      {formatDate(
                        ticket.sla_deadline,
                      )}
                    </dd>
                  </div>

                  <div>
                    <dt className="text-slate-400">
                      Resolved
                    </dt>

                    <dd className="mt-1 font-medium text-slate-700">
                      {formatDate(
                        ticket.resolved_at,
                      )}
                    </dd>
                  </div>
                </dl>
              </section>
            </aside>
          </div>
        </div>
      </main>
    </div>
  );
}