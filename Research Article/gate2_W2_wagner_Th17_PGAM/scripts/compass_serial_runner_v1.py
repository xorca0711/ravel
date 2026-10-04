#!/usr/bin/env python
"""Wp-R2: run Compass serially, because this host forbids multiprocessing pipes.

Compass 1.0.0 (the authors' wagnerlab-berkeley fork) always creates a
`multiprocessing.Pool`, even with `--num-processes 1`. On this sandboxed Windows
host `CreateNamedPipe` is denied, so Compass cannot start at all. This runner
replaces `compass.utils.create_process_pool` with a drop-in serial object whose
`apply_async`, `imap`, `imap_unordered`, `map`, `close`, `join` and `terminate`
behave as the single-worker case of the real pool: the same function is called
with the same arguments in the same order, in this process.

This is an execution shim, not an algorithmic change - no penalty, constraint,
objective or solver setting is touched. It is declared as a deviation in the
Wp-R2 contract, together with the two deviations that matter scientifically: the
input is not the paper's scVI-imputed matrix (never deposited) but micropooled
normalised counts, and the reaction set is restricted to the four subsystems the
paper's claim depends on.

Every argument after `--` is passed to Compass unchanged.
"""
from __future__ import annotations

import sys


class _Result:
    def __init__(self, value, error=None):
        self._value, self._error = value, error

    def get(self, timeout=None):
        if self._error is not None:
            raise self._error
        return self._value

    def wait(self, timeout=None):
        return None

    def ready(self):
        return True

    def successful(self):
        return self._error is None


class SerialPool:
    """Single-worker stand-in for multiprocessing.Pool, same call order."""

    def apply_async(self, func, args=(), kwds=None, callback=None, error_callback=None):
        try:
            value = func(*args, **(kwds or {}))
        except BaseException as exc:                      # noqa: BLE001 - mirrors Pool semantics
            if error_callback is not None:
                error_callback(exc)
            return _Result(None, error=exc)
        if callback is not None:
            callback(value)
        return _Result(value)

    def map(self, func, iterable, chunksize=None):
        return [func(x) for x in iterable]

    def imap(self, func, iterable, chunksize=None):
        return (func(x) for x in iterable)

    def imap_unordered(self, func, iterable, chunksize=None):
        return (func(x) for x in iterable)

    def close(self):
        return None

    def terminate(self):
        return None

    def join(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def main() -> int:
    if "--" not in sys.argv:
        print("usage: compass_serial_runner_v1.py -- <compass arguments>", file=sys.stderr)
        return 2
    passthrough = sys.argv[sys.argv.index("--") + 1:]

    from compass import utils
    utils.create_process_pool = lambda args: SerialPool()
    from compass import main as compass_main
    compass_main.utils.create_process_pool = lambda args: SerialPool()

    sys.argv = ["compass"] + passthrough
    compass_main.entry()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
