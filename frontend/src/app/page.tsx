import {
  AlertTriangle,
  Clock3,
  TicketCheck,
  Users,
} from "lucide-react";

import { Sidebar } from "@/components/sidebar";
import { StatCard } from "@/components/stat-card";
import { TicketTable } from "@/components/ticket-table";
import {
  getCustomers,
  getDevices,
  getTickets,
} from "@/lib/api";


export default async function Home() {
  const [
    tickets,
    customers,
    devices,
  ] = await Promise.all([
    getTickets(),
    getCustomers(),
    getDevices(),
  ]);

  const openTickets = tickets.filter(
    (ticket) =>
      ticket.status !== "CLOSED" &&
      ticket.status !== "RESOLVED",
  );

  const highPriorityTickets = openTickets.filter(
    (ticket) =>
      ticket.priority === "HIGH",
  );

  const now = new Date();

  const slaRiskTickets = openTickets.filter(
    (ticket) => {
      if (!ticket.sla_deadline) {
        return false;
      }

      const deadline = new Date(
        ticket.sla_deadline,
      );

      const remaining =
        deadline.getTime() - now.getTime();

      return (
        remaining > 0 &&
        remaining <= 60 * 60 * 1000
      );
    },
  );

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <main className="min-w-0 flex-1">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-8">
          <div>
            <p className="text-sm font-medium text-slate-900">
              Help Desk Simulator
            </p>

            <p className="text-xs text-slate-500">
              Tier 1 Service Desk
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-slate-900">
                Technician
              </p>

              <p className="text-xs text-slate-500">
                Training Environment
              </p>
            </div>

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">
              T1
            </div>
          </div>
        </header>

        <div className="mx-auto max-w-[1600px] p-8">
          <div>
            <p className="text-sm font-medium text-slate-500">
              Service Desk Overview
            </p>

            <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-950">
              Ticket Operations
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              Monitor incidents, priorities, and SLA activity across the simulated organization.
            </p>
          </div>

          <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <StatCard
              title="Open Tickets"
              value={openTickets.length}
              subtitle={`${tickets.length} total incidents`}
              icon={TicketCheck}
            />

            <StatCard
              title="High Priority"
              value={highPriorityTickets.length}
              subtitle="Requires immediate attention"
              icon={AlertTriangle}
            />

            <StatCard
              title="SLA Risk"
              value={slaRiskTickets.length}
              subtitle="Due within the next hour"
              icon={Clock3}
            />

            <StatCard
              title="Employees"
              value={customers.length}
              subtitle={`${devices.length} managed devices`}
              icon={Users}
            />
          </section>

          <section className="mt-8">
            <TicketTable
              tickets={tickets}
              customers={customers}
            />
          </section>
        </div>
      </main>
    </div>
  );
}