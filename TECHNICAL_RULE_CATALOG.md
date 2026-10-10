# InfraWeft technical rule catalog

**Version context:** InfraWeft 0.1.0  
**Author:** Snehasish Das

This catalog documents the implemented rule behavior in `src/infraweft/core.py`. It is intentionally narrower than a general cloud security policy. A rule finding is a prompt for review, not an automatic verdict that a configuration is exploitable.

## Rule summary

| Rule | Current target | Trigger implemented in version 0.1.0 | Severity emitted | Example remediation |
|---|---|---|---|---|
| `CS-101` | `aws_security_group` | A changed resource's planned ingress has source CIDR `0.0.0.0/0` or `::/0`, and the rule sees SSH (22), RDP (3389), protocol `-1`, or the encoded all-port range 0–65535 | High | Restrict ingress to an approved source range or private access path |
| `CS-201` | `aws_iam_policy`, `aws_iam_role_policy` | A statement has wildcard action scope or a full wildcard resource scope; statement parsing accepts a policy object or JSON string | Critical when both action and resource scope are wildcard; otherwise High | Enumerate necessary actions and resource ARNs; add conditions when appropriate |
| `CS-301` | Selected persistent data types or any resource tagged as production | Planned actions include `delete`, and the resource is in the selected persistent-resource set or carries an `environment`, `env`, or `stage` tag with value `prod`, `production`, or `live` | Critical | Verify change approval, restore-tested backups, lifecycle controls, and downstream impact |
| `CS-401` | `aws_db_instance`, `aws_rds_cluster`, `aws_efs_file_system` | A changed resource's planned `after` object explicitly sets `storage_encrypted` or `encrypted` to Boolean `false` | High | Enable encryption and validate key, rotation, backup, and compatibility requirements |
| `CS-501` | `aws_s3_bucket_public_access_block` | One or more of `block_public_acls`, `ignore_public_acls`, `block_public_policy`, `restrict_public_buckets` is explicitly Boolean `false` | High | Enable the public-access block settings unless an approved exception exists |
| `CS-502` | `aws_s3_bucket`, `aws_s3_bucket_acl` | Planned `acl` is `public-read`, `public-read-write`, or `authenticated-read` | Critical for `public-read-write`; otherwise High | Prefer private ACLs and narrowly scoped IAM/bucket policies; verify effective account and organization controls |

## Shared behavior

- The parser requires a JSON object with a `resource_changes` array. It raises a `PlanFormatError` for an invalid root or missing/invalid array.
- Items without a usable resource address, type, and action list are skipped.
- Empty actions, `["no-op"]`, and `["read"]` are not analyzed as changes.
- Findings include a resource address, evidence path, evidence value, message, remediation, identified downstream dependents, and priority points.
- The dependency graph is read from `configuration.root_module` and recursively visited `child_modules`. Its edges come from declared `depends_on` entries represented in the plan.
- A finding's points are its severity weight plus `min(15, 3 × downstream-dependent count)`. Weights are Critical 40, High 25, Medium 12, Low 5. The overall score is the sum of finding points capped at 100.
- Sorting is deterministic: severity weight descending, dependent count descending, resource address, then rule code.

## Important boundaries and failure modes

### CS-101 — public ingress
The current code does not cover all network resource types or all firewall semantics. It checks the planned `after.ingress` representation for the exact public CIDRs and port patterns described above. It does not evaluate organization-specific exceptions or prove a route is reachable from the public internet. A public HTTPS rule is not flagged by this rule alone.

### CS-201 — wildcard IAM scope
This is a lexical rule, not a complete IAM policy evaluator. It does not fully resolve policy variables, all conditions, action semantics, permission boundaries, SCPs, resource policies, or effective permissions. A wildcard can be mitigated by other controls, while a non-wildcard policy can still be over-permissive.

### CS-301 — destructive changes
The current persistent-type set in source code is `aws_db_instance`, `aws_rds_cluster`, `aws_dynamodb_table`, `aws_s3_bucket`, `aws_efs_file_system`, `azurerm_mssql_database`, `azurerm_storage_account`, `google_storage_bucket`, and `google_sql_database_instance`. The set does not include every storage or database resource. Production identification depends on the tag keys `environment`, `env`, or `stage` with values `prod`, `production`, or `live` (case-insensitive). Replacements normally include a delete action, but nonstandard resource behavior and missing tags can affect coverage. A flagged deletion can still be intentional.

### CS-401 — encryption
Only explicit Boolean `false` values for the listed fields on the listed resource types trigger this rule. Missing or unknown values are not treated as disabled. Provider defaults, inherited settings, key policy, and encryption behavior outside those fields are not analyzed.

### CS-501 and CS-502 — S3 public access
These rules inspect selected bucket-level fields and ACL literals. They do not calculate effective access across account-level or organization-level Block Public Access settings, bucket policies, access points, object ownership, or every supported S3 configuration. A reported issue requires contextual review; absence of a finding is not evidence that the bucket is private.

## Reviewer decision record

For each finding, a reviewer should record:

1. **Disposition:** confirmed, approved exception, false positive, or requires investigation.
2. **Context:** why the rule does or does not apply in the target environment.
3. **Action:** remediation commit, exception owner and expiry, or follow-up issue.
4. **Evidence:** a sanitized plan path or configuration reference that does not expose secrets.

This record is not emitted by version 0.1.0; it is a suggested human review practice.

## References

- HashiCorp, *JSON Output Format Overview*: https://developer.hashicorp.com/terraform/internals/json-format
- HashiCorp, *`terraform show` command*: https://developer.hashicorp.com/terraform/cli/commands/show
- AWS, *Prepare for least-privilege permissions*: https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html
- AWS, *Configuring Block Public Access settings for S3 buckets*: https://docs.aws.amazon.com/AmazonS3/latest/userguide/configuring-block-public-access-bucket.html
