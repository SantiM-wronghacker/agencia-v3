"""
CLI entrypoint for TeamDirector.

Usage::

    python -m src.agencia.agents.builder.run --goal "Launch MVP" --roles strategy,tech
    python -m src.agencia.agents.builder.run --goal "Expand to new market"

When ``--roles`` is omitted every registered built-in role participates.
"""
from __future__ import annotations

import argparse
import json
import sys

from .default_roles import BUILTIN_ROLES
from .team_director import TeamDirector


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Run TeamDirector with built-in roles",
    )
    parser.add_argument("--goal", required=True, help="Goal to accomplish")
    parser.add_argument(
        "--roles",
        default=None,
        help="Comma-separated list of roles (default: all registered)",
    )
    args = parser.parse_args(argv)

    director = TeamDirector(name="cli-team")
    for agent in BUILTIN_ROLES.values():
        director.register(agent)

    roles = [r.strip() for r in args.roles.split(",")] if args.roles else None

    try:
        result = director.run(goal=args.goal, roles=roles)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
