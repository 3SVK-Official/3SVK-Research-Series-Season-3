# Finding triage runbook

**Project:** InfraWeft 0.1.0  
**Author:** Snehasish Das

## Purpose

Use this checklist to review InfraWeft output consistently. The tool reports selected static signals; it does not approve, reject, or apply a Terraform plan.

## Step 1 — Confirm context

Before interpreting findings, verify:
- The plan was generated for the intended workspace, branch, and change.
- The plan is current and was generated with the expected Terraform/provider versions.
- The report corresponds to the exact plan being reviewed.
- The report contains no values that must remain confidential before sharing.

## Step 2 — Review each finding

For every finding:

1. Open the cited `evidence_path` in the report input or corresponding plan representation.
2. Check the `resource` address and planned action.
3. Compare the `evidence` value with the trigger described in `docs/TECHNICAL_RULE_CATALOG.md`.
4. Consider context not represented by the rule: approved network boundaries, effective IAM controls, account-level policies, backups, maintenance windows, and business purpose.
5. Record one disposition:
   - **Confirmed risk** — evidence matches an unacceptable condition.
   - **Approved exception** — condition is intentional and an accountable owner has approved it.
   - **False positive** — rule interpretation does not apply to the actual configuration.
   - **Needs investigation** — there is not enough context to decide.
6. Record the responsible owner, action or rationale, and follow-up reference.

Do not immediately apply a generic remediation without considering availability, recovery, compatibility, and intended architecture.

## Step 3 — Interpret the score correctly

The aggregate score is generated from fixed severity weights and a capped bonus for declared downstream dependencies. It is a prioritization aid, not a probability, expected loss, or certification. A score of 100 means the sum reached the configured cap; it does not mean a 100% chance of an incident.

Read the individual evidence and severity before using the aggregate score to order work. Two reports with similar scores can represent different risks.

## Step 4 — Interpret an empty report correctly

“No findings matched” means only that the current rules did not match the inspected representation. It does not mean:
- the plan is secure,
- every relevant resource type was inspected,
- unknown values were resolved,
- effective cloud permissions were calculated, or
- runtime and organization controls were evaluated.

Continue ordinary infrastructure review and run the organization's approved policy and scanning tools.

## Step 5 — Escalation

Escalate immediately through the organization's normal security/change process when evidence suggests exposed administrative access, excessive privilege, potential data loss, or an unexplained change to data protection controls. Include sanitized evidence and the exact plan revision. Do not put unredacted plan JSON into public issues or pull requests.

## Review record template

```text
Plan/change reference:
InfraWeft version and commit:
Finding rule and resource:
Disposition:
Evidence reviewed:
Context not represented by the rule:
Decision and rationale:
Owner:
Remediation or exception reference:
Follow-up date:
Reviewer:
```

The record is a human process artifact; version 0.1.0 does not store these fields automatically.
