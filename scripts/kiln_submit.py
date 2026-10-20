"""Submit a local Python file to the Kilnjudge API on this machine.

The judge still runs the source in a child process with network sockets disabled
and with the problem's wall-clock timeout. This script only posts the file.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit a .py file to the local Kilnjudge API.")
    parser.add_argument("slug", help="Problem slug, for example shelf-gaps")
    parser.add_argument("source", type=pathlib.Path, help="Path to the Python solution")
    parser.add_argument("--username", required=True, help="Account on the local judge")
    parser.add_argument("--password", required=True, help="Password for that local account")
    parser.add_argument("--api", default="http://127.0.0.1:8000", help="API origin")
    parser.add_argument(
        "--samples-only",
        action="store_true",
        help="Check samples without storing an official submission",
    )
    args = parser.parse_args()

    if args.source.suffix.lower() != ".py":
        print("The source path must be a .py file.", file=sys.stderr)
        return 2
    if not args.source.is_file():
        print(f"No file at {args.source}.", file=sys.stderr)
        return 2

    origin = args.api.rstrip("/")
    token = _login(origin, args.username, args.password)
    path = "samples" if args.samples_only else "submit"
    payload = _request(
        f"{origin}/api/problems/{args.slug}/{path}/",
        {"source_code": args.source.read_text(encoding="utf-8")},
        token=token,
    )
    verdict = str(payload.get("verdict", "unknown"))
    print(verdict)
    message = payload.get("message")
    if message:
        print(message)
    if "runtime_ms" in payload:
        print(f"{payload['runtime_ms']} milliseconds")
    if not args.samples_only and payload.get("id") is not None:
        print(f"stored submission {payload['id']}")
    return 0 if verdict == "accepted" else 1


def _login(origin: str, username: str, password: str) -> str:
    body = _request(f"{origin}/api/auth/token/", {"username": username, "password": password})
    access = body.get("access")
    if not isinstance(access, str) or not access:
        raise SystemExit("The API did not return an access token.")
    return access


def _request(url: str, payload: dict, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print(detail or error.reason, file=sys.stderr)
        code = error.code if isinstance(error.code, int) else 1
        raise SystemExit(code)
    except urllib.error.URLError as error:
        print(f"Could not reach {url}: {error.reason}", file=sys.stderr)
        raise SystemExit(1)
    parsed = json.loads(raw) if raw else {}
    if not isinstance(parsed, dict):
        raise SystemExit("The API returned a response this script does not understand.")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
