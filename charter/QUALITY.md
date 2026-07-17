# QUALITY — What Makes a Plugin Great

A plugin is a guest in someone else's session: it costs context on every launch, runs
code on their machine, and speaks for this marketplace. Judge accordingly.

## The six axes (score 1–5 each; Reviewer records scores at sign-off)

1. **Scope discipline.** One job, done whole. Every component earns its place; a
   plugin that "also" does things is two plugins or half of one.
2. **Prompt craft.** Skill/agent bodies are excellent prompts: concrete procedure,
   inputs/outputs named, edge behavior specified. Descriptions are the auto-invoke
   trigger — write them so the installed host fires the component exactly when it
   should and never otherwise.
3. **Token thrift.** Budget: ≤ ~300 always-on tokens per plugin (descriptions +
   listing text) unless an ADR grants more. Heavy reference material goes in skill
   supporting files (loaded on invoke), never in descriptions. Check with
   `claude plugin details <name>` when the CLI is available.
4. **Hook safety.** Read-only or reversible effects; narrow matchers (`Write|Edit`,
   not `.*`); graceful failure (a broken hook must never brick a session); quoted
   target-native plugin-root variables; executable scripts with shebangs; no network
   calls or writes outside the project without loud documentation.
5. **Docs truth.** README's install and usage lines work as pasted; examples are
   real; CHANGELOG tells the version story; the record's spec matches what shipped.
6. **Structural correctness.** Official layouts exactly: components at plugin root;
   native Claude, Codex, Cursor, Copilot, and Gemini manifests; target-native hook
   maps; kebab-case name; relative `./` paths; semver in sync. Passes
   `tools/adapters.py --check`, `tools/validate.py`, and Claude's strict validator.

## Gate bars
- **→ rc:** QA Test log with `TEST VERDICT: pass`; axes 4 and 6 at 5 (safety and
  structure are pass/fail, not gradients).
- **→ published:** Reviewer sign-off with all axes ≥ 4; marketplace entry + version
  + CHANGELOG in sync.
- **Bounce** is one stage back with reasons in the record. Two bounces on the same
  cause → `blocked:` in BACKLOG with diagnosis.

## House anti-patterns (automatic bounces)
- Kitchen-sink plugins ("dev-tools-plus") — bounce at spec.
- Vague descriptions ("Helps with your code") — bounce at review; the description IS
  the invocation contract.
- `matcher: ".*"` hooks, destructive hooks, or unquoted plugin-root paths — bounce
  at QA, always.
- Shipping process files (records, test scratch) inside `plugins/<name>/` — bounce.
- Editing a published plugin without a version bump + CHANGELOG entry — Version-law
  violation; Maintainer reverts or completes it.

## The metadata exemption (ADR-013)
Weekly re-verification refreshes `verified:` (and `tested_with` when the CLI is
present) on published records. These are metadata-only writes: exempt from the
version-bump law because no plugin file changes and behavior is untouched. Any
write under plugins/ remains fully bound — version numbers keep meaning
"behavior changed". Stamps are withheld from records whose suites fail; a stale
stamp is a signal, never a cosmetic.
