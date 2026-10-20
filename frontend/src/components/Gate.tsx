import { Flame } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "react-router-dom";

export function Gate({
  title,
  lede,
  children,
  alternate,
}: {
  title: string;
  lede: string;
  children: ReactNode;
  alternate: { href: string; text: string };
}) {
  return (
    <main className="gate">
      <section className="gate-card">
        <p className="brand-kicker">
          <Flame size={18} aria-hidden="true" />
          Kilnjudge
        </p>
        <h1>{title}</h1>
        <p className="lede">{lede}</p>
        {children}
        <p className="alternate">
          <Link to={alternate.href}>{alternate.text}</Link>
        </p>
      </section>
    </main>
  );
}
