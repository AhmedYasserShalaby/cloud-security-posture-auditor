from __future__ import annotations

import argparse

from cloud_audit.config import load_settings, project_path
from cloud_audit.generate_snapshots import generate_snapshots
from cloud_audit.health import assert_outputs
from cloud_audit.rules import load_rules
from cloud_audit.scan import scan_snapshots, write_reports


def main() -> None:
    parser = argparse.ArgumentParser(description="Cloud security posture auditor")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("generate-snapshots", help="Generate synthetic AWS-style snapshots")
    scan_parser = subparsers.add_parser("scan", help="Scan snapshots with YAML policy rules")
    scan_parser.add_argument("--source", choices=["snapshots", "aws"], default="snapshots")
    subparsers.add_parser("export-report", help="Regenerate markdown reports from CSV exports")
    subparsers.add_parser("validate-rules", help="Validate YAML policy rules")
    subparsers.add_parser("health-check", help="Validate exports and scorecards")
    args = parser.parse_args()

    if args.command == "generate-snapshots":
        outputs = generate_snapshots()
        print("Generated snapshots:")
        for name, path in outputs.items():
            print(f"- {name}: {path}")
    elif args.command == "scan":
        outputs = scan_snapshots(source=args.source)
        print(f"Findings: {outputs['findings']}")
        print(f"Risk summary: {outputs['risk_summary']}")
        print(f"Account scorecard: {outputs['account_scorecard']}")
    elif args.command == "export-report":
        import pandas as pd

        settings = load_settings()
        exports = settings["exports"]
        write_reports(
            pd.read_csv(project_path(exports["findings"])),
            pd.read_csv(project_path(exports["risk_summary"])),
            pd.read_csv(project_path(exports["account_scorecard"])),
        )
        print("Regenerated security_report.md and remediation_plan.md")
    elif args.command == "validate-rules":
        settings = load_settings()
        rules = load_rules(project_path(settings["paths"]["rules"]))
        print(f"Validated rules: {len(rules)}")
    elif args.command == "health-check":
        assert_outputs()
        print("Health checks passed.")


if __name__ == "__main__":
    main()
