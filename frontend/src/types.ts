export type Verdict = "accepted" | "wrong_answer" | "time_limit" | "runtime_error";

export type Tag = {
  slug: string;
  label: string;
};

export type ProblemSummary = {
  slug: string;
  title: string;
  position: number;
  difficulty: string;
  tags: Tag[];
  summary: string;
  time_limit_ms: number;
  sample_count: number;
  hidden_count: number;
};

export type Sample = {
  input_data: string;
  expected_output: string;
};

export type Hint = {
  position: number;
  body: string;
};

export type Editorial = {
  notes: string;
  updated_at: string;
};

export type ProblemDetail = {
  slug: string;
  title: string;
  position: number;
  difficulty: string;
  tags: Tag[];
  summary: string;
  statement: string;
  input_format: string;
  output_format: string;
  time_limit_ms: number;
  hidden_count: number;
  hints: Hint[];
  editorial: Editorial | null;
  samples: Sample[];
};

export type Submission = {
  id: number;
  problem_slug: string;
  problem_title: string;
  verdict: Verdict;
  runtime_ms: number;
  message: string;
  source_code: string;
  created_at: string;
};
