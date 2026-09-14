export type TicketPriority = "LOW" | "MEDIUM" | "HIGH";

export type TicketStatus =
  | "NEW"
  | "ASSIGNED"
  | "IN_PROGRESS"
  | "WAITING_ON_USER"
  | "WAITING_ON_VENDOR"
  | "ESCALATED"
  | "RESOLVED"
  | "CLOSED";

export interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  description: string;
  priority: TicketPriority;
  status: TicketStatus;
  category: string;
  subcategory: string | null;
  customer_id: number;
  device_id: number | null;
  sla_deadline: string | null;
  resolved_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  department: string;
  job_title: string;
  technical_skill: number;
  patience: number;
  cooperation: number;
  confidence: number;
  communication_clarity: number;
  created_at: string;
}

export interface Device {
  id: number;
  asset_tag: string;
  hostname: string;
  customer_id: number | null;

  device_type:
    | "LAPTOP"
    | "DESKTOP"
    | "PRINTER"
    | "PHONE"
    | "TABLET"
    | "OTHER";

  status:
    | "ONLINE"
    | "OFFLINE"
    | "REPAIR"
    | "RETIRED";

  manufacturer: string;
  model: string;
  operating_system: string;
  os_version: string | null;
  ip_address: string | null;
  created_at: string;
}