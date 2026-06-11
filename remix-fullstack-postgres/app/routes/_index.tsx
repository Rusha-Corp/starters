import type { MetaFunction } from "@remix-run/node";
import { Link } from "@remix-run/react";

export const meta: MetaFunction = () => {
  return [
    { title: "Remix Fullstack App" },
    { name: "description", content: "A Remix fullstack application with PostgreSQL" },
  ];
};

export default function Index() {
  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: 1.8 }}>
      <h1>Welcome to Remix</h1>
      <p>
        This is a fullstack Remix application backed by PostgreSQL.
      </p>
      <nav>
        <Link to="/health">Health Check</Link>
      </nav>
    </div>
  );
}
