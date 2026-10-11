# End-to-end results - spindoctor-qwerty-claude 1.1.0

Date: 2026-10-10 (PT). Engine 1.1.0, parity target: **updated SpinDoctor 3.1.2** (build 3.1.2-298-20261010).

**Publishing decision (recorded as instructed):** Russell approved publishing on the basis of the updated SpinDoctor 3.1.2 passing its own
test suite 18/18, with the three 29-qubit test checks adapted to the new 298-qubit limit.

## Host

- **Real host: Claude Code CLI 2.1.296** (`@anthropic-ai/claude-code`), installed from npm on a Linux test machine. No sign-in, no API
  key, no model call; each run used a throw-away `HOME`.
- Schema rule: newest schema the real host accepts. The Claude plugin manifest and marketplace file have no versioned schema (`$schema`
  is optional and ignored at load time), so they are checked with Claude Code's own `claude plugin validate` and the documented rules.
  Agent Plugins and MCPB do not apply to this package.
- **Tool calls are host-simulated:** Claude Code only calls MCP tools inside a signed-in session. It does start the plugin's server and
  reports it Connected (that's an MCP initialize handshake), but the end-to-end tool calls are made by `tests/e2e_mcp.py` against Claude
  Code's installed copy of the plugin, launched exactly as `.mcp.json` declares (`${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}` expanded).
- claude.ai chat and Cowork were not tested (they need an Anthropic account).

## Clean-room gate (before push)

The staged repo was copied to a fresh empty folder and run with an empty environment (`env -i`, only `PATH` and a fresh `HOME`), following
only the README.

| Run | Command | Result |
|---|---|---|
| Real Claude Code | `CLAUDE=<claude> python3 tests/claude_host_check.py` | **16/16** checks, end-to-end **12/12** |
| Stand-in (no Claude Code on PATH) | `python3 tests/claude_host_check.py` | **9/9**, end-to-end **12/12** |
| `.plugin` | `python3 tools/build_plugin.py` (twice) | 47 files, identical SHA-256 |
| Sample PDFs | `python3 skills/spindoctor-qwerty/examples/theory/make_sample_pdfs.py` | 2 PDFs written (git-ignored, not packed) |

Static checks: plugin.json (name rules incl. reserved names, displayName, version, description, author, license, homepage URL);
marketplace.json (name, owner, source "./", version); .mcp.json (stdio, plain file argument under `${CLAUDE_PLUGIN_ROOT}`, workspace under
`${CLAUDE_PLUGIN_DATA}`); front matter of the skill, 4 commands and the agent; no `bin/`, no hooks; README 40+ words; LICENSE; text files only;
`.plugin` zip (manifest at the zip root, no `bin/`, 47 files, about 925 KB, text only).

Real Claude Code checks: `claude plugin validate` for the marketplace, the manifest and the unzipped `.plugin`; `claude plugin marketplace add
<repo>`; `claude plugin install spindoctor-qwerty@spindoctor-qwerty-claude`; `claude plugin list` (1.1.0, enabled); `claude plugin details`
(5 skills = skill + 4 commands, 1 agent `qwerty-helper`, 1 MCP server, 0 hooks); `claude mcp list` (server started, **Connected**);
`claude --plugin-dir <unzipped .plugin> mcp list` (**Connected**); end-to-end.

End-to-end (`tests/e2e_mcp.py`):

| Check | Result |
|---|---|
| initialize (server spindoctor-qwerty 1.1.0) | PASS |
| tools/list exposes the 6 tools | PASS |
| function table (Markdown, 19 sections, 298-qubit limits listed) | PASS |
| 241 presets listed | PASS |
| one script per command family (16 families, every table example) | PASS |
| 298-qubit circuit with mcx7 (prepared-factor Born-Z) | PASS |
| q.folder on a mixed .txt/.csv/.json/.qasm folder (+ .md skipped) | PASS |
| theory from a file -> supported, TXT+PDF report | PASS |
| theory from a chat summary + quoted excerpts -> supported | PASS |
| theory from an exported chat transcript -> supported | PASS |
| presets qc-001..qc-025 vs the updated 3.1.2 reference (20 identical, 5 documented differences) | PASS |
| TXT+PDF reports valid (255 PDFs, 255 TXT twins) | PASS |

The 5 documented preset differences are the engine's known, accepted work-accounting counters, as in every spindoctor-qwerty repo.

## Post-push check

After publishing (commit df8a9fd3034e6117c5e69cbc6dafcc064cc53c04), the repo was cloned back from GitHub into a fresh folder:

- 56/56 files byte-identical to the staged copy; the clone's working tree stayed clean after the tests.
- **Real Claude Code, straight from GitHub:** `claude plugin marketplace add LKVexa/spindoctor-qwerty-claude` +
  `claude plugin install spindoctor-qwerty@spindoctor-qwerty-claude` -> 1.1.0 enabled, copied to
  `~/.claude/plugins/cache/spindoctor-qwerty-claude/spindoctor-qwerty/1.1.0/`; `claude mcp list` -> **Connected**; end-to-end against that
  GitHub-installed copy **12/12**.
- From the clone, empty environment: `tests/claude_host_check.py` with real Claude Code **16/16** (end-to-end 12/12); without Claude Code
  **9/9** (end-to-end 12/12).
