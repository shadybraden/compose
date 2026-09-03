#!/usr/bin/env python3
"""Lint docker compose YAML files.

Only does two things, everything else (comments, blank lines, ordering of
anything that is not a service key) is left untouched:

  1. Reorders the keys inside each service to the fixed order below.
  2. Ensures a top-level `name:` block exists, adding an empty one if missing.

Keys not in the list are pushed to the end, keeping their relative order.

Usage:
    compose_lint.py [--check] [path ...]
      path may be a file or a directory (directories are searched
      recursively for compose.yaml / docker-compose{.yml,.yaml} / compose.yml).
      Defaults to the current directory.
"""

import argparse
import sys
from pathlib import Path

KEY_ORDER = [
    "image",
    "build",
    "container_name",
    "depends_on",
    "volumes",
    "volumes_from",
    "configs",
    "secrets",
    "environment",
    "env_file",
    "ports",
    "networks",
    "network_mode",
    "extra_hosts",
    "command",
    "entrypoint",
    "working_dir",
    "restart",
    "healthcheck",
    "logging",
    "labels",
    "user",
    "isolation",
    "cap_add",
    "cap_drop",
    "cpu_shares",
    "mem_limit",
    "mem_reservation",
    "dns",
    "sysctls",
    "deploy",
    "dns",
    "expose",
    "pids_limit",
    "init",
    "read_only",
    "device_cgroup_rules",
    "hostname",
    "security_opt",
    "tmpfs",
    "tty",
]
_RANK = {k: i for i, k in enumerate(KEY_ORDER)}
_UNKNOWN_RANK = len(_RANK)

COMPOSE_NAMES = {"compose.yaml", "docker-compose.yaml", "docker-compose.yml", "compose.yml"}


def is_blank(line):
    return not line.strip()


def is_comment(line):
    return line.lstrip().startswith("#")


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def key_line(lines, start, end):
    """Index of the first key line in a slice, or None."""
    for i in range(start, end):
        if not is_blank(lines[i]) and not is_comment(lines[i]):
            return i
    return None


def key_name(lines, i):
    return lines[i].strip().split(":", 1)[0].strip()


def split_slices(lines, level):
    """Partition lines into contiguous, non-overlapping [start, end) slices, one
    per block whose key line sits at `level` spaces of indentation. A block owns
    its key line and its body; the blank/comment run directly before the next
    key is peeled off and carried along as the following block's leading lines.
    """
    keys = [
        i
        for i, ln in enumerate(lines)
        if not is_blank(ln) and not is_comment(ln) and indent_of(ln) == level
    ]
    if not keys:
        return []
    n = len(keys)
    ranges = []
    prev_end = 0
    for j, k in enumerate(keys):
        end = keys[j + 1] if j + 1 < n else len(lines)
        stop = end
        if j + 1 < n:
            while stop - 1 >= k and (is_blank(lines[stop - 1]) or is_comment(lines[stop - 1])):
                stop -= 1
        start = prev_end if j > 0 else 0
        ranges.append([start, stop])
        prev_end = stop
    return ranges


def first_key_indent(lines):
    for i, ln in enumerate(lines):
        if not is_blank(ln) and not is_comment(ln):
            return indent_of(ln)
    return None


def reorder_service_body(body_lines, member_lv):
    # keep leading/trailing blank runs pinned to the service key line / the
    # block that follows, so reordering never strands a separator mid-service
    body = list(body_lines)
    lead = []
    while body and is_blank(body[0]):
        lead.append(body.pop(0))
    trail = []
    while body and is_blank(body[-1]):
        trail.append(body.pop(-1))
    slices = split_slices(body, member_lv)
    order = sorted(
        enumerate(slices),
        key=lambda t: (
            _RANK.get(key_name(body, key_line(body, t[1][0], t[1][1])), _UNKNOWN_RANK),
            t[0],
        ),
    )
    out = []
    for _, sl in order:
        out.extend(body[sl[0]:sl[1]])
    return lead + out + trail


def process(text):
    """Reorder services and ensure a top-level `name:` block. Returns new text."""
    lines = text.splitlines(keepends=True)
    if not lines:
        return text

    svc = None
    for a, b in split_slices(lines, 0):
        k = key_line(lines, a, b)
        if k is not None and key_name(lines, k) == "services":
            svc = (a, b)
            break

    edits = []  # (start, end, new_lines), applied bottom-up

    if svc:
        svc_key, svc_end = svc[0], svc[1]
        body = lines[svc_key + 1:svc_end]
        name_lv = first_key_indent(body)
        if name_lv is not None:
            for a, b in split_slices(body, name_lv):
                k = key_line(body, a, b)
                if k is None:
                    continue
                svc_body_start = svc_key + 1 + k + 1
                svc_body_end = svc_key + 1 + b
                member_lv = first_key_indent(body[k + 1:b])
                if member_lv is None:
                    continue
                new_body = reorder_service_body(
                    lines[svc_body_start:svc_body_end], member_lv
                )
                if new_body != lines[svc_body_start:svc_body_end]:
                    edits.append((svc_body_start, svc_body_end, new_body))

    has_name = any(
        key_line(lines, a, b) is not None
        and key_name(lines, key_line(lines, a, b)) == "name"
        for a, b in split_slices(lines, 0)
    )

    for start, end, new_lines in sorted(edits, reverse=True):
        lines[start:end] = new_lines

    if svc and not has_name:
        lines.insert(1, "name:\n") if lines[0].strip() == "---" else lines.insert(0, "name:\n")

    return "".join(lines)


def find_files(paths):
    files = []
    for p in paths:
        if p.is_file():
            files.append(p)
        else:
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.name in COMPOSE_NAMES:
                    files.append(f)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="compose_lint", description="Reorder service keys and ensure a top-level name: block."
    )
    ap.add_argument("--check", action="store_true",
                    help="report files that would change and exit 1; do not modify anything")
    ap.add_argument("paths", nargs="*", default=["."], type=Path,
                    help="files or directories to lint (default: current dir)")
    args = ap.parse_args(argv)

    files = find_files(args.paths)
    if not files:
        print("no compose files found", file=sys.stderr)
        return 2

    changed = []
    for f in files:
        try:
            orig = f.read_text()
        except OSError as e:
            print(f"{f}: read error: {e}", file=sys.stderr)
            continue
        new = process(orig)
        if new != orig:
            changed.append((f, new))

    if args.check:
        for f, _ in changed:
            print(f"would reformat {f}")
        return 1 if changed else 0

    for f, new in changed:
        f.write_text(new)
        print(f"reformatted {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())