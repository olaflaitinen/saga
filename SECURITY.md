# Security policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

Only the latest release in the 1.x series receives security fixes. Older major versions are
not supported.

## Reporting a vulnerability

Please do NOT report security vulnerabilities through public GitHub Issues. Instead, disclose
them privately to the corresponding author by email.

**Contact:** olaf.laitinen@su.se

**Subject line:** Use the subject prefix `[SAGA SECURITY]` so that the message is routed
correctly.

**Expected response time:** 5 working days from receipt of the initial disclosure.

**Responsible disclosure:** We ask that you allow a 90-day window from the date of initial
disclosure before any public disclosure of the vulnerability. This window may be extended by
mutual agreement if a fix requires coordination with a third-party dependency maintainer.

## Scope

The following categories of issues fall within the security scope of this repository:

- Vulnerabilities in the Python source code that could allow arbitrary code execution when
  processing untrusted input data (for example, a maliciously crafted parquet file or YAML
  configuration file passed to the SAGA pipeline).
- Vulnerabilities in the Docker image that expose the host system or other containers.
- Dependency vulnerabilities in packages listed in `requirements.txt` or `environment.yaml`
  that have a CVE with a severity of High or Critical.

The following are out of scope:

- Vulnerabilities in the GitHub Actions CI infrastructure (report these to GitHub).
- Issues that require physical access to the SCB MONA secure compute environment (these are
  governed by Statistics Sweden's own security policies).
- Social-engineering attacks on individual contributors.

## Dependency scanning

Dependabot is enabled on this repository (see `.github/dependabot.yaml`) and scans pip,
GitHub Actions, and Docker dependencies weekly. Dependabot pull requests for non-major
version upgrades are opened automatically. Major-version upgrades are flagged but not
auto-opened to avoid breaking API changes.

CodeQL analysis and Bandit static analysis run weekly via the `.github/workflows/security.yaml`
workflow. Results are available on the GitHub Security tab.
