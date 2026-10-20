"""Run the owner's Python against local tests with a wall-clock limit."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time

PRELUDE = """\
import _socket
import runpy
import socket
import sys


def _deny_network(*_args, **_kwargs):
    raise OSError("network sockets are disabled")


_socket.socket = _deny_network
socket.socket = _deny_network
socket.create_connection = _deny_network
if hasattr(socket, "create_server"):
    socket.create_server = _deny_network
if hasattr(_socket, "socketpair"):
    _socket.socketpair = _deny_network
if hasattr(socket, "socketpair"):
    socket.socketpair = _deny_network

solution = sys.argv[1]
sys.argv = [solution]
runpy.run_path(solution, run_name="__main__")
"""


def run_source(source_code: str, tests, time_limit_ms: int) -> dict:
    ordered = list(tests)
        if not ordered:
            return _outcome("runtime_error", 0, "This problem has no tests, so it cannot be judged.")

    workdir = tempfile.mkdtemp(prefix="kilnjudge-")
    try:
        prelude_path = os.path.join(workdir, "_kiln_prelude.py")
        solution_path = os.path.join(workdir, "solution.py")
        _write(prelude_path, PRELUDE)
        _write(solution_path, source_code)

        command = [sys.executable, "-I", "-X", "utf8", prelude_path, solution_path]
        timeout_s = max(int(time_limit_ms), 1) / 1000
        run_kwargs = {
            "capture_output": True,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "timeout": timeout_s,
            "cwd": workdir,
            "env": _child_env(),
        }
        if os.name == "nt":
            run_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        total_ms = 0
        sample_number = 0
        hidden_number = 0
        for test in ordered:
            if test.is_sample:
                sample_number += 1
                label = f"sample {sample_number}"
            else:
                hidden_number += 1
                label = f"hidden test {hidden_number}"

            started = time.perf_counter()
            try:
                completed = subprocess.run(
                    command,
                    input=test.input_data,
                    **run_kwargs,
                )
            except subprocess.TimeoutExpired:
                total_ms += int(timeout_s * 1000)
                return _outcome(
                    "time_limit",
                    total_ms,
                    (
                        f"Time limit of {int(time_limit_ms)} ms for this problem was exceeded on {label}. "
                        "The run was stopped, and later tests were not started."
                    ),
                )
            except OSError:
                return _outcome(
                    "runtime_error",
                    total_ms,
                    "Runtime error. The Python interpreter could not be started for this problem.",
                )

            total_ms += int((time.perf_counter() - started) * 1000)
            if completed.returncode != 0:
                hint = _stderr_hint(completed.stderr) if test.is_sample else ""
                return _outcome(
                    "runtime_error",
                    total_ms,
                    f"Runtime error on {label}. The solution stopped before printing an answer.{hint}",
                )
            if _normalize(completed.stdout) != _normalize(test.expected_output):
                return _outcome(
                    "wrong_answer",
                    total_ms,
                    f"Wrong answer on {label}. The printed output did not match, and later tests were not run.",
                )

        noun = "test" if len(ordered) == 1 else "tests"
        return _outcome(
            "accepted",
            total_ms,
            f"Accepted. Passed all {len(ordered)} {noun}, including every hidden test stored for this problem.",
        )
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _write(path: str, contents: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(contents)


def _child_env() -> dict:
    keep = (
        "SYSTEMROOT",
        "SYSTEMDRIVE",
        "WINDIR",
        "PATH",
        "PATHEXT",
        "COMSPEC",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "HOMEDRIVE",
        "HOMEPATH",
    )
    env = {key: os.environ[key] for key in keep if os.environ.get(key)}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _normalize(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.strip():
        return ""
    return "\n".join(line.rstrip() for line in normalized.strip().split("\n"))


def _stderr_hint(stderr: str) -> str:
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    if not lines:
        return ""
    return " " + lines[-1][:160]


def _outcome(verdict: str, runtime_ms: int, message: str) -> dict:
    return {
        "verdict": verdict,
        "runtime_ms": max(runtime_ms, 0),
        "message": message[:300],
    }
