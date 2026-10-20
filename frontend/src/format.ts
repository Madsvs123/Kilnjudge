import type { Verdict } from "./types";

export const VERDICT_LABEL: Record<Verdict, string> = {
  accepted: "Accepted",
  wrong_answer: "Wrong answer",
  time_limit: "Time limit",
  runtime_error: "Runtime error",
};

export const VERDICT_DETAIL: Record<Verdict, string> = {
  accepted: "Every compared test matched, including hidden tests when they were run.",
  wrong_answer: "The printed output did not match a test, so later tests were skipped.",
  time_limit: "A test ran longer than the wall-clock limit stored on this problem.",
  runtime_error: "The solution stopped with an error before it could finish the test.",
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
