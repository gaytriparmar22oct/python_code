"""
argparse — build proper command-line tools with flags, defaults, and help.

Why SREs care: every automation script becomes a CLI others use. argparse gives
you --flags, type validation, defaults, required args, and auto-generated
--help. This is how you turn a script into a reusable tool.

Run:
  python argparse_demo.py --service payments --replicas 5
  python argparse_demo.py --service auth --dry-run
  python argparse_demo.py --help
"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scale a service to a desired replica count.",
    )

    # Required option (must be provided).
    parser.add_argument(
        "--service", required=True,
        help="Name of the service to scale.",
    )

    # Typed option with a default — argparse validates it's an int.
    parser.add_argument(
        "--replicas", type=int, default=3,
        help="Desired replica count (default: 3).",
    )

    # Restrict to a fixed set of values.
    parser.add_argument(
        "--env", choices=["dev", "staging", "prod"], default="dev",
        help="Target environment.",
    )

    # Boolean flag: present -> True, absent -> False.
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the action without performing it.",
    )
    return parser


def main():
    args = build_parser().parse_args()

    action = f"Scale '{args.service}' in {args.env} to {args.replicas} replicas"
    if args.dry_run:
        print(f"[DRY-RUN] Would: {action}")
    else:
        print(f"Executing: {action}")


if __name__ == "__main__":
    main()
