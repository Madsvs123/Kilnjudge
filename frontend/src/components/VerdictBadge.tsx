import clsx from "clsx";

import { VERDICT_DETAIL, VERDICT_LABEL } from "../format";
import type { Verdict } from "../types";

export function VerdictBadge({ verdict }: { verdict: Verdict }) {
  return (
    <span className={clsx("badge", `verdict-${verdict}`)} title={VERDICT_DETAIL[verdict]}>
      {VERDICT_LABEL[verdict]}
    </span>
  );
}
