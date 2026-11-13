#!/usr/bin/env python3
"""Unified CLI for generating and auditing all blog SVG diagrams.

Examples:
    python tools/visuals.py list
    python tools/visuals.py build gauss poncelet
    python tools/visuals.py build all
    python tools/visuals.py audit
"""

import argparse
import sys

from visuals import TOPICS, audit_all_svgs


def cmd_list():
    print(f"Registered visual topics ({len(TOPICS)}):")
    for slug in sorted(TOPICS):
        meta = TOPICS[slug]
        print(f"  {slug:24s} [{meta['domain']:17s}] {meta['summary']}")


def cmd_build(targets):
    slugs = sorted(TOPICS) if ("all" in targets or not targets) else targets
    unknown = [s for s in slugs if s not in TOPICS]
    if unknown:
        print(f"Error: unknown topic(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(TOPICS))}", file=sys.stderr)
        return 1
    for slug in slugs:
        print(f"[{slug}] building & verifying assertions...")
        TOPICS[slug]["fn"]()
    count = audit_all_svgs()
    print(f"Done: {len(slugs)} topic(s) built; {count} SVGs passed XML & UX typography audit.")
    return 0


def cmd_audit():
    count = audit_all_svgs()
    print(f"Audit passed: all {count} SVGs in assets/images/ have valid XML, aspect ratios, and Chirpy font bounds.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Hands-on Dad blog SVG visuals toolkit")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all registered diagram topics")

    p_build = sub.add_parser("build", help="Generate SVGs and run assertions for topic(s) or 'all'")
    p_build.add_argument("topics", nargs="*", default=["all"], help="Topic slug(s) or 'all'")

    sub.add_parser("audit", help="Validate XML, aspect ratios, and rendered font sizes across all SVGs")

    args = parser.parse_args(argv)
    if args.command == "list":
        cmd_list()
        return 0
    if args.command == "audit":
        return cmd_audit()
    if args.command == "build":
        return cmd_build(args.topics)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
