"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import type {
  TicketStatus,
} from "@/types";

import {
  updateTicketStatus,
} from "@/lib/api";


interface TicketStatusControlsProps {
  ticketNumber: string;
  currentStatus: TicketStatus;
}


const transitions: Record<
  TicketStatus,
  TicketStatus[]
> = {
  NEW: [
    "ASSIGNED",
    "IN_PROGRESS",
    "ESCALATED",
  ],
  ASSIGNED: [
    "IN_PROGRESS",
    "ESCALATED",
  ],
  IN_PROGRESS: [
    "WAITING_ON_USER",
    "WAITING_ON_VENDOR",
    "ESCALATED",
    "RESOLVED",
  ],
  WAITING_ON_USER: [
    "IN_PROGRESS",
    "ESCALATED",
    "RESOLVED",
  ],
  WAITING_ON_VENDOR: [
    "IN_PROGRESS",
    "ESCALATED",
    "RESOLVED",
  ],
  ESCALATED: [
    "IN_PROGRESS",
    "WAITING_ON_USER",
    "WAITING_ON_VENDOR",
    "RESOLVED",
  ],
  RESOLVED: [
    "CLOSED",
    "IN_PROGRESS",
  ],
  CLOSED: [
    "IN_PROGRESS",
  ],
};


function statusLabel(
  status: TicketStatus,
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


export function TicketStatusControls({
  ticketNumber,
  currentStatus,
}: TicketStatusControlsProps) {
  const router = useRouter();

  const [loading, setLoading] =
    useState<TicketStatus | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  async function changeStatus(
    status: TicketStatus,
  ) {
    setLoading(status);
    setError(null);

    try {
      await updateTicketStatus(
        ticketNumber,
        status,
      );

      router.refresh();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to update ticket",
      );
    } finally {
      setLoading(null);
    }
  }

  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {transitions[currentStatus].map(
          (status) => (
            <button
              key={status}
              type="button"
              disabled={loading !== null}
              onClick={() =>
                changeStatus(status)
              }
              className="rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading === status
                ? "Updating..."
                : statusLabel(status)}
            </button>
          ),
        )}
      </div>

      {error && (
        <p className="mt-3 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}