# gramide-toml

Original scanner and grammar informed by the
[TOML 1.0 specification](https://toml.io/en/v1.0.0).

Reads assignments, bare/quoted/dotted keys, table and array-table headers,
arrays with comments and trailing commas, inline tables, booleans, integers,
floats, date/time spellings and basic/literal strings, including multiline
strings and escaped line continuations. UTF-8 ranges refer to the original
source; multiline strings and CRLF keep subsequent line numbers correct.

The package offers `tokens`, `parse`, `outline`, `symbols`, `tags` and `map`.
It does **not** advertise `check` or `symbols-recovered`. In particular it
does not validate duplicate keys/tables, table redefinition, calendar ranges,
integer bounds or Unicode scalar values in escapes. Quoted keys retain their
source quoting. Symbols describe syntactic headers and assignments; they do
not resolve implicit TOML table ownership into fully qualified semantic keys.
Some malformed key spellings remain permissive. TOML 1.1 extensions are not
claimed. Fixtures are also accepted by Python's standard `tomllib`.

From this directory: `almide test`, then
`almide build cli/main.almd -o gramide_toml`.
Regenerate the table with `./gramide_toml gen-table > src/table.almd`.

MIT or Apache-2.0, at your option; see LICENSE-MIT and LICENSE-APACHE.

Line endings follow TOML 1.0: LF or CRLF. Bare CR and raw DEL in string
literals are rejected.

## Repository contract

This repository owns this language package and its tests. `src/mod.almd` exports
`definition()` using the shared gramide package API. The `gramide-cli` repository
composes it as a git dependency; no grammar source is vendored into the CLI.
`bash ci/check.sh` runs the complete package gate with an explicit test entry
point, avoiding recursive parallel compiler fan-out. CI pins Almide and Rust
in `.github/workflows/quality.yml`.
