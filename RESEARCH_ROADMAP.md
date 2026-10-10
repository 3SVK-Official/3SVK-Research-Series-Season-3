# InfraWeft research and engineering roadmap

**Author:** Snehasish Das  
**Baseline:** version 0.1.0

This roadmap distinguishes immediate engineering work from claims that need experimental evidence. Priorities are ordered by risk reduction and evidential value rather than by feature count.

## Stage 1 — Preserve current behavior

**Objective:** establish a stable and reproducible baseline.

Work:
- Keep the synthetic fixtures and their expected outcomes under version control.
- Require tests for every rule change.
- Record runtime and software version with validation results.
- Verify deterministic report order and clearly report malformed or unsupported inputs.

Exit criteria:
- Test suite passes from a clean checkout.
- Each rule has at least one positive and one relevant negative test.
- Published demo output matches output from the recorded command.

## Stage 2 — Improve coverage transparency

**Objective:** make unsupported or indeterminate cases visible to reviewers.

Candidate work:
- Add explicit notices for unknown planned values and unrecognized resource shapes.
- Document supported Terraform and provider schema versions.
- Evaluate whether rule findings need confidence or applicability metadata; do not add a confidence percentage without a defined interpretation.
- Review policy parsing edge cases, including arrays of statements and string/object forms.

Exit criteria:
- Each new behavior has tests for positive, negative, malformed, and missing-value cases.
- Release notes list rule changes and their possible compatibility effects.

## Stage 3 — Evaluate detection independently

**Objective:** measure detection behavior on labeled examples.

Work:
- Assemble a sanitized corpus with negative controls and compound cases.
- Obtain two independent labels per case and resolve disagreements.
- Report per-rule confusion counts and precision/recall/F1.
- Keep held-out projects separate from development examples.

Exit criteria:
- Corpus and labels have versions and hashes.
- Evaluation command and all configuration are published.
- Results can be reproduced without access to private infrastructure.

## Stage 4 — Test the value of dependency weighting

**Objective:** test rather than assume that downstream context improves triage.

Work:
- Compare severity-only, severity-plus-count, and the current dependency-weighted approach.
- Run a dependency-bonus ablation.
- Evaluate ranking against adjudicated reviewer priorities.
- Analyze cases where declared dependencies differ from operational impact.

Exit criteria:
- Ranking metrics are calculated on held-out labeled cases.
- Results, including negative or inconclusive outcomes, are recorded.
- The paper's claims are updated only to match those results.

## Stage 5 — Consider controlled integration

**Objective:** determine whether the tool can be safely integrated into review workflows.

Work:
- Test sanitized pull-request artifacts without exposing real plan JSON in logs.
- Define human override, exception ownership, and audit history.
- Pin versions and make rule-set changes reviewable.
- Compare with an established infrastructure-as-code scanner.

Exit criteria:
- Security and privacy review is complete.
- Owners approve the coverage and exception policy.
- No deployment is automatically approved solely by absence of findings or the heuristic score.

## Explicit non-goals for version 0.1.0

The current version does not claim complete cloud coverage, exploitability analysis, effective IAM computation, runtime blast-radius discovery, calibrated breach probability, production readiness, or superiority to existing tools.
