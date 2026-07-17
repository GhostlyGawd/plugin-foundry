# Security Policy

Nightshift Foundry plugins run on your machine. Skills can influence an agent's
behavior, and hooks can execute local code, so every package is treated as a
security-sensitive artifact.

## Report a vulnerability privately

Do not open a public issue for exploitable behavior, suspected credential
exposure, or a bypass of a host's trust controls. Use GitHub's
[private vulnerability reporting](https://github.com/GhostlyGawd/plugin-foundry/security/advisories/new).
The repository has private reporting enabled. Reports are acknowledged on the
advisory thread; reporters receive credit in the fix unless they prefer not to.

For non-exploitable defects, use the public
[bug form](https://github.com/GhostlyGawd/plugin-foundry/issues/new?template=bug.yml).
Never paste secrets, private source code, customer data, or personal information
into an issue, discussion, commission request, or pull request.

## Supported versions

Only the latest published version of each shelf plugin is supported. The same
behavior is packaged natively for Codex, Claude Code, Gemini CLI, Cursor, and
GitHub Copilot. Update instructions and host-specific package details live in
[COMPATIBILITY.md](COMPATIBILITY.md). Every downloadable ZIP has a published
SHA-256 digest in `site/downloads/index.json`.

## Enforced shipping boundary

The repository's validation, doctor, export, and QA gates enforce these rules:

- Hook matchers are narrow, lifecycle maps are host-native, and shipped scripts
  fail open unless their documented purpose is an explicit guard.
- Shipped scripts are offline: network-capable commands and URLs are rejected.
- Symlinks and credential-shaped files such as `.env`, private keys, and
  `credentials.json` are rejected before packaging.
- Scripts require a shebang and executable mode; generated adapters cannot
  drift from the shared plugin source.
- Each host archive contains only its native manifest/hook map plus the shared,
  inspectable behavior. Archives are deterministic and digest-indexed.

Installing a plugin does not bypass the host's own permission or trust model.
Inspect the ZIP, manifest, scripts, certificate, and digest before enabling it.

## Repository and automation boundary

- GitHub secret scanning, push protection, Dependabot security updates, private
  vulnerability reporting, and CodeQL are enabled for this public repository.
- GitHub Actions default to read-only permissions and cannot approve pull
  requests. Workflows declare any write permission at the smallest job scope.
- Hosted model work receives `OPENAI_API_KEY` only as an input to the
  commit-pinned official Codex Action. The model job is read-only; a separate
  keyless job validates and proposes its patch.
- Every third-party action is commit-SHA pinned. Repository policy permits only
  GitHub-owned actions plus the explicitly allowed OpenAI Codex Action.
- Repository secrets are never copied into generated pages, downloadable
  packages, logs, artifacts, or model patches.

The current tree has zero GitHub secret-scanning or Dependabot alerts. That is a
point-in-time signal, not a guarantee; the automated gates and private reporting
channel remain the safety net.
