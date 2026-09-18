"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Activity,
  HardDrive,
  Network,
  Power,
  RefreshCw,
  Search,
  ServerCog,
} from "lucide-react";

import {
  checkDeviceResources,
  enableDeviceNetworkAdapter,
  inspectDevice,
  rebootDevice,
  restartDeviceService,
  testDeviceConnectivity,
  testDeviceDns,
} from "@/lib/api";

import type {
  DeviceToolResult,
} from "@/types";


interface DeviceToolsProps {
  ticketNumber: string;
}


export function DeviceTools({
  ticketNumber,
}: DeviceToolsProps) {
  const router = useRouter();

  const [result, setResult] =
    useState<DeviceToolResult | null>(null);

  const [loading, setLoading] =
    useState<string | null>(null);

  const [error, setError] =
    useState<string | null>(null);


  async function runAction(
    name: string,
    action: () => Promise<DeviceToolResult>,
  ) {
    setLoading(name);
    setError(null);

    try {
      const response = await action();

      setResult(response);
      router.refresh();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Diagnostic action failed",
      );
    } finally {
      setLoading(null);
    }
  }


  return (
    <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-6 py-4">
        <h2 className="font-semibold text-slate-950">
          Device Diagnostics
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Inspect and troubleshoot the simulated endpoint.
        </p>
      </div>

      <div className="p-6">
        {!result ? (
          <button
            type="button"
            disabled={loading !== null}
            onClick={() =>
              runAction(
                "inspect",
                () => inspectDevice(ticketNumber),
              )
            }
            className="flex items-center gap-2 rounded-md bg-slate-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
          >
            <Search size={17} />

            {loading === "inspect"
              ? "Inspecting..."
              : "Inspect Device"}
          </button>
        ) : (
          <>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <StateItem
                label="Adapter"
                value={
                  result.state.network_adapter_enabled
                    ? "Enabled"
                    : "Disabled"
                }
              />

              <StateItem
                label="Gateway"
                value={
                  result.state.gateway_reachable
                    ? "Reachable"
                    : "Unreachable"
                }
              />

              <StateItem
                label="DNS"
                value={
                  result.state.dns_resolving
                    ? "Working"
                    : "Failing"
                }
              />

              <StateItem
                label="Internet"
                value={
                  result.state.internet_reachable
                    ? "Reachable"
                    : "Unreachable"
                }
              />

              <StateItem
                label="CPU"
                value={`${result.state.cpu_usage_percent}%`}
              />

              <StateItem
                label="Memory"
                value={`${result.state.memory_usage_percent}%`}
              />

              <StateItem
                label="Disk Free"
                value={`${result.state.disk_free_gb} GB`}
              />

              <StateItem
                label="Reboot"
                value={
                  result.state.pending_reboot
                    ? "Pending"
                    : "Not pending"
                }
              />
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              <ToolButton
                icon={Network}
                label="Connectivity"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "connectivity",
                    () =>
                      testDeviceConnectivity(
                        ticketNumber,
                      ),
                  )
                }
              />

              <ToolButton
                icon={Activity}
                label="DNS Test"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "dns",
                    () =>
                      testDeviceDns(
                        ticketNumber,
                      ),
                  )
                }
              />

              <ToolButton
                icon={HardDrive}
                label="Resources"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "resources",
                    () =>
                      checkDeviceResources(
                        ticketNumber,
                      ),
                  )
                }
              />

              <ToolButton
                icon={Power}
                label="Enable Adapter"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "adapter",
                    () =>
                      enableDeviceNetworkAdapter(
                        ticketNumber,
                      ),
                  )
                }
              />

              <ToolButton
                icon={ServerCog}
                label="Restart Service"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "service",
                    () =>
                      restartDeviceService(
                        ticketNumber,
                      ),
                  )
                }
              />

              <ToolButton
                icon={RefreshCw}
                label="Reboot"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "reboot",
                    () =>
                      rebootDevice(
                        ticketNumber,
                      ),
                  )
                }
              />
            </div>

            <p className="mt-4 text-sm text-slate-600">
              {result.message}
            </p>
          </>
        )}

        {error && (
          <p className="mt-4 text-sm text-red-600">
            {error}
          </p>
        )}
      </div>
    </section>
  );
}


interface StateItemProps {
  label: string;
  value: string;
}


function StateItem({
  label,
  value,
}: StateItemProps) {
  return (
    <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
      <p className="text-xs uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-slate-800">
        {value}
      </p>
    </div>
  );
}


interface ToolButtonProps {
  icon: React.ComponentType<{
    size?: number;
  }>;
  label: string;
  disabled: boolean;
  onClick: () => void;
}


function ToolButton({
  icon: Icon,
  label,
  disabled,
  onClick,
}: ToolButtonProps) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className="flex items-center gap-2 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
    >
      <Icon size={16} />

      {label}
    </button>
  );
}