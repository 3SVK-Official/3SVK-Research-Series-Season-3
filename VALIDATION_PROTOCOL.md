# InfraWeft validation protocol

**Status:** Proposed protocol; not yet executed  
**Author:** Snehasish Das  
**Implementation under study:** InfraWeft 0.1.0

## 1. Objective

Test two different claims separately:

1. **Detection claim:** the implemented rules identify the specific conditions they are intended to match in the tested inputs.
2. **Prioritization claim:** adding declared dependency context improves the ordering of review items against independently adjudicated reviewer priorities.

Passing the current unit tests supports only code behavior on a small set of examples. It does not establish field accuracy or prove the prioritization claim.

## 2. Research questions

- RQ1: What precision, recall, and F1 score does each rule achieve on a labeled test corpus?
- RQ2: Does dependency weighting better align output order with reviewer-assigned impact priority than severity-only and finding-count baselines?
- RQ3: How often are results limited by missing or indirect dependency edges?
- RQ4: What is the runtime and memory footprint on plans of different sizes?

All answers should be reported from observed measurements, not inferred from the prototype design.

## 3. Corpus design

Build a versioned collection of sanitized Terraform plan JSON from:
- Minimal synthetic cases for each implemented rule.
- Benign controls, including expected public HTTPS ingress.
- Compound cases in which several supported patterns coexist.
- Destructive changes with and without recognized production tags.
- Missing, null, unknown, and malformed attributes.
- Dependency chains, multiple downstream branches, and nested modules.
- Cases using unsupported resource types to test the limits of scope disclosure.

Synthetic cases should be marked as synthetic in the manifest. They should not be mixed with sanitized real plans without an explicit `source_type` field. No production identifiers, secrets, or customer information should be included.

## 4. Labeling procedure

1. Prepare a written labeling guide with one definition per rule and a severity rubric.
2. Have two reviewers label each corpus item independently before viewing InfraWeft's output.
3. Record rule presence, severity, whether the finding is actionable, expected impact priority, and confidence.
4. Resolve disagreements through a documented adjudication step; retain both initial labels and the adjudicated label.
5. Record experience level and conflicts of interest for reviewers.
6. Keep a held-out evaluation set separate from development fixtures. Split by project or origin, not by individual rows from the same project, to reduce leakage.

If two independent reviewers cannot be obtained, report the limitation; do not describe a single-author label set as independent ground truth.

## 5. Baselines and ablation

Run identical inputs through:
- **B1 — Severity-only:** rank findings by rule severity.
- **B2 — Severity plus count:** add a predeclared bonus based on number of findings for a resource or plan.
- **B3 — InfraWeft score:** current severity weight plus capped declared downstream-dependent count.
- **B4 — External tool:** one established IaC scanner, with version, configuration, and supported-rule mapping documented.

Run an ablation with the dependency bonus set to zero. Do not compare tools on issue classes one tool cannot represent without explaining the mismatch.

## 6. Metrics

Detection:
- Per-rule precision, recall, and F1.
- Macro-average and micro-average, when the dataset supports them.
- False-positive and false-negative counts with case identifiers.
- Results stratified by synthetic/real source and by rule.

Ranking:
- Spearman rank correlation or a suitable rank-based metric against adjudicated priority.
- Top-k recall for critical findings.
- Pairwise ranking agreement.
- Difference between full score and dependency-bonus ablation.

Operations:
- Wall-clock runtime, peak memory, plan size, Python version, platform, and InfraWeft commit hash.
- Parse failures and skipped/unsupported cases.
- Dependency-edge coverage for cases with known graph structure.

Report confidence intervals where the sample size and design justify them. If the sample is too small, provide counts and avoid overstated statistical conclusions.

## 7. Pre-registered decision criteria

Before running held-out cases, record:
- The exact corpus version and hash.
- Baselines and configuration.
- The minimum number of cases per supported rule.
- The acceptable false-negative tolerance and the rationale for it.
- The rank metric and the minimum improvement considered useful.
- Handling of ties, unsupported inputs, and reviewer disagreement.

A result should not be described as an improvement unless the predeclared criteria are met on held-out cases. If criteria are not met, report the negative or inconclusive result.

## 8. Reproduction record template

For every execution, retain:

```text
Study ID:
Git commit:
Corpus version and SHA-256:
Python version:
Operating system:
Command:
Tool versions and options:
Number of plans:
Number of labels:
Parse failures:
Per-rule precision / recall / F1:
Ranking metric and uncertainty:
Runtime and memory:
Deviations from protocol:
```

Do not add results to the paper until the experiment has actually been run and raw outputs can be inspected. Current status remains: 12 unit tests passed locally on the original synthetic tests; the study in this document has not been executed.
