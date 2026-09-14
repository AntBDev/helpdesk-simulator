import {
  BookOpen,
  GraduationCap,
  LayoutDashboard,
  Monitor,
  TicketCheck,
  Users,
} from "lucide-react";


const navigation = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    active: true,
  },
  {
    label: "Tickets",
    icon: TicketCheck,
  },
  {
    label: "Customers",
    icon: Users,
  },
  {
    label: "Devices",
    icon: Monitor,
  },
  {
    label: "Knowledge Base",
    icon: BookOpen,
  },
  {
    label: "Training",
    icon: GraduationCap,
  },
];


export function Sidebar() {
  return (
    <aside className="flex h-screen w-64 flex-col border-r border-slate-800 bg-slate-950 text-slate-300">
      <div className="border-b border-slate-800 px-6 py-5">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
          IT Operations
        </p>

        <h1 className="mt-1 text-lg font-semibold text-white">
          Service Desk
        </h1>
      </div>

      <nav className="flex-1 space-y-1 p-3">
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={`flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-sm transition ${
                item.active
                  ? "bg-slate-800 text-white"
                  : "hover:bg-slate-900 hover:text-white"
              }`}
            >
              <Icon size={18} />

              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="border-t border-slate-800 p-4">
        <div className="rounded-md bg-slate-900 p-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />

            <span className="text-xs font-medium text-slate-300">
              Systems Operational
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}