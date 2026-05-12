from __future__ import annotations

from pathlib import Path

import pandas as pd

from cloud_audit.config import load_settings, project_path
from cloud_audit.rules import load_rules


def required_exports() -> dict[str, Path]:
    settings = load_settings()
    return {name: project_path(path) for name, path in settings["exports"].items()}


def verify_outputs() -> list[str]:
    settings = load_settings()
    failures = []
    paths = required_exports()
    for name, path in paths.items():
        if not path.exists():
            failures.append(f"Missing export: {name}")
    if failures:
        return failures

    findings = pd.read_csv(paths["findings"])
    summary = pd.read_csv(paths["risk_summary"])
    scorecard = pd.read_csv(paths["account_scorecard"])
    if findings.empty:
        failures.append("No findings generated")
    if int(summary["finding_count"].sum()) != len(findings):
        failures.append("Risk summary count does not match findings")
    threshold = settings["quality"]["minimum_security_score"]
    low_scores = scorecard[scorecard["security_score"] < threshold]
    failures.extend(f"{row.account_id} score below threshold" for row in low_scores.itertuples(index=False))
    load_rules(project_path(settings["paths"]["rules"]))
    return failures


def assert_outputs() -> None:
    failures = verify_outputs()
    if failures:
        raise RuntimeError("Health checks failed:\n- " + "\n- ".join(failures))
