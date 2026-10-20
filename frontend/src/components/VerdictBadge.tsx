import clsx from "clsx";

import { VERDICT_LABEL } from "../format";
import type { Verdict } from "../types";

export function VerdictBadge({ verdict }: { verdict: Verdict }) {
  return <span className={clsx("badge", `verdict-${verdict}`)}>{VERDICT_LABEL[verdict]}</span>;
}
