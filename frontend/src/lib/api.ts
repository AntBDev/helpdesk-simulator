import type {
  Customer,
  Device,
  Ticket,
} from "@/types";


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000/api/v1";


async function apiRequest<T>(
  endpoint: string,
): Promise<T> {
  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status}`,
    );
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