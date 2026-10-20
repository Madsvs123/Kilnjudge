import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Clock3, LockKeyhole, Play } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link, useParams } from "react-router-dom";
import { z } from "zod";

import { api, formatApiError } from "../api";
import { VerdictBadge } from "../components/VerdictBadge";
import { difficultyLabel, formatLimit, formatRuntime, formatWhen } from "../format";
import type { ProblemDetail, Submission } from "../types";
import { usePageTitle } from "../usePageTitle";

const schema = z.object({
  source_code: z.string().min(1, "Write a solution before running it.").max(100000),
});

type SolutionValues = z.infer<typeof schema>;

const STARTER = `def main() -> None:
    first = input()
    # Read further lines the way the statement describes.
    print(first)


if __name__ == "__main__":
    main()
`;

function Paragraphs({ text }: { text: string }) {
  return (
    <>
      {text.split(/\n\n+/).map((paragraph, index) => (
        <p key={index}>{paragraph}</p>
      ))}
    </>
  );
}

export function ProblemPage() {
  const { slug = "" } = useParams();
  const queryClient = useQueryClient();
  const problem = useQuery({
    queryKey: ["problem", slug],
    enabled: Boolean(slug),
    queryFn: async () => (await api.get<ProblemDetail>(`/api/problems/${slug}/`)).data,
  });
  const attempts = useQuery({
    queryKey: ["submissions", slug],
    enabled: Boolean(slug),
    queryFn: async () =>
      (await api.get<Submission[]>("/api/submissions/", { params: { problem: slug } })).data,
  });
  const form = useForm<SolutionValues>({
    resolver: zodResolver(schema),
    defaultValues: { source_code: "" },
  });
  const submit = useMutation({
    mutationFn: async (sourceCode: string) =>
      (await api.post<Submission>(`/api/problems/${slug}/submit/`, { source_code: sourceCode })).data,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["submissions"] });
    },
  });

  usePageTitle(problem.data?.title ?? "Problem");

  async function onSubmit(values: SolutionValues) {
    submit.mutate(values.source_code);
  }

  function insertStarter() {
    const current = form.getValues("source_code");
    if (current.trim() && !window.confirm("Replace the current solution with the starter?")) {
      return;
    }
    form.setValue("source_code", STARTER, { shouldValidate: true });
  }

  if (problem.isLoading) {
    return (
      <main className="page">
        <p className="status">Loading the statement.</p>
      </main>
    );
  }
  if (problem.isError || !problem.data) {
    return (
      <main className="page">
        <p className="status is-error">{formatApiError(problem.error)}</p>
      </main>
    );
  }

  const detail = problem.data;
  const result = submit.data;

  return (
    <main className="page">
      <div className="workbench">
        <article className="statement">
          <p className="eyebrow">Problem {String(detail.position).padStart(2, "0")}</p>
          <h1>{detail.title}</h1>
          <div className="card-meta">
            <span className={`difficulty difficulty-${detail.difficulty}`}>
              {difficultyLabel(detail.difficulty)}
            </span>
            {detail.tags.map((tag) => (
              <span key={tag.slug} className="tag">
                {tag.label}
              </span>
            ))}
            <span>
              <Clock3 size={14} aria-hidden="true" />
              {formatLimit(detail.time_limit_ms)}
            </span>
            <span>
              <LockKeyhole size={14} aria-hidden="true" />
              {detail.hidden_count} hidden tests stored on the server
            </span>
          </div>
          <Paragraphs text={detail.statement} />
          <section>
            <h2>Input</h2>
            <Paragraphs text={detail.input_format} />
          </section>
          <section>
            <h2>Output</h2>
            <Paragraphs text={detail.output_format} />
          </section>
          <section>
            <h2>Samples</h2>
            {detail.samples.map((sample, index) => (
              <article key={index} className="sample">
                <h3>Sample {index + 1}</h3>
                <div className="io">
                  <div>
                    <span>Input</span>
                    <pre>{sample.input_data}</pre>
                  </div>
                  <div>
                    <span>Output</span>
                    <pre>{sample.expected_output}</pre>
                  </div>
                </div>
              </article>
            ))}
          </section>
          <section>
            <h2>Your runs</h2>
            {attempts.isLoading ? <p className="status">Loading your runs.</p> : null}
            {attempts.data && attempts.data.length === 0 ? (
              <p className="status">No solutions submitted for this problem yet.</p>
            ) : null}
            {attempts.data && attempts.data.length > 0 ? (
              <ul className="attempt-list">
                {attempts.data.map((attempt) => (
                  <li key={attempt.id}>
                    <Link to={`/submissions/${attempt.id}`}>
                      <VerdictBadge verdict={attempt.verdict} />
                      <span>{formatWhen(attempt.created_at)}</span>
                      <span>{formatRuntime(attempt.runtime_ms)}</span>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : null}
          </section>
        </article>
        <aside className="editor-panel">
          <div className="editor-bar">
            <strong>solution.py</strong>
            <button type="button" className="ghost" onClick={insertStarter}>
              Insert starter
            </button>
          </div>
          {result ? (
            <div className={`result-banner verdict-${result.verdict}`}>
              <VerdictBadge verdict={result.verdict} />
              <p>{result.message}</p>
              <p className="runtime">{formatRuntime(result.runtime_ms)}</p>
              <Link to={`/submissions/${result.id}`}>Open this run</Link>
            </div>
          ) : null}
          {submit.isError ? <p className="form-error">{formatApiError(submit.error)}</p> : null}
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <label className="sr-only" htmlFor="source_code">
              Python solution
            </label>
            <textarea
              id="source_code"
              spellCheck={false}
              placeholder="Read from stdin and print the answer."
              {...form.register("source_code")}
              onKeyDown={(event) => {
                if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
                  event.preventDefault();
                  void form.handleSubmit(onSubmit)();
                }
              }}
            />
            {form.formState.errors.source_code?.message ? (
              <p className="form-error">{form.formState.errors.source_code.message}</p>
            ) : null}
            <button type="submit" className="primary" disabled={submit.isPending}>
              <Play size={16} aria-hidden="true" />
              {submit.isPending ? "Running…" : "Run solution"}
            </button>
            <p className="hint">Ctrl+Enter runs the solution. Each test stops at the wall-clock limit.</p>
          </form>
        </aside>
      </div>
    </main>
  );
}
