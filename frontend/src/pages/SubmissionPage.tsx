import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { api, formatApiError } from "../api";
import { VerdictBadge } from "../components/VerdictBadge";
import { formatRuntime, formatWhen, VERDICT_DETAIL } from "../format";
import type { Submission } from "../types";
import { usePageTitle } from "../usePageTitle";

export function SubmissionPage() {
  const { id = "" } = useParams();
  const submission = useQuery({
    queryKey: ["submission", id],
    enabled: Boolean(id),
    queryFn: async () => (await api.get<Submission>(`/api/submissions/${id}/`)).data,
  });

  usePageTitle(submission.data ? `${submission.data.problem_title} run` : "Submission");

  if (submission.isLoading) {
    return (
      <main className="page">
        <p className="status">Loading the submission.</p>
      </main>
    );
  }
  if (submission.isError || !submission.data) {
    return (
      <main className="page">
        <p className="status is-error">{formatApiError(submission.error)}</p>
      </main>
    );
  }

  const record = submission.data;
  return (
    <main className="page narrow">
      <p className="eyebrow">Stored run</p>
      <h1>
        <Link to={`/problems/${record.problem_slug}`}>{record.problem_title}</Link>
      </h1>
      <div className={`result-banner verdict-${record.verdict}`}>
        <VerdictBadge verdict={record.verdict} />
        <p>{VERDICT_DETAIL[record.verdict]}</p>
        <p>{record.message}</p>
        <p className="runtime">
          {formatRuntime(record.runtime_ms)} · {formatWhen(record.created_at)}
        </p>
      </div>
      <section className="source-block">
        <h2>Source</h2>
        <pre>{record.source_code}</pre>
      </section>
      <p>
        <Link to="/history">Back to history</Link>
      </p>
    </main>
  );
}
