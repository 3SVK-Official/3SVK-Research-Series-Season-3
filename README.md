# InfraWeft

**Explainable, offline risk review for cloud infrastructure changes**  
Prepared by **Snehasish Das** for the **National Research & Innovation Challenge Season 3 by 3SVK — Cloud Engineering track**.

> InfraWeft helps a reviewer see not only which infrastructure rule matched, but the exact planned evidence, a concrete remediation, and the downstream resources that may be affected.

## Why this prototype

Terraform plan output describes intended infrastructure changes, but a reviewer still has to connect security-sensitive values, destructive actions, and dependencies. InfraWeft is a small, credential-free review layer for a machine-readable Terraform plan. Its initial contribution is deliberately narrow: deterministic rules plus an explainable, dependency-weighted triage score.

This is an early prototype, not a production security product. It is not a substitute for provider-native policy, code review, backups, or a full IaC scanner.

## What it currently checks

| Rule | Signal | Initial severity |
|---|---|---|
| `CS-101` | Public SSH/RDP or all-port ingress in an AWS security group | High |
| `CS-201` | Wildcard IAM action and/or resource scope in an AWS IAM policy | High/Critical |
| `CS-301` | Delete/replace of a production-tagged or persistent data resource | Critical |
| `CS-401` | Explicitly disabled at-rest encryption on supported AWS database/EFS resources | High |
| `CS-501` | One or more S3 Block Public Access settings explicitly disabled | High |
| `CS-502` | Public-read or public-read-write ACL on a supported S3 bucket resource | High/Critical |

Rules examine planned `after` values (and `before` values where the risk is a deletion). Unrecognized resource types and unknown values are not inferred to be safe. Rule coverage is incomplete and provider-specific.

## Risk ranking

For each finding:

`priority_points = severity_weight + min(15, 3 × downstream_dependent_count)`

Severity weights: Critical 40, High 25, Medium 12, Low 5. The overall score is the sum of finding points, capped at 100. Score bands are Low (0–19), Moderate (20–39), High (40–69), and Critical (70–100).

This is an **explicit heuristic**, not an empirically calibrated probability of breach, downtime, or loss. The dependency graph comes from Terraform configuration dependency declarations; omitted or indirect edges can make blast-radius counts incomplete. The score should guide reviewer attention, never approve or apply a plan by itself.

## Run locally

Requires Python 3.10+; the prototype uses only the standard library.

```bash
# Optional virtual environment
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -e .

# Review the included synthetic risky plan
infraweft --plan examples/risky_plan.json --format markdown

# Save machine-readable output
infraweft --plan examples/risky_plan.json --format json --output report.json

# Run the test suite without installing the package
PYTHONPATH=src python -m unittest discover -s tests -v
```

To analyze a real Terraform plan locally:

```bash
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
infraweft --plan tfplan.json --format markdown --output infraweft-report.md
```

**Data handling:** Terraform plan JSON can contain sensitive infrastructure details. Keep real plan files and generated reports out of public repositories, CI logs, and screenshots unless they have been reviewed and sanitized. The included fixtures are synthetic and contain no cloud credentials.

## Example run

The bundled `examples/risky_plan.json` intentionally contains four risky patterns. The current prototype reports **4 findings** and a capped **Critical 100/100 heuristic score** for that synthetic fixture. This demonstrates rule execution; it is not a real-cloud benchmark or a claim of detection accuracy.

See [`docs/demo-risk-report.md`](docs/demo-risk-report.md) for the evidence-linked output and [`docs/research_note.md`](docs/research_note.md) for methodology, scope, and limitations.

## Reproducibility status

- Python standard library only.
- 12 unit tests currently pass in the local test run.
- Tests cover rule detection, dependency context, a benign public HTTPS case, malformed input, and deterministic output.
- Fixtures are intentionally small and synthetic; they do not estimate real-world false-positive/false-negative rates.
- No cloud account, live API, production plan, or third-party scanner was used in validation.

## Scope and next experiments

Before using this as a deployment gate, extend provider/resource coverage; test against sanitized real plans; compare against at least one established scanner; run blind-labeled cases with multiple reviewers; measure false positives, false negatives, analyst agreement, runtime and score-ranking usefulness; and review policy behavior with infrastructure owners. See [`docs/evaluation_plan.md`](docs/evaluation_plan.md).

## Official challenge workflow

The challenge listing calls for a research implementation, a GitHub pull request through the prescribed workflow, and submission of the participant's GitHub profile link plus screenshot proof. This folder does **not** create a PR or submit forms for you. Follow the [official Season 3 site](https://sites.google.com/view/3svk-research-s3/home) and its linked [Submission Guide & GitHub Steps](https://drive.google.com/file/d/1MBppotjMBeJ8N1uUFkRhxwzx7kID29gl/view?usp=sharing). Use the included [`docs/pull-request-template.md`](docs/pull-request-template.md) as a draft, then replace placeholders with the real PR URL and proof from your account.

## References

1. HashiCorp, *JSON Output Format Overview*. https://developer.hashicorp.com/terraform/internals/json-format
2. Amazon Web Services, *Configuring block public access settings for your S3 buckets*. https://docs.aws.amazon.com/AmazonS3/latest/userguide/configuring-block-public-access-bucket.html
3. Amazon Web Services, *Granting public access to your Amazon S3 data*. https://docs.aws.amazon.com/AmazonS3/latest/userguide/granting-public-access.html
4. GitHub Docs, *Creating a pull request from a fork*. https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork

## License

MIT. See [`LICENSE`](LICENSE).
