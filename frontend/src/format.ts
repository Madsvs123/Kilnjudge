import type { Verdict } from "./types";

export const VERDICT_LABEL: Record<Verdict, string> = {
  accepted: "Accepted",
  wrong_answer: "Wrong Answer",
  time_limit: "Time Limit",
  runtime_error: "Runtime Error",
};

export function formatLimit(milliseconds: number): string {
  return `${milliseconds} ms per test on this problem`;
}

export function formatRuntime(milliseconds: number): string {
  return `${milliseconds} ms`;
}

export function formatWhen(iso: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(iso));
}

export function difficultyLabel(difficulty: string): string {
  if (!difficulty) {
    return "Practice";
  }
  return difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
}
