# SpinDoctor Qwerty for Claude

**spindoctor-qwerty-claude** is a **Claude plugin** for claude.ai chat, Cowork and Claude Code. It packages the SpinDoctor Qwerty
quantum-circuit **simulator** as a skill (with the engine inside it), four commands, a helper agent and a local MCP server. Claude can
then build and run circuits with SpinDoctor's `q.*` commands, run any of the 241 presets, process a folder of command files with
`q.folder`, test a theory you give it, and write TXT, PDF, JSON and CSV reports.

- Version **1.1.0**, engine at **SpinDoctor 3.1.2 parity** (update 3.1.2-298-20261010).
- The plugin is the repository root, laid out as in <https://claude.com/docs/plugins/build>: `.claude-plugin/plugin.json`,
  `skills/spindoctor-qwerty/` (`SKILL.md` + the bundled engine), `commands/`, `agents/`, `.mcp.json`, README and LICENSE.
  `.claude-plugin/marketplace.json` makes the same repo a one-plugin marketplace (`spindoctor-qwerty-claude`).
- `tools/build_plugin.py` builds `dist/spindoctor-qwerty.plugin`, the ZIP that claude.ai and Cowork accept under **Upload plugin**.
- No hooks, no `bin/`, no network access, no installs. The engine is pure Python (standard library only; NumPy is used if present).
- The Claude plugin manifest has no versioned schema (`$schema` is optional and ignored by Claude Code); the files pass
  `claude plugin validate` from Claude Code 2.1.296.

> **Honest limits.** SpinDoctor runs classical FP64 arithmetic on your computer (or in Claude's code sandbox). It is **not** a quantum
> computer, never contacts quantum hardware, and gives no quantum speed-up or quantum advantage. Registers hold 1-298 logical qubits, but
> any group of entangled qubits (one "factor") is limited to 59 qubits, and dense factors are limited much further by memory
> (2^n x 16 bytes; about 22 qubits with the standard library, more with NumPy). Registers wider than 29 qubits sample in basis Z only.
> Python 3.8 or newer is required (`python3` on PATH).

## Which repository should I use?

| You use... | Choose |
| --- | --- |
| claude.ai chat or Cowork (upload a `.plugin` file), or one plugin that works across claude.ai, Cowork and Claude Code | **this repo**, `spindoctor-qwerty-claude` |
| Claude Code only, and want CLI-first slash commands (run, script, preset, folder, report, functions, theory), a subagent, a Windows Python switcher and a team settings file | [spindoctor-qwerty-claude-code](https://github.com/LKVexa/spindoctor-qwerty-claude-code) |

Both bundle the same engine and give the same results. In Claude Code, enable only **one** of them, because both start the same
six tools. The plugin names differ (`spindoctor-qwerty` here, `spindoctor-qwerty-code` there), so their commands never clash.

## What runs where

| Surface | What loads | How SpinDoctor runs |
|---|---|---|
| claude.ai chat (web, desktop, mobile) | skill + commands (as skills) | Claude runs the bundled CLI with its code tool; local MCP servers are not started in chat |
| Cowork | skill, commands, agent; the local MCP server when the Cowork session runs on your computer | `spindoctor_*` tools, or the CLI |
| Claude Code | everything | `spindoctor_*` MCP tools (`/mcp` shows the server), or the CLI |

## Install

**claude.ai / Cowork**
- From this repo: **Customize > Plugins > Add marketplace**, enter `LKVexa/spindoctor-qwerty-claude`, then install **SpinDoctor Qwerty**.
- From a file: run `python3 tools/build_plugin.py`, then **Customize > Plugins > Add > Upload plugin** and choose
  `dist/spindoctor-qwerty.plugin`. A plugin added to your account also appears in Claude Code as a synced plugin.

**Claude Code** (needs Python 3.8+ as `python3`):
```sh
claude plugin marketplace add LKVexa/spindoctor-qwerty-claude
claude plugin install spindoctor-qwerty@spindoctor-qwerty-claude
```
or, in a session, `/plugin install spindoctor-qwerty --marketplace LKVexa/spindoctor-qwerty-claude`. To try it without installing:
`claude --plugin-dir ./spindoctor-qwerty-claude`. Check with `claude plugin list` and `claude mcp list` (the server shows as
`plugin:spindoctor-qwerty:spindoctor-qwerty ... Connected`), then ask *"show the SpinDoctor functions"*.

`.mcp.json` starts `python3 ${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_mcp.py` with reports in
`${CLAUDE_PLUGIN_DATA}/workspace` (Claude Code keeps it under `~/.claude/plugins/data/`). On Windows, if `python3` is not available,
change `"command"` to `"python"` in a clone and install from that folder.

## Commands

| Command | What it does |
|---|---|
| `/spindoctor-qwerty:qwerty-run <q.* commands>` | Runs q.* commands and summarises probabilities, counts and report paths |
| `/spindoctor-qwerty:qwerty-preset <qc-NNN> [name=value ...]` | Runs one of the 241 presets |
| `/spindoctor-qwerty:qwerty-functions [section] [filter]` | Shows the function table |
| `/spindoctor-qwerty:qwerty-theory <file \| text \| "we discussed">` | Tests a theory and writes a theory test report |

The agent `spindoctor-qwerty:qwerty-helper` (Cowork and Claude Code) runs scripts, presets, folders and theory tests and explains them.

## What you can ask for

## SpinDoctor Qwerty - plugin tools

| Function | What it does | Command to type |
|---|---|---|
| Function table (spindoctor_functions) | Show this table in chat | Ask: "show the SpinDoctor functions" (CLI: `spindoctor_cli.py functions`) |
| Run a script (spindoctor_run_script) | Run any q.* lines above; returns results + TXT/JSON/CSV/PDF report paths | Ask: "run q.circuit new bell 2 / q.circuit add h 0 / ..." |
| Run a preset (spindoctor_run_preset) | Run qc-001..qc-241 with overrides | Ask: "run preset qc-067 with shots=64" |
| List presets (spindoctor_list_presets) | Search the 241 presets | Ask: "list presets about Grover" |
| Read a report (spindoctor_report) | List/read TXT reports (PDF/JSON paths alongside) | Ask: "show the newest SpinDoctor report" |
| Test a theory from a file (spindoctor_test_theory source=file) | Read a .txt/.md/.pdf/.py/.json/.csv/.q attachment, then hypothesis -> prediction -> q.* script -> run -> verdict + TXT/PDF theory report | Ask: "test the theory in C:/notes/theory.md" (the host must pass the file path/content) |
| Test a theory from text (spindoctor_test_theory source=text) | Same pipeline for pasted text | Ask: "test this theory: a Hadamard on \|0> gives 50/50" |
| Test the theory we discussed (spindoctor_test_theory source=chat) | The AI summarises the theory from the conversation (claims, assumptions, variables, prediction), you confirm, then it is tested; quoted excerpts go in the report under 'Source: chat history'. An exported chat transcript (.txt/.md/.json/.html) also works | Ask: "test the theory we discussed" or "test the theory in my exported chat C:/chats/conversation.json" |

Every command family is listed with a runnable example in **[FUNCTIONS.md](FUNCTIONS.md)** (the exact table the tool shows):
circuits (`q.circuit`, including 298-qubit wide registers and the `mcx7` gate), queries (`q.query`), the tranche register
(`q.tranche`), the procedural grid, presets and sequences, resource planning, math calculators, physics models, lessons, noise, error
correction, compilation, algorithms, inputs/folders/history (`q.input`, `q.folder`, `q.history`) and the cartridge commands.

## Theory testing

`spindoctor_test_theory` turns a claim into a test: hypothesis -> measurable prediction -> `q.*` script -> run -> compare -> a TXT +
JSON + PDF **theory test report** with the hypothesis, script, raw results, verdict (*supported*, *not supported* or *inconclusive*)
and limits.

- **From a file:** .txt, .md, .pdf, .py, .json, .csv or .q. In Claude Code, give the file's path. In claude.ai, uploaded files appear in the code sandbox (usually under `/mnt/user-data/uploads/`) and Claude passes that path.
- **From pasted text.**
- **From the chat history:** say *"test the theory we discussed"*. The model writes a short summary (claims, assumptions, variables,
  measurable prediction), shows it to you to confirm or correct, then passes it with optional quoted excerpts; the report records them
  under *Source: chat history*. Exported chat transcripts (.txt/.md/.json/.html from ChatGPT, Claude and others) also work.
- The plugin cannot read your conversation or attachments by itself: only the model sees them, and very long conversations may already
  be truncated by the context window.

Sample theory files and chat transcripts are in `skills/spindoctor-qwerty/examples/theory/`. The two sample
PDFs are stored as text; run `python3 skills/spindoctor-qwerty/examples/theory/make_sample_pdfs.py` to
recreate them.

## Folder ingestion (`q.folder`)

`q.folder run path="<folder>"` runs every supported file at the top level of a folder (.txt, .csv, .json, .qasm, .qasm2, .circuit,
.pdf) in ordinal name order: 1-128 supported files, at most 4 MiB per file, 1-128 commands per file and 4096 characters per command,
strict UTF-8. Other files (for example .md) are skipped and listed. The first failing file stops the job.

## Testing

| Test | Command | Result for 1.1.0 |
|---|---|---|
| Host check with the **real Claude Code CLI** | `CLAUDE=$(command -v claude) python3 tests/claude_host_check.py` | 16/16 checks, end-to-end 12/12 |
| Same without Claude Code | `python3 tests/claude_host_check.py` | 9/9 checks, end-to-end 12/12 |
| `.plugin` zip | `python3 tools/build_plugin.py` (twice: same SHA-256) | 47 files, identical hashes |

**Real host, tool calls host-simulated:** Claude Code 2.1.296 was installed from npm on a Linux test machine and used **without signing
in** and without calling a model. It validated the marketplace, the manifest and the unzipped `.plugin`, added the marketplace, installed
the plugin, listed it enabled at 1.1.0, showed its 5 skills, 1 agent and 1 MCP server, started the MCP server and reported it
**Connected**, and did the same for the unzipped `.plugin` with `--plugin-dir`. Calling tools through Claude Code needs a signed-in session,
so `tests/e2e_mcp.py` drives the server from Claude Code's installed copy, launched exactly as `.mcp.json` declares. claude.ai and
Cowork were not tested (they need an account). Details in [E2E_RESULTS.md](E2E_RESULTS.md).

## Author and license

Author: **RUSSELL PHILIP SMITHSON** <russellsmithson77@outlook.com>

Copyright (C) 2026 RUSSELL PHILIP SMITHSON. Licensed under the GNU General Public License v3.0 or later (`GPL-3.0-or-later`): see
[LICENSE](LICENSE), [NOTICE](NOTICE) and [COPYRIGHT](COPYRIGHT). `plugin.json` and `marketplace.json` carry the license and author.
Claude and Claude Code are trademarks of Anthropic; this project is not affiliated with Anthropic.
