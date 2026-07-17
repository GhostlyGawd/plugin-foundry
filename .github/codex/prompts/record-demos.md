# Record real plugin demos

Refresh the dated demo transcripts in `foundry/demos/`.

For every `foundry/demos/prompts/*.prompt` file:

1. Match it to `plugins/<name>/` and read that plugin's manifest, skills, scripts,
   and current tests before running anything.
2. Create a disposable Git repository outside the checkout and carry out the
   prompt there using the matching plugin skill as the procedure. Do not install
   packages, use network access, or read credentials.
3. Write only `foundry/demos/<name>.txt`. Start with `recorded: YYYY-MM-DD`, then
   include the prompt and the concise final response produced from the disposable
   fixture. Never invent command output; if a task cannot run safely and locally,
   leave the previous transcript unchanged and explain the skip in your final
   message.

Do not edit plugins, records, state, workflows, generated site files, or existing
transcripts that have no matching prompt. Do not commit, push, or open a PR. A
separate job will validate and propose the exact transcript-only patch.
