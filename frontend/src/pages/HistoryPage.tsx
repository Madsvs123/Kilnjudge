import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";

import { api, formatApiError } from "../api";
import { VerdictBadge } from "../components/VerdictBadge";
import { formatRuntime, formatWhen } from "../format";
import type { Submission } from "../types";
import { usePageTitle } from "../usePageTitle";

export function HistoryPage() {
  usePageTitle("History");
  const [leftId, setLeftId] = useState<number | null>(null);
  const [rightId, setRightId] = useState<number | null>(null);
  const history = useQuery({
    queryKey: ["submissions"],
    queryFn: async () => (await api.get<Submission[]>("/api/submissions/")).data,
  });

  return (
    <main className="page">
      <header className="page-intro">
        <p className="eyebrow">Your firings</p>
        <h1>Submission history</h1>
        <p>Only the signed-in account can see these runs. Verdicts are stored with the source you sent.</p>
      </header>
      {history.isLoading ? <p className="status">Loading history.</p> : null}
      {history.isError ? <p className="status is-error">{formatApiError(history.error)}</p> : null}
      <p className="compare-bar">
        Left {leftId ?? "—"} · Right {rightId ?? "—"}{" "}
        {leftId && rightId ? (
          <Link to={`/compare?left=${leftId}&right=${rightId}`}>Compare these runs</Link>
        ) : (
          <span>Choose two runs to compare.</span>
        )}
      </p>
      {history.data && history.data.length === 0 ? (
        <p className="status">You have not submitted a solution yet.</p>
      ) : null}
      {history.data && history.data.length > 0 ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>When</th>
                <th>Problem</th>
                <th>Verdict</th>
                <th>Runtime</th>
                <th>Compare</th>
              </tr>
            </thead>
            <tbody>
              {history.data.map((submission) => (
                <tr key={submission.id}>
                  <td>
                    <Link to={`/submissions/${submission.id}`}>{formatWhen(submission.created_at)}</Link>
                  </td>
                  <td>
                    <Link to={`/problems/${submission.problem_slug}`}>{submission.problem_title}</Link>
                  </td>
                  <td>
                    <VerdictBadge verdict={submission.verdict} />
                  </td>
                  <td>{formatRuntime(submission.runtime_ms)}</td>
                  <td className="compare-picks">
                    <button type="button" className="ghost" onClick={() => setLeftId(submission.id)}>
                      Left
                    </button>
                    <button type="button" className="ghost" onClick={() => setRightId(submission.id)}>
                      Right
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </main>
  );
}
