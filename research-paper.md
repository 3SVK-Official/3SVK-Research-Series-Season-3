# InfraWeft: Explainable Risk Review for Cloud Infrastructure Changes

**Author:** Snehasish Das  
**Track:** Cloud Engineering  
**Challenge:** National Research & Innovation Challenge Season 3 by 3SVK  
**Prototype version:** 0.1.0  
**Prepared:** 10 October 2026

## Abstract

InfraWeft is an offline prototype that analyzes Terraform plan JSON and produces evidence-linked findings for selected infrastructure risks. It targets a practical review problem: security-sensitive planned values, destructive changes, and dependency context may be difficult to assess together during code review. The current implementation includes rules for public administrative ingress, wildcard IAM scope, destructive changes to production or persistent resources, explicit disabled encryption, and selected S3 public-access controls. Findings include a resource address, evidence path, explanation, remediation, and the count of declared downstream dependents. A transparent heuristic ranks findings by severity and dependency fan-out. The prototype requires no cloud credentials and uses synthetic fixtures for testing. Twelve unit tests pass locally, but this is functional verification—not evidence of production efficacy. Provider coverage is limited, the score is not calibrated as a probability, and no comparison against established scanners or blind-labeled real infrastructure plans has yet been completed.

## 1. Problem statement

Infrastructure-as-code review is often distributed across several kinds of reasoning: what changed, whether a resulting configuration is risky, whether a change is destructive, and which downstream resources depend on the changed component. The prototype focuses on the review step after a Terraform plan has been generated. It does not attempt to replace Terraform, a policy-as-code platform, cloud-native security controls, or a complete static analyzer.

The input format is the machine-readable plan representation produced by `terraform show -json`. The plan includes a set of resource changes and a configuration representation. A plan can contain sensitive details; local processing reduces the need to upload it to a third-party service, but users must still protect files and generated reports.

## 2. Research question and hypothesis

**Research question:** Does attaching explicit evidence and declared downstream-dependency context to deterministic infrastructure findings make the review output more actionable than a flat list of rule matches?

**Working hypothesis:** In controlled, labeled scenarios, a transparent score combining rule severity with downstream dependency fan-out can rank compound-impact changes more consistently with expert review priorities than a simple count of findings.

This hypothesis remains unproven. The current fixture tests establish that implemented cases behave as coded; they do not establish improved reviewer performance or generalize to production infrastructure.

## 3. Proposed contribution

The prototype combines four elements in one reproducible local command:

1. **Planned-state inspection:** evaluates explicit planned values and actions in Terraform plan JSON.
2. **Evidence-linked findings:** every finding includes a resource address, JSON evidence path, observed value, reason, and remediation.
3. **Declared dependency context:** counts downstream resources reachable through the dependency edges represented in Terraform configuration.
4. **Deterministic prioritization:** computes a visible score from severity weights plus a capped dependency fan-out bonus.

The contribution is not a claim that IaC scanning or policy-as-code is new. The proposal is a small, inspectable approach to combining these signals in an offline PR-review artifact. Differentiation and usefulness require evaluation against existing tools and reviewers.

## 4. Architecture

1. **Input:** a local Terraform plan file rendered to JSON (`terraform show -json`).
2. **Parser:** validates the `resource_changes` list and reads configuration dependency declarations.
3. **Rule engine:** evaluates supported resource types and explicit planned values.
4. **Impact context:** creates edges from a declared dependency to the resource that depends on it, then counts transitive downstream dependents of each changed resource.
5. **Scorer:** adds a rule-severity weight and a capped dependent-count bonus; caps the project score at 100.
6. **Output:** Markdown for human review or JSON for automation.

No credentials are requested by the application. The current prototype does not query live cloud resources, estimate monetary cost, automatically apply changes, or block a production deployment.

## 5. Implemented rules

| Rule | Detection in version 0.1.0 | Main limitation |
|---|---|---|
| CS-101 | Public CIDR plus SSH/RDP or all-port ingress for `aws_security_group` | Does not model every protocol, provider, or organization exception |
| CS-201 | Wildcard actions and/or resource scope in `aws_iam_policy` and `aws_iam_role_policy` | Policy structure/conditions are not exhaustively interpreted |
| CS-301 | Delete/replace on selected persistent resource types or production-tagged resources | Resource type list and production tags are incomplete conventions |
| CS-401 | Explicit `false` encryption field on selected AWS database/EFS resources | Missing/unknown encryption fields are not inferred to be disabled |
| CS-501 | Any explicit `false` among four S3 Block Public Access flags | Effective account and organization controls are outside this offline check |
| CS-502 | Public-read/public-read-write/authenticated-read ACL for supported S3 bucket resources | Does not fully evaluate bucket policies, access points, or organization controls |

The tool does not claim that absence of findings means a plan is safe.

## 6. Risk model

For finding *i*:

\[
P_i = W(s_i) + \min(15, 3D_i)
\]

where `W` is the severity weight and `D_i` is the number of distinct downstream dependents found in the declared graph.

| Severity | Weight |
|---|---:|
| Critical | 40 |
| High | 25 |
| Medium | 12 |
| Low | 5 |

The total score is `min(100, sum(P_i))`. Bands: Low 0–19, Moderate 20–39, High 40–69, Critical 70–100. Because the model is heuristic and currently uncalibrated, the score is neither a loss estimate nor a probability. It should not be used as a sole automated approval gate.

## 7. Current validation

The current test suite contains **12 unit tests**, all of which passed in a local run on 10 October 2026. Tests exercise the risky synthetic fixture, detection of public SSH, wildcard IAM, production database deletion, selected S3 controls, encryption explicitly disabled in a constructed case, dependency context, a public HTTPS non-match, malformed input, and deterministic output.

The bundled synthetic risky fixture produces four findings: wildcard IAM scope, destructive database change, public administrative ingress, and disabled S3 public-access guardrails. Its heuristic score reaches the 100-point cap. That is an expected output for a deliberately risky test fixture, not an accuracy, benchmark, or real-environment claim.

No measured runtime benchmark, blind-label evaluation, false-positive rate, false-negative rate, user study, cost reduction, or comparison with an established scanner is reported in this version.

## 8. Evaluation plan

A meaningful next-stage study should:

1. Assemble a sanitized, versioned corpus of Terraform plans with no credentials, customer data, or exploitable secrets.
2. Define rule-level ground truth with at least two independent reviewers; resolve disagreements and report inter-rater agreement.
3. Include benign changes, isolated misconfigurations, compound misconfigurations, deletes/replacements, unknown values, and nested-module dependencies.
4. Compare InfraWeft with (a) severity-only ranking, (b) simple finding-count ranking, and (c) at least one established IaC scanner using equivalent input scope.
5. Report precision, recall, F1 by rule and overall; false positives per plan; rank correlation with reviewer priority; runtime and memory; and the effect of disabling dependency weighting (ablation).
6. Run repeated measurements where nondeterministic components exist; this version is deterministic and has no stochastic model.
7. Publish fixtures, labels, commands, and environment details so results can be independently reproduced.

Pre-register the comparison and acceptance criteria before examining results. Do not claim superiority unless measured results support it.

## 9. Threats to validity and limitations

- **Construct validity:** synthetic patterns are simpler than real-world infrastructure and can overstate apparent coverage.
- **Coverage:** current rules cover selected AWS resource shapes only. Absence of a finding means only that no current rule matched.
- **Dependency graph completeness:** declared edges do not necessarily capture every operational dependency or indirect blast radius.
- **Severity subjectivity:** the score weights are chosen for transparency, not learned or calibrated against observed incidents.
- **Input safety:** plan JSON can expose infrastructure details and values; local execution is not a license to commit plans or reports.
- **Threat adaptation:** policies, provider schemas, and cloud defaults change; rules need versioning and review.
- **Deployment risk:** InfraWeft does not run Terraform apply, fetch remote state, or make an automatic safety decision.

## 10. Ethical and operational considerations

A finding is a prompt for human review, not an instruction to disable a legitimate feature. Public endpoints may be intentional, and destructive replacements may be valid when backups and migration plans exist. Reviewers should document approved exceptions. Reports should minimize sensitive values; before public sharing, sanitize resource names, identifiers, topology, account context, and any embedded secret-like data.

## 11. Conclusion

InfraWeft demonstrates a small offline path from Terraform plan JSON to explainable findings and a transparent heuristic score. The functional prototype passes its current unit tests and makes its scope visible. It has not yet demonstrated improved accuracy, reviewer speed, or production readiness. The most valuable next contribution is a blind-labeled evaluation with realistic sanitized plans and a comparison to established tools—not a larger score or stronger marketing claim.

## References

1. HashiCorp. *JSON Output Format Overview*. https://developer.hashicorp.com/terraform/internals/json-format
2. Amazon Web Services. *Configuring block public access settings for your S3 buckets*. https://docs.aws.amazon.com/AmazonS3/latest/userguide/configuring-block-public-access-bucket.html
3. Amazon Web Services. *Granting public access to your Amazon S3 data*. https://docs.aws.amazon.com/AmazonS3/latest/userguide/granting-public-access.html
4. GitHub Docs. *Creating a pull request from a fork*. https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork
5. 3SVK Official. *National Research & Innovation Challenge Season 3 — official site and submission guide*. https://sites.google.com/view/3svk-research-s3/home
