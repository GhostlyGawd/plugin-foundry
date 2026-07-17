# Cross-host plugin packages

Every Nightshift Foundry plugin has one inspectable source and five native
packages. Skills and scripts stay shared; generated metadata adapts each host's
manifest, lifecycle-event names, and plugin-root variable.

| Host | Native archive manifest | Native archive hooks |
| --- | --- | --- |
| Claude Code | `.claude-plugin/plugin.json` | `hooks/hooks.json` |
| Codex | `.codex-plugin/plugin.json` | `hooks/codex.json` (Open Plugin events) |
| Gemini CLI | `gemini-extension.json` | `hooks/hooks.json` (Gemini events) |
| Cursor | `.cursor-plugin/plugin.json` | `hooks/cursor.json` |
| GitHub Copilot CLI | `.github/plugin/plugin.json` | `hooks/copilot.json` (Open Plugin events) |

The behavior lives once in `skills/` and `scripts/`. `tools/adapters.py` derives
the host manifests and lifecycle maps, while `tools/validate.py` blocks drift.
`tools/export.py` keeps incompatible schemas out of one another's ZIPs. This is
necessary because Claude/Open Plugin and Gemini both reserve `hooks/hooks.json`
but define different event names. Hook-enabled plugins remain fail-open or
advisory exactly as their records specify.

## Install

Replace `PLUGIN` below with a shelf name such as `commit-craft`.

### Claude Code

```text
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install PLUGIN@foundry
```

### Codex

Add the Git marketplace, then install from the **Nightshift Foundry** source in
the ChatGPT desktop app's Plugins Directory:

```bash
codex plugin marketplace add GhostlyGawd/plugin-foundry
```

The repo-native catalog is `.agents/plugins/marketplace.json`. Codex caches the
selected plugin and loads its `.codex-plugin/plugin.json` manifest.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add GhostlyGawd/plugin-foundry
copilot plugin install PLUGIN@foundry
```

### Gemini CLI

Download the plugin's `gemini-cli` ZIP from the living window, extract it, then:

```bash
gemini extensions install ./PLUGIN
```

Gemini copies the extension at install time. Run
`gemini extensions update PLUGIN` after replacing the local package with a newer
download.

### Cursor

Download and extract the plugin's `cursor` ZIP into Cursor's local-plugin
directory:

```bash
# macOS / Linux
mkdir -p ~/.cursor/plugins/local
cp -R ./PLUGIN ~/.cursor/plugins/local/PLUGIN
```

On Windows, copy it to `%USERPROFILE%\.cursor\plugins\local\PLUGIN`. Restart
Cursor or run **Developer: Reload Window**; the plugin appears under
**Settings → Plugins → Installed**. The repository also carries
`.cursor-plugin/marketplace.json` for marketplace/team import workflows.

## Verify a download

`site/downloads/index.json` publishes every host package's version, byte size,
and SHA-256 digest. Archives are deterministic: identical source produces
identical bytes. To rebuild and compare locally:

```bash
python3 tools/adapters.py --check
python3 tools/export.py --all
```

## Runtime requirements and trust

- Skills are Markdown and need no plugin-specific credentials.
- Hook-enabled packages use small Bash scripts and may require `git` and
  `python3`; inspect each plugin's Trust & footprint section before enabling.
- Hooks make no network calls and do not receive Foundry service credentials.
- Claude, Codex, Copilot, Cursor, and Gemini apply their own plugin/hook trust
  controls. Installing a package does not bypass a host's permission model.

Official format references: [Claude Code plugins](https://code.claude.com/docs/en/plugins-reference),
[Codex plugins](https://developers.openai.com/codex/plugins/build),
[Gemini CLI extensions](https://geminicli.com/docs/extensions/reference/),
[Cursor plugins](https://github.com/cursor/plugins), and
[GitHub Copilot CLI plugins](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).
