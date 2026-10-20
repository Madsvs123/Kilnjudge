import { useQuery } from "@tanstack/react-query";
import { Clock3, LockKeyhole } from "lucide-react";
import { Link } from "react-router-dom";

import { api, formatApiError } from "../api";
import { difficultyLabel, formatLimit } from "../format";
import type { ProblemSummary } from "../types";
import { usePageTitle } from "../usePageTitle";

export function ProblemListPage() {
  usePageTitle("Problems");
  const problems = useQuery({
    queryKey: ["problems"],
    queryFn: async () => (await api.get<ProblemSummary[]>("/api/problems/")).data,
  });

  return (
    <main className="page">
      <header className="page-intro">
        <p className="eyebrow">Practice log</p>
        <h1>Your exercises</h1>
        <p>
          Original string, array, and math problems, tagged by topic. Sample cases are printed
          here. Hidden cases stay on the server and are used when you run a solution.
        </p>
      </header>
      {problems.isLoading ? <p className="status">Loading problems.</p> : null}
      {problems.isError ? <p className="status is-error">{formatApiError(problems.error)}</p> : null}
      {problems.data && problems.data.length === 0 ? (
        <p className="status">No problems are loaded. Run migrations on the backend.</p>
      ) : null}
      <div className="problem-list">
        {problems.data?.map((problem) => (
          <Link key={problem.slug} to={`/problems/${problem.slug}`} className="problem-card">
            <span className="index">{String(problem.position).padStart(2, "0")}</span>
            <span className="problem-copy">
              <span className="card-meta">
                <span className={`difficulty difficulty-${problem.difficulty}`}>
                  {difficultyLabel(problem.difficulty)}
                </span>
                <span>
                  <Clock3 size={14} aria-hidden="true" />
                  {formatLimit(problem.time_limit_ms)}
                </span>
                <span>
                  <LockKeyhole size={14} aria-hidden="true" />
                  {problem.hidden_count} hidden
                </span>
              </span>
              <h2>{problem.title}</h2>
              <p>{problem.summary}</p>
              {problem.tags.length > 0 ? (
                <span className="tag-row">
                  {problem.tags.map((tag) => (
                    <span key={tag.slug} className="tag">
                      {tag.label}
                    </span>
                  ))}
                </span>
              ) : null}
            </span>
          </Link>
        ))}
      </div>
    </main>
  );
}
