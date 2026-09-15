"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  KeyRound,
  LockOpen,
  Search,
  ShieldCheck,
} from "lucide-react";

import {
  lookupAccount,
  resetAccountMfa,
  resetAccountPassword,
  unlockAccount,
} from "@/lib/api";

import type {
  AccountToolResult,
} from "@/types";


interface AccountToolsProps {
  ticketNumber: string;
}


export function AccountTools({
  ticketNumber,
}: AccountToolsProps) {
  const router = useRouter();

  const [result, setResult] =
    useState<AccountToolResult | null>(null);

  const [loading, setLoading] =
    useState<string | null>(null);

  const [error, setError] =
    useState<string | null>(null);


  async function runAction(
    name: string,
    action: () => Promise<AccountToolResult>,
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
          : "Tool action failed",
      );
    } finally {
      setLoading(null);
    }
  }


  return (
    <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-6 py-4">
        <h2 className="font-semibold text-slate-950">
          Technician Tools
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Simulated enterprise account administration.
        </p>
      </div>

      <div className="p-6">
        {!result ? (
          <button
            type="button"
            disabled={loading !== null}
            onClick={() =>
              runAction(
                "lookup",
                () =>
                  lookupAccount(
                    ticketNumber,
                  ),
              )
            }
            className="flex items-center gap-2 rounded-md bg-slate-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-700 disabled:opacity-50"
          >
            <Search size={17} />

            {loading === "lookup"
              ? "Looking up..."
              : "Look Up User Account"}
          </button>
        ) : (
          <>
            <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                    Username
                  </p>

                  <p className="mt-1 font-mono font-semibold text-slate-900">
                    {
                      result.account
                        .username
                    }
                  </p>
                </div>

                <span
                  className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
                    result.account
                      .is_locked
                      ? "bg-red-50 text-red-700"
                      : "bg-emerald-50 text-emerald-700"
                  }`}
                >
                  {result.account.is_locked
                    ? "Locked"
                    : "Unlocked"}
                </span>
              </div>

              <dl className="mt-4 grid gap-4 text-sm sm:grid-cols-2">
                <div>
                  <dt className="text-slate-400">
                    Failed logins
                  </dt>

                  <dd className="mt-1 font-medium text-slate-700">
                    {
                      result.account
                        .failed_login_attempts
                    }
                  </dd>
                </div>

                <div>
                  <dt className="text-slate-400">
                    MFA
                  </dt>

                  <dd className="mt-1 font-medium text-slate-700">
                    {result.account
                      .mfa_enrolled
                      ? "Enrolled"
                      : "Not enrolled"}
                  </dd>
                </div>

                <div>
                  <dt className="text-slate-400">
                    Account
                  </dt>

                  <dd className="mt-1 font-medium text-slate-700">
                    {result.account
                      .is_enabled
                      ? "Enabled"
                      : "Disabled"}
                  </dd>
                </div>

                <div>
                  <dt className="text-slate-400">
                    Password change
                  </dt>

                  <dd className="mt-1 font-medium text-slate-700">
                    {result.account
                      .password_reset_required
                      ? "Required"
                      : "Not required"}
                  </dd>
                </div>
              </dl>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              <button
                type="button"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "unlock",
                    () =>
                      unlockAccount(
                        ticketNumber,
                      ),
                  )
                }
                className="flex items-center gap-2 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                <LockOpen size={16} />

                Unlock
              </button>

              <button
                type="button"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "password",
                    () =>
                      resetAccountPassword(
                        ticketNumber,
                      ),
                  )
                }
                className="flex items-center gap-2 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                <KeyRound size={16} />

                Reset Password
              </button>

              <button
                type="button"
                disabled={loading !== null}
                onClick={() =>
                  runAction(
                    "mfa",
                    () =>
                      resetAccountMfa(
                        ticketNumber,
                      ),
                  )
                }
                className="flex items-center gap-2 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
              >
                <ShieldCheck size={16} />

                Reset MFA
              </button>
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