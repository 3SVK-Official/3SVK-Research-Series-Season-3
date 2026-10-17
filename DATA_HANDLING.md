# Data handling and reproducibility notes

**Project:** InfraWeft  
**Author:** Snehasish Das

## 1. Why plan JSON requires care

Terraform's `show -json` representation is machine-readable and useful for automated inspection. It can also expose sensitive values in plain text, including values represented as sensitive in Terraform. Treat plan JSON and reports generated from it as potentially confidential.

Official reference: HashiCorp, [`terraform show`](https://developer.hashicorp.com/terraform/cli/commands/show).

## 2. Data classes

| Class | Examples | Public-repository rule |
|---|---|---|
| Public synthetic | Hand-authored sample plans with fake names and no credentials | May be published after checking the diff |
| Sanitized research | Plan derived from a real project after documented sanitization and approval | Publish only when ownership and disclosure approval are confirmed |
| Internal infrastructure | Real resource names, account IDs, addresses, module paths, planned values | Do not publish by default |
| Secret-bearing | Tokens, passwords, private keys, cloud credentials, secret values | Never commit; rotate/revoke if exposed |

## 3. Safe local workflow

1. Store real plan files in a controlled working directory outside the Git repository.
2. Generate JSON locally and run InfraWeft against that path.
3. Write output to a private location; do not attach it to public CI logs by default.
4. Inspect the report for values, resource addresses, account identifiers, service names, network topology, and internal hostnames.
5. Sanitize copied examples using stable fake identifiers, then verify that the sanitized fixture still tests the intended behavior.
6. Run a repository diff and secret scan before pushing.

Example `.gitignore` entries for a local repository (adapt them to the project's established ignore policy):

```gitignore
# Local Terraform artifacts and state
*.tfstate
*.tfstate.*
*.tfplan
tfplan
tfplan.json

# Locally generated reports from real infrastructure
infraweft-private-report.*
```

Do not remove existing ignore rules. These patterns are safeguards, not a guarantee that sensitive files can never be committed.

## 4. Reproducibility metadata

For a test run, record the repository commit, Python version, operating system, command, test result, and whether all inputs were synthetic. For future benchmark runs, also record the corpus hash, label-set version, scanner versions, configuration, and deviations from protocol.

Synthetic examples should have:
- A unique case identifier.
- A short purpose statement.
- Declared expected rule codes.
- An explanation of the intended positive or negative behavior.
- No values copied from live infrastructure.

## 5. Public release check

Before creating a release or pull request:
- Inspect staged and unstaged diffs.
- Confirm fixtures contain only synthetic values.
- Confirm no Terraform state, plan binary, credential, or unredacted plan JSON is present.
- Verify that outputs in documentation match the code and fixtures.
- Retain enough local metadata to repeat any claimed test run.

This process supports reproducibility but is not a formal certification or complete privacy guarantee.
