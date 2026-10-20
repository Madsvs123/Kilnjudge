import { useQuery } from "@tanstack/react-query";
import { Link, useSearchParams } from "react-router-dom";

import { api, formatApiError } from "../api";
import { VerdictBadge } from "../components/VerdictBadge";
import { formatRuntime } from "../format";
import type { SubmissionCompare } from "../types";
import { usePageTitle } from "../usePageTitle";

export function ComparePage() {
  usePageTitle("Compare");
  const [params] = useSearchParams();
  const left = params.get("left") ?? "";
  const right = params.get("right") ?? "";
  const ready = Boolean(left) && Boolean(right);
  const comparison = useQuery({
    queryKey: ["compare", left, right],
    enabled: ready,
    queryFn: async () =>
      (
        await api.get<SubmissionCompare>("/api/submissions/compare/", {
          params: { left, right },
        })
      ).data,
  });

  return (
    <main className="page">
      <header className="page-intro">
        <p className="eyebrow">Two firings</p>
        <h1>Compare submissions</h1>
        <p>Both runs must belong to the signed-in account. The diff is the source you stored.</p>
      </header>
      {!ready ? (
        <p className="status">
          Pick a left run and a right run from <Link to="/history">history</Link>.
        </p>
      ) : null}
      {comparison.isLoading ? <p className="status">Comparing the two runs.</p> : null}
      {comparison.isError ? <p className="status is-error">{formatApiError(comparison.error)}</p> : null}
      {comparison.data ? <CompareResult comparison={comparison.data} /> : null}
    </main>
  );
}

function CompareResult({ comparison }: { comparison: SubmissionCompare }) {
  const delta = comparison.runtime_delta_ms;
  const deltaLabel = delta === 0 ? "same runtime" : `${delta > 0 ? "+" : ""}${delta} ms on the right run`;

  return (
    <>
      <p className="lede">
        {comparison.same_verdict ? "Same verdict." : "Different verdicts."}{" "}
        {comparison.same_source ? "Same source." : "Source differs."} Runtime delta: {deltaLabel}.
      </p>
      <div className="compare-grid">
        <CompareColumn side="Left" record={comparison.left} />
        <CompareColumn side="Right" record={comparison.right} />
      </div>
      <section className="source-block">
        <h2>Source diff</h2>
        <pre>{comparison.source_diff || "The two sources are identical."}</pre>
      </section>
    </>
  );
}

function CompareColumn({
  side,
  record,
}: {
  side: string;
  record: SubmissionCompare["left"];
}) {
  return (
    <article className="source-block">
      <h2>
        {side}: <Link to={`/problems/${record.problem_slug}`}>{record.problem_title}</Link>
      </h2>
      <p>
        <VerdictBadge verdict={record.verdict} />{" "}
        <Link to={`/submissions/${record.id}`}>Run {record.id}</Link>
      </p>
      <p className="runtime">{formatRuntime(record.runtime_ms)}</p>
      <pre>{record.source_code}</pre>
    </article>
  );
}
