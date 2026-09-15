import type {
  Customer,
  Device,
  Ticket,
  TicketEvent,
  TicketStatus,
  AccountToolResult,
} from "@/types";


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000/api/v1";


async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      cache: "no-store",
      ...options,
    },
  );

  if (!response.ok) {
    const body = await response
      .json()
      .catch(() => null);

    const detail =
      body?.detail ??
      `API request failed: ${response.status}`;

    throw new Error(detail);
  }

  return response.json();
}


export function getTickets(): Promise<Ticket[]> {
  return apiRequest<Ticket[]>("/tickets");
}


export function getCustomers(): Promise<Customer[]> {
  return apiRequest<Customer[]>("/customers");
}


export function getDevices(): Promise<Device[]> {
  return apiRequest<Device[]>("/devices");
}


export function getTicket(
  ticketNumber: string,
): Promise<Ticket> {
  return apiRequest<Ticket>(
    `/tickets/${ticketNumber}`,
  );
}


export function getTicketEvents(
  ticketNumber: string,
): Promise<TicketEvent[]> {
  return apiRequest<TicketEvent[]>(
    `/tickets/${ticketNumber}/events`,
  );
}


export function getCustomer(
  customerId: number,
): Promise<Customer> {
  return apiRequest<Customer>(
    `/customers/${customerId}`,
  );
}


export function getDevice(
  deviceId: number,
): Promise<Device> {
  return apiRequest<Device>(
    `/devices/${deviceId}`,
  );
}


export function updateTicketStatus(
  ticketNumber: string,
  status: TicketStatus,
): Promise<Ticket> {
  return apiRequest<Ticket>(
    `/tickets/${ticketNumber}/status`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        status,
      }),
    },
  );
}

export function lookupAccount(
  ticketNumber: string,
): Promise<AccountToolResult> {
  return apiRequest<AccountToolResult>(
    `/tickets/${ticketNumber}/tools/account/lookup`,
    {
      method: "POST",
    },
  );
}


export function unlockAccount(
  ticketNumber: string,
): Promise<AccountToolResult> {
  return apiRequest<AccountToolResult>(
    `/tickets/${ticketNumber}/tools/account/unlock`,
    {
      method: "POST",
    },
  );
}


export function resetAccountPassword(
  ticketNumber: string,
): Promise<AccountToolResult> {
  return apiRequest<AccountToolResult>(
    `/tickets/${ticketNumber}/tools/account/password-reset`,
    {
      method: "POST",
    },
  );
}


export function resetAccountMfa(
  ticketNumber: string,
): Promise<AccountToolResult> {
  return apiRequest<AccountToolResult>(
    `/tickets/${ticketNumber}/tools/account/mfa-reset`,
    {
      method: "POST",
    },
  );
}